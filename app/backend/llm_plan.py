import os
from dotenv import load_dotenv
import psycopg
import requests
from psycopg.types.json import Json


def main() -> None:
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL mangler. Tjek app/backend/.env")

    display_name = os.getenv("APP_USER_DISPLAY_NAME", "Eliza")
    events_limit = int(os.getenv("EVENTS_LIMIT", "30"))
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
    ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

    todos_limit = int(os.getenv("TODOS_LIMIT", "20"))

    try:
        tags_resp = requests.get(f"{ollama_base_url}/api/tags", timeout=10)
        tags_resp.raise_for_status()
        tags_data = tags_resp.json()
        installed_models = [m.get("name") for m in tags_data.get("models", []) if m.get("name")]
    except requests.RequestException as e:
        raise RuntimeError(
            "Kunne ikke kontakte Ollama på OLLAMA_BASE_URL. "
            "Sørg for at Ollama kører lokalt og at OLLAMA_BASE_URL peger korrekt. "
            f"Detalje: {e}"
        )

    if installed_models and ollama_model not in installed_models:
        preferred = None
        if "qwen2.5:3b" in installed_models:
            preferred = "qwen2.5:3b"
        elif "qwen2.5:1.5b" in installed_models:
            preferred = "qwen2.5:1.5b"
        elif installed_models:
            preferred = installed_models[0]

        if preferred:
            print(
                "Bemærk: OLLAMA_MODEL er ikke installeret lokalt: "
                f"{ollama_model!r}. Bruger i stedet: {preferred!r}."
            )
            print("Installerede modeller:")
            for name in installed_models:
                print(f"- {name}")
            ollama_model = preferred

    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id
                FROM app_users
                WHERE display_name = %s
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (display_name,),
            )
            row = cur.fetchone()
            if not row:
                raise RuntimeError(
                    f"Fandt ingen user med display_name={display_name!r}. "
                    "Opret den i Neon eller ret APP_USER_DISPLAY_NAME."
                )
            user_id = row[0]

            cur.execute(
                """
                SELECT title
                FROM focus_items
                WHERE user_id = %s
                  AND focus_date = CURRENT_DATE
                ORDER BY slot ASC
                """,
                (user_id,),
            )
            focus_items = [r[0] for r in cur.fetchall()]

            cur.execute(
                """
                SELECT id, title, status, priority, due_date
                FROM tasks
                WHERE user_id = %s
                  AND status = 'todo'
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (user_id, todos_limit),
            )
            open_todos = cur.fetchall()

            cur.execute(
                """
                SELECT e.event_type,
                       e.entity_type,
                       e.entity_id,
                       e.occurred_at,
                       e.payload,
                       t.title AS task_title
                FROM events e
                LEFT JOIN tasks t
                  ON e.entity_type = 'task'
                 AND e.entity_id = t.id
                WHERE e.user_id = %s
                ORDER BY e.occurred_at DESC
                LIMIT %s
                """,
                (user_id, events_limit),
            )
            events = cur.fetchall()

            readable_events: list[str] = []
            for event_type, entity_type, entity_id, occurred_at, payload, task_title in events:
                label = None
                if entity_type == "task" and task_title:
                    if event_type == "TASK_CREATED":
                        label = f"Opgave oprettet: {task_title}"
                    elif event_type == "TASK_COMPLETED":
                        label = f"Opgave færdig: {task_title}"
                    elif event_type == "TASK_UPDATED":
                        label = f"Opgave opdateret: {task_title}"
                if event_type == "FOCUS_SET":
                    label = "Fokus sat"
                elif event_type == "CONTEXT_SWITCH":
                    label = "Konteksskift (sidespor)"
                elif event_type in {"SESSION_STARTED", "SESSION_ENDED"}:
                    label = event_type.replace("_", " ").lower()

                if not label:
                    label = f"{event_type}"

                readable_events.append(f"- {occurred_at:%Y-%m-%d %H:%M} | {label}")

            todo_lines: list[str] = []
            for _id, title, status, priority, due_date in open_todos:
                suffix_parts: list[str] = []
                if priority:
                    suffix_parts.append(f"prio={priority}")
                if due_date:
                    suffix_parts.append(f"due={due_date}")
                suffix = ""
                if suffix_parts:
                    suffix = " (" + ", ".join(suffix_parts) + ")"
                todo_lines.append(f"- {title}{suffix}")

            prompt = "\n".join(
                [
                    "Du er en strikt management-konsulent (på dansk).",
                    "Opgave: Hvis jeg kun har 1 time nu, lav en konkret plan.",
                    "Krav til output:",
                    "1) Start med en 1-linjers diagnose.",
                    "2) Giv en prioriteret plan med 3-7 punkter, hvert punkt med estimerede minutter.",
                    "3) Medtag 1 tydelig fravalgsliste (hvad jeg IKKE gør i denne time).",
                    "4) Slut med en 1-linjers 'første handling' jeg kan gøre NU.",
                    "",
                    "Dagens fokus (hvis tomt, foreslå 3 fokusområder):",
                    *(f"- {t}" for t in (focus_items or [])),
                    "",
                    "Mine åbne to-do's (seneste først):",
                    *(todo_lines or ["- (ingen åbne to-do's fundet)"]),
                    "",
                    "Seneste hændelser (oversat):",
                    *(readable_events or ["- (ingen events fundet)"]),
                ]
            )

            ollama_payload = {
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
            }

            resp = requests.post(
                f"{ollama_base_url}/api/generate",
                json=ollama_payload,
                timeout=120,
            )
            try:
                resp.raise_for_status()
            except requests.HTTPError as e:
                if resp.status_code == 404:
                    raise RuntimeError(
                        "Ollama returnerede 404. Det sker typisk når modellen ikke findes lokalt. "
                        f"Forsøgte model={ollama_model!r}. "
                        "Tjek OLLAMA_MODEL i .env eller pull en model via 'ollama pull <model>'. "
                        f"Installerede modeller: {installed_models}"
                    ) from e
                raise
            data = resp.json()
            output_text = data.get("response", "").strip()
            if not output_text:
                raise RuntimeError("Ollama svarede uden 'response'-tekst")

            event_payload = {
                "output_text": output_text,
                "meta": {
                    "model": ollama_model,
                    "ollama_base_url": ollama_base_url,
                    "events_limit": events_limit,
                    "todos_limit": todos_limit,
                },
                "input": {
                    "focus_items": focus_items,
                    "open_todos": [t[1] for t in open_todos],
                    "readable_events": readable_events,
                },
            }

            cur.execute(
                """
                INSERT INTO events (user_id, event_type, entity_type, entity_id, payload)
                VALUES (%s, 'LLM_PLAN_GENERATED', 'day', NULL, %s)
                """,
                (user_id, Json(event_payload)),
            )
            conn.commit()

    print(f"User: {display_name} ({user_id})")
    print("\n--- LLM PLAN ---\n")
    print(output_text)


if __name__ == "__main__":
    main()
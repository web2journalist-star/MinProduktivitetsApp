# MinProduktivitetsApp

## Status
Dette repo indeholder pt. flere prototype/demo-versioner (HTML/CSS/JS). Formålet er at samle dem til en produktklar app med en iterativ, feature-for-feature proces.

## Dagens arbejdsform (fast)
- Timebox pr. session: aftales (standard 60 min)
- Start: “Dagens opgave” (1 sætning)
- Undervejs: checkpoint “Er vi på rette vej?”
- Slut: “Nåede vi dagens opgave?”, “Hvor langt er vi (0–100%)?”, “Næste lille skridt”

## Arkitektur-retning (høj niveau)
- Lokal-first først (Eliza), multi-user senere
- Eget dataejerskab
- Audit/historik som first-class (event-log)
- LLM: rules/heuristics baseline, Ollama-first, cloud senere

## Mapper (planlagt)
- docs/: beslutninger, vision, roadmap, data model, API-kontrakt, rules
- todos/: roadmap/backlog + afsluttede opgaver
- db/: SQL schema + træningsqueries (Neon/Postgres)

## Prototype-filer (nuværende)
Se roden for HTML/CSS/JS demoer og mappen Tidligere/ for en ældre version.

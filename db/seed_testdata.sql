-- Seed testdata til MinProduktivitetsApp (Neon/Postgres)
-- Formål: give et lille, realistisk datasæt til LLM v0 (Daily Reflection & Next Nudge)
-- Kør i Neon SQL Editor efter `db/schema.sql`.

-- Find seneste Eliza-user (hvis du har flere) og brug den som owner for seed data
WITH u AS (
  SELECT id
  FROM app_users
  WHERE display_name = 'Eliza'
  ORDER BY created_at DESC
  LIMIT 1
),
seed_focus AS (
  INSERT INTO focus_items (user_id, focus_date, slot, title)
  SELECT u.id, CURRENT_DATE, f.slot, f.title
  FROM u
  CROSS JOIN (
    VALUES
      (1, 'Oprette denne app, lære at arbejde med SQL, lære at oprette min anden LLM model'),
      (2, 'Karriere-boblerne next step (FMbi): migrere webside + lave 1000 data i DB til LLM test'),
      (3, 'Evaluere og glæde mig over dagens work senest kl. 17')
  ) AS f(slot, title)
  ON CONFLICT (user_id, focus_date, slot)
  DO UPDATE SET title = EXCLUDED.title, updated_at = now()
  RETURNING id, slot
),
seed_tasks AS (
  INSERT INTO tasks (user_id, title, status, priority, due_date)
  SELECT u.id, t.title, t.status, t.priority, t.due_date
  FROM u
  CROSS JOIN (
    VALUES
      ('Oprette projektfundament i repo (docs/, todos/, db/)', 'done', 'høj', CURRENT_DATE),
      ('Køre db/schema.sql i Neon og oprette tabeller', 'done', 'høj', CURRENT_DATE),
      ('Oprette app_users (Eliza) via INSERT ... RETURNING', 'done', 'mellem', CURRENT_DATE),
      ('Oprette første task i Neon og verificere med SELECT', 'done', 'mellem', CURRENT_DATE),
      ('Oprette audit events i events-tabellen (TASK_CREATED) + verificere med SELECT', 'done', 'mellem', CURRENT_DATE),
      ('Planlægge LLM v0: Daily Reflection & Next Nudge (Ollama-first)', 'todo', 'mellem', CURRENT_DATE),
      ('Oprette seed testdata (focus + tasks + events) til LLM', 'todo', 'mellem', CURRENT_DATE),
      ('FMbi Karriere-boblerne: migrere webside (næste skridt)', 'todo', 'lav', CURRENT_DATE)
  ) AS t(title, status, priority, due_date)
  RETURNING id, title, status
),
log_task_events AS (
  INSERT INTO events (user_id, event_type, entity_type, entity_id, payload)
  SELECT
    u.id,
    CASE
      WHEN st.status = 'done' THEN 'TASK_COMPLETED'
      ELSE 'TASK_CREATED'
    END,
    'task',
    st.id,
    jsonb_build_object(
      'source', 'seed_testdata.sql',
      'title', st.title
    )
  FROM seed_tasks st
  CROSS JOIN u
  RETURNING id
),
log_focus_events AS (
  INSERT INTO events (user_id, event_type, entity_type, entity_id, payload)
  SELECT
    u.id,
    'FOCUS_SET',
    'focus_item',
    sf.id,
    jsonb_build_object(
      'source', 'seed_testdata.sql',
      'slot', sf.slot,
      'focus_date', CURRENT_DATE
    )
  FROM seed_focus sf
  CROSS JOIN u
  RETURNING id
)
INSERT INTO events (user_id, event_type, entity_type, entity_id, payload)
SELECT
  u.id,
  'CONTEXT_SWITCH',
  'day',
  NULL,
  jsonb_build_object(
    'source', 'seed_testdata.sql',
    'note', 'Sidespor: solgt 2 aktier, købt 2 aktier og overført penge fra bankkonto til Nordnet'
  )
FROM u
RETURNING id, occurred_at;

-- Efter seed: tjek data
-- SELECT slot, title FROM focus_items WHERE user_id=(SELECT id FROM app_users WHERE display_name='Eliza' ORDER BY created_at DESC LIMIT 1) AND focus_date=CURRENT_DATE ORDER BY slot;
-- SELECT title, status FROM tasks WHERE user_id=(SELECT id FROM app_users WHERE display_name='Eliza' ORDER BY created_at DESC LIMIT 1) ORDER BY created_at DESC;
-- SELECT event_type, entity_type, occurred_at, payload FROM events WHERE user_id=(SELECT id FROM app_users WHERE display_name='Eliza' ORDER BY created_at DESC LIMIT 1) ORDER BY occurred_at DESC LIMIT 50;

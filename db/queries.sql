-- Træningsqueries til Neon (kør dem manuelt og lær)

-- 0) Hvis gen_random_uuid() fejler, kør:
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1) Opret en lokal bruger (Eliza)
INSERT INTO app_users (display_name) VALUES ('Eliza') RETURNING id;

-- 2) Se brugere
SELECT * FROM app_users ORDER BY created_at DESC;

-- 3) Opret en task (erstat :user_id med id fra step 1)
-- INSERT INTO tasks (user_id, title, priority, due_date) VALUES (':user_id', 'Min første task', 'mellem', CURRENT_DATE);

-- 4) Hent tasks
SELECT id, title, status, priority, due_date, created_at
FROM tasks
ORDER BY created_at DESC;

-- 5) Log et event (audit)
-- INSERT INTO events (user_id, event_type, entity_type, entity_id, payload)
-- VALUES (':user_id', 'TASK_CREATED', 'task', ':task_id', '{"source":"neon_sql_editor"}');

-- 6) Seneste events
SELECT event_type, entity_type, entity_id, occurred_at, payload
FROM events
ORDER BY occurred_at DESC
LIMIT 20;

-- 7) Fokus trio for i dag (slots 1..3)
-- INSERT INTO focus_items (user_id, focus_date, slot, title)
-- VALUES
-- (':user_id', CURRENT_DATE, 1, 'Fokus 1'),
-- (':user_id', CURRENT_DATE, 2, 'Fokus 2'),
-- (':user_id', CURRENT_DATE, 3, 'Fokus 3');

-- 8) Hent fokus for i dag
-- SELECT slot, title FROM focus_items WHERE user_id=':user_id' AND focus_date=CURRENT_DATE ORDER BY slot;

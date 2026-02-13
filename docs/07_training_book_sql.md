# Træningsbog — SQL/DB (MinProduktivitetsApp)

## Formål
At du kan gentage øvelserne, se progression og vælge næste træningsmål uden at bruge mange tokens.

## Log (hvad vi har trænet)

### 2026-02-13
- Trænet: `CREATE TABLE` via `db/schema.sql` (Postgres/Neon)
- Trænet: `INSERT ... RETURNING` (oprettede `app_users`)
- Trænet: `SELECT ... ORDER BY ... LIMIT` (hentede tasks)
- Trænet: Audit-logik via `events` tabellen
- Trænet: `JSONB` payload i events
- Trænet (terminal): navigering til korrekt mappe med `cd`, tjek af placering med `pwd`
- Trænet (terminal): oprettelse af Python virtual environment med `python3 -m venv .venv` i `app/backend/`
- Trænet (sikkerhed): `.env` skal ignoreres i git (`.gitignore`), og DB password/credentials roteres ved eksponering
- Trænet (Neon): connection string i `.env` skal være ren `postgresql://...` URL (ikke `psql ...` wrapper)

## Gentagelsesopgaver (samme dag eller en anden dag)
1. Opret en ny task og log `TASK_CREATED` event.
2. Markér en task som done (via `UPDATE tasks SET status='done' ...`) og log `TASK_COMPLETED` event.
3. Indsæt fokus-trio for i dag og hent den igen.

## Terminal-cheatsheet (denne app)
- Stå i backend-mappen:
  - `cd /Users/elizabeths/Documents/MinProduktivitetsApp/app/backend`
  - `pwd` (skal ende på `/MinProduktivitetsApp/app/backend`)
- Opret venv:
  - `python3 -m venv .venv`
- Aktivér venv:
  - `source .venv/bin/activate`
- Deaktivér venv (gå ud af venv-miljøet):
  - `deactivate`
- Vigtigt: `.venv` er både en mappe og et miljø-navn i prompten
  - `cd .venv` betyder kun “gå ind i mappen”, ikke “aktiver venv”
  - `(.venv)` i prompten betyder at venv-miljøet er aktivt
- Installér dependencies:
  - `python -m pip install --upgrade pip`
  - `python -m pip install -r requirements.txt`

## Næste øvelser (når du er klar)
- `UPDATE` + `WHERE`
- `JOIN` (når vi har flere tabeller i brug)
- Aggregation: `COUNT`, `SUM`, `GROUP BY`
- Indekser: hvorfor og hvornår

## Noter / spørgsmål til næste session
- (skriv her)

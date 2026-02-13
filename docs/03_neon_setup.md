# Neon setup (SQL læring)

## Mål
- Du opretter et Neon-projekt
- Du kører `db/schema.sql` i Neon SQL Editor
- Du kører de første queries i `db/queries.sql`

## Trin
1. Opret Neon projekt + database
2. Åbn Neon -> SQL Editor
3. Kør først:
   - `CREATE EXTENSION IF NOT EXISTS pgcrypto;`
4. Kør hele `db/schema.sql`
5. Kør `db/queries.sql` stepvis (en blok ad gangen)

## Læringsfokus
- `CREATE TABLE`
- `PRIMARY KEY`, `REFERENCES`
- `INSERT ... RETURNING`
- `SELECT ... ORDER BY ... LIMIT`
- Hvorfor `events` (audit) er fundamentet for historik

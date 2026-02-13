# Data model (koncept)

## Entities (state)
- User (senere)
- Task
- FocusItem (Dagens Fokus Trio)
- Session (timer/pomodoro)
- Note
- Tada (sejr)

## Audit / Event log
Vi gemmer centrale ændringer som events, så vi kan:
- Se historik
- Genskabe state
- Analysere vaner/flow

Events er ikke “projekter”. Events er en generel audit-log over hvad der skete, hvornår, og på hvilken ting (entity) det skete.

Typiske event-typer i denne app:
- `TASK_CREATED`, `TASK_COMPLETED`
- `FOCUS_SET`
- `SESSION_STARTED`, `SESSION_ENDED`
- `CONTEXT_SWITCH` (sidespor)
- `LLM_PLAN_GENERATED` (LLM output gemmes som event, så vi kan se historik og forbedre prompts)

Event eksempel (koncept)
- event_type
- entity_type
- entity_id
- occurred_at
- payload (json)

`entity_type` og `entity_id`:
- `entity_type` beskriver hvilken type objekt eventet handler om (fx `task`, `focus_item`, `session`, `day`).
- `entity_id` er id’et på det konkrete objekt (UUID). Kan være `NULL`, hvis eventet handler om “dagen” eller en generel tilstand.

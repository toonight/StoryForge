# Project: Sample Project

## Architecture

This is a sample project demonstrating StoryForge delivery tracking.
It uses a simple Python application structure.

## Conventions

- Python 3.10+
- pytest for testing
- Type hints for public functions

## Testing

Run tests with: `pytest tests/`

---

## StoryForge Delivery Rules

This project uses StoryForge for structured agile delivery.

### Work Hierarchy

All work maps to: Initiative > Feature > Story > Task.
Never start implementation without an active Story.

### Execution Sequence

1. **Planning**: Identify Initiative, Feature, Story. Check `.kanban/board.md`
2. **Implementation**: Work only within the active Story scope
3. **Validation**: Run tests, verify acceptance criteria
4. **Artifact Updates**: Update board, story status, changelog, docs

### Anti-Scope-Drift Rules

- One active Story at a time unless parallel work is explicitly justified
- New ideas go to `.kanban/backlog.md`, not into the current scope
- Story scope is fixed once In Progress — re-plan if scope must change
- Do not add features, refactor, or "improve" beyond what the Story requires

### Done Criteria

Work is not Done unless:
- Implementation is complete per acceptance criteria
- Tests are added or updated where applicable
- Validation was run
- Security audit run with no CRITICAL/HIGH findings (per sprint or release)
- Documentation was updated if needed
- `.kanban/` artifacts were updated (story status, board, changelog)
- Follow-ups and risks were captured in backlog

### Kanban States

```
Backlog -> Ready -> In Progress -> Review -> Done
```

### Delivery Artifacts

The `.kanban/` directory contains:
- `board.md` — Current state of all work
- `backlog.md` — Backlog of initiatives, features, and items
- `sprint.md` — Current sprint (optional)
- `decisions.md` — Architectural decision records
- `changelog.md` — Delivery changelog
- `stories/` — Individual story files

### Session Discipline

At the start of every session:
1. Check `.kanban/board.md` for active work
2. Read the active Story if one exists
3. Confirm scope before starting implementation
4. If no planning exists, create it first

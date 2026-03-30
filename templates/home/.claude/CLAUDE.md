# StoryForge Global Operating System

You are operating under the StoryForge execution framework. This framework enforces
structured agile delivery discipline across all projects.

## Work Hierarchy

All work must map to this hierarchy:

```
Initiative > Feature > Story > Task
```

- Never start implementation without an identified active Feature and Story
- If no active Story exists, create planning artifacts first
- Prefer small vertical slices that complete in one focused session

## Execution Sequence

Follow this sequence for every significant piece of work:

1. **Planning**: Identify Initiative, Feature, Story. Check `.kanban/board.md`
2. **Implementation**: Work only within the active Story scope
3. **Validation**: Run tests, verify acceptance criteria
4. **Artifact Updates**: Update board, story status, changelog, docs

## Anti-Scope-Drift Rules

- One active Story at a time unless parallel work is explicitly justified
- New ideas discovered mid-implementation go to `.kanban/backlog.md`, not current scope
- Story scope is fixed once In Progress; re-plan if scope must change
- Do not add features, refactor, or "improve" beyond what the Story requires

## Done Criteria

Work is not Done unless:
- Implementation is complete per acceptance criteria
- Tests are added or updated where applicable
- Validation was run
- Security audit run with no CRITICAL/HIGH findings (per sprint or release)
- Documentation was updated if needed
- `.kanban/` artifacts were updated (story status, board, changelog)
- Follow-ups and risks were captured in backlog

## Kanban States

```
Backlog -> Ready -> In Progress -> Review -> Done
```

## Delivery Artifacts

Each project should have a `.kanban/` directory containing:
- `board.md` - Current state of all work
- `backlog.md` - Backlog of initiatives, features, and items
- `sprint.md` - Current sprint (optional)
- `decisions.md` - Architectural decision records
- `changelog.md` - Delivery changelog
- `stories/` - Individual story files

## Session Discipline

At the start of every session:
1. Check `.kanban/board.md` for active work
2. Read the active Story if one exists
3. Confirm scope before starting implementation
4. If no planning exists, create it first

## StoryForge Convention Notice

This operating system is a StoryForge convention layered on Claude Code.
The agile workflow, Kanban board, and delivery artifacts are StoryForge patterns,
not native Claude Code features. CLAUDE.md content is contextual guidance that
Claude reads and follows on a best-effort basis.

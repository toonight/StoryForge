# StoryForge Operating Model

## Work Hierarchy

All work in StoryForge-managed projects follows this hierarchy:

```
Initiative (strategic goal)
  +-> Feature (deliverable capability)
        +-> Story (vertical slice of user value)
              +-> Task (atomic implementation step)
```

### Initiative

- A strategic goal or theme spanning multiple features
- Example: "Establish StoryForge v1.0 as a production-grade framework"
- Tracked in `.kanban/backlog.md` at the initiative level

### Feature

- A deliverable capability that provides user value
- Must belong to an Initiative
- Example: "Global agent system with orchestrator and specialists"
- Tracked in `.kanban/board.md`

### Story

- A vertical slice of a Feature
- Must be small enough to complete in one focused session
- Has clear acceptance criteria
- Tracked in `.kanban/stories/STORY-NNN.md`

### Task

- An atomic implementation step within a Story
- Examples: "Create agent file", "Write test", "Update docs"
- Tracked within the Story file itself

## Kanban Board States

```
Backlog -> Ready -> In Progress -> Review -> Done
```

| State | Meaning | Entry Criteria | Exit Criteria |
|---|---|---|---|
| Backlog | Identified but not refined | Idea captured | Refined with acceptance criteria |
| Ready | Refined and ready to start | Acceptance criteria defined | Work begun |
| In Progress | Actively being worked on | Developer assigned | Implementation complete |
| Review | Implementation complete, needs review | Code done, tests pass | Review approved |
| Done | Fully complete | Review passed | All done criteria met |

## Done Criteria

Work cannot be marked Done unless ALL of the following are true:

1. Implementation is complete
2. Tests are added or updated where applicable
3. Validation was run (scripts, manual checks)
4. Security audit run with no CRITICAL or HIGH findings (per sprint or release)
5. Documentation was updated if needed
6. Kanban artifacts were updated (story status, board)
7. Follow-ups and risks were captured in backlog
8. Decision records were created for architectural choices

## Execution Sequence

Every significant piece of work follows this sequence:

### 1. Planning Phase

- Identify or create the relevant Initiative and Feature
- Write or refine the Story with acceptance criteria
- Define non-goals to prevent scope drift
- Move Story to "Ready" state

### 2. Implementation Phase

- Move Story to "In Progress"
- Work only on tasks within the active Story
- If new ideas emerge, add them to Backlog (not current scope)
- Keep changes small and focused

### 3. Validation Phase

- Run tests
- Run validation scripts
- Verify acceptance criteria are met
- Check for regressions

### 4. Artifact Update Phase

- Update Story status
- Update board.md
- Update changelog.md
- Record decisions in decisions.md if applicable
- Add follow-ups to backlog.md

## Anti-Scope-Drift Rules

These rules prevent work from expanding beyond the active Story:

1. **No implementation without an active Story**
   - If no Story exists for the requested work, create one first

2. **One active Story at a time** (default)
   - Parallel Stories require explicit justification

3. **New ideas go to Backlog**
   - Discoveries during implementation are captured as backlog items
   - They do not expand the current Story's scope

4. **Story scope is fixed once In Progress**
   - Acceptance criteria don't change mid-implementation
   - If scope must change, move Story back to Ready and re-plan

5. **Prefer small vertical slices**
   - A Story should be completable in one focused session
   - If it feels too large, split it

## Sprint Planning (Optional)

StoryForge supports optional sprint-based planning on top of Kanban:

- Sprint duration is configurable (default: 1 week)
- Sprint planning selects Stories from Ready state
- Sprint tracked in `.kanban/sprint.md`
- Sprint review captures what was done and what carries over

Sprints are optional. The Kanban board is always the primary tracking mechanism.

## Agent Operating Rules

### portfolio-orchestrator Behavior

When invoked, the portfolio-orchestrator must:

1. Read `.kanban/board.md` to find active work
2. Read active Story file to understand scope
3. If no active Story:
   - Ask user what they want to work on
   - Delegate to planner to create artifacts
4. If active Story exists:
   - Confirm scope with user
   - Delegate to implementer for bounded work
5. After work completes:
   - Delegate to reviewer for quality check
   - Delegate to doc-maintainer for artifact updates

### Specialist Behavior

Each specialist agent:
- Operates only within its defined scope
- Reports results back to the main conversation
- Does not modify artifacts outside its responsibility
- Follows the active Story's acceptance criteria

## Decision Records

Architectural and significant design decisions are recorded in `.kanban/decisions.md`
or `docs/decisions/` using this format:

```
## DECISION-NNN: Title

- Date: YYYY-MM-DD
- Status: Proposed | Accepted | Superseded
- Context: Why this decision was needed
- Decision: What was decided
- Consequences: What follows from this decision
- Alternatives considered: What else was evaluated
```

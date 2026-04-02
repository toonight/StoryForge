---
paths:
  - ".kanban/**/*"
---

# Kanban Artifact Rules

When editing files under .kanban/:

- Use sequential IDs: STORY-NNN, DECISION-NNN, INIT-NNN, FEAT-NNN
- Story status must be one of: Backlog, Ready, In Progress, Review, Done
- When changing a Story status, also update board.md
- When completing work, add an entry to changelog.md
- Do not modify acceptance criteria of In Progress stories (re-plan first)
- Follow-ups go to backlog.md under "Discovered During Implementation"
- Decision records use the DECISION-NNN format with Date, Status, Context,
  Decision, Consequences, and Alternatives fields
- Every Feature must have a file in features/FEAT-NNN.md
- Every Story must reference an existing Feature in its metadata
- Every STORY-NNN referenced in board.md must have a file in stories/
- When creating a new Feature, use FEAT-TEMPLATE.md as the base

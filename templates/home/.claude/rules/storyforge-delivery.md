---
paths:
  - ".kanban/**/*"
---

# StoryForge Delivery Rules (Global)

These rules apply when working with .kanban/ artifacts in any project:

- All work maps to Initiative > Feature > Story > Task
- No implementation starts without an active Story in "In Progress" state
- New ideas discovered during implementation go to backlog, not current scope
- Story scope is fixed once In Progress
- Work is not Done until: implementation complete, tests pass, artifacts updated
- One active Story at a time unless parallel work is explicitly justified

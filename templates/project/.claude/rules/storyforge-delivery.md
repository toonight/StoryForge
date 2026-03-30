---
paths:
  - ".kanban/**/*"
---

# StoryForge Delivery Rules

These rules apply when working with .kanban/ artifacts:

- All work maps to Initiative > Feature > Story > Task
- No implementation starts without an active Story in "In Progress" state
- New ideas discovered during implementation go to backlog, not current scope
- Story scope is fixed once In Progress
- Work is not Done until: implementation complete, tests pass, artifacts updated
- One active Story at a time unless parallel work is explicitly justified
- Security audit must run before sprint closure (no CRITICAL/HIGH findings)

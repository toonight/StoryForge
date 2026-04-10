---
name: sprint-groom
description: Plan or review a sprint by selecting Stories from Ready state into the sprint backlog. Use for sprint planning or mid-sprint reviews.
disable-model-invocation: true
paths:
  - ".kanban/sprint.md"
---

# Sprint Grooming

Plan or review the current sprint by managing the sprint backlog.

## Instructions

### For Sprint Planning

1. Read `.kanban/board.md` to see all Features and Stories
2. Read `.kanban/backlog.md` to see available work
3. Identify Stories in "Ready" state
4. Present the Ready stories to the user with their acceptance criteria summaries
5. Ask the user which Stories to include in the sprint
6. Update `.kanban/sprint.md` with:
   - Sprint name and number
   - Start date (today)
   - Sprint goal
   - Selected Stories in the Sprint Backlog table
7. Confirm the sprint plan

### For Mid-Sprint Review

1. Read `.kanban/sprint.md` to see current sprint
2. Read each Story in the sprint to check status
3. Report:
   - Stories completed (Done)
   - Stories in progress
   - Stories not started
   - Any blockers or risks
4. Ask if any adjustments are needed:
   - Add Stories from backlog
   - Remove Stories that won't fit
   - Re-prioritize remaining work

### Sprint Completion

When a sprint is complete:
1. List all completed Stories
2. List any Stories that carry over
3. Capture lessons learned
4. Archive the sprint data in sprint.md (keep history)
5. **Run security audit** before closing the sprint:
   ```bash
   python scripts/security_audit.py . --report
   ```
   If CRITICAL or HIGH findings exist, flag them before sprint closure.
   Create Stories for any findings that need remediation.
6. Suggest starting a new sprint planning session

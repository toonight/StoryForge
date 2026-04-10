---
name: doc-update
description: Update StoryForge delivery artifacts after work is completed. Updates story status, board, changelog, and captures follow-ups. Use after completing implementation work.
disable-model-invocation: true
paths:
  - ".kanban/stories/*.md"
---

# Documentation Update

Update StoryForge delivery artifacts after work is completed.

## Instructions

1. Ask the user (or determine from context):
   - Which Story was completed or updated?
   - What was the new status? (Ready, In Progress, Review, Done)
   - What was accomplished?
   - Any follow-ups or discoveries?
   - Any decisions that need recording?

2. Update the Story file in `.kanban/stories/`:
   - Change the Status field
   - Check off completed acceptance criteria
   - Add implementation notes if relevant
   - Add validation notes if tests were run
   - Add follow-ups if discovered

3. Update `.kanban/board.md`:
   - Move the Story to the correct column
   - Update any Feature statuses if all Stories are Done

4. Update `.kanban/changelog.md`:
   - Add today's date header if not present
   - Add a bullet point describing what was done

5. If follow-ups were discovered:
   - Add them to `.kanban/backlog.md` under "Discovered During Implementation"
   - Include enough context to be actionable later

6. If an architectural decision was made:
   - Add a decision record to `.kanban/decisions.md`
   - Use the next sequential DECISION-NNN number

7. Confirm all updates were made and summarize what changed

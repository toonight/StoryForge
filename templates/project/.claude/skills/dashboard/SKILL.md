---
name: dashboard
description: Display the StoryForge Kanban dashboard showing board status, features, active stories, sprint progress, and recent activity. Use to get a quick overview of project delivery state.
disable-model-invocation: true
paths:
  - ".kanban/board.md"
---

# StoryForge Dashboard

Display the Kanban dashboard for the current project.

## Instructions

Run the StoryForge dashboard script to display the current project delivery state:

```bash
python scripts/dashboard.py .
```

If the dashboard script is not available locally, read the .kanban/ files directly
and present a summary:

1. Read `.kanban/board.md` - show story counts per column
2. Read active stories from `.kanban/stories/` - show progress on acceptance criteria
3. Read `.kanban/sprint.md` - show sprint burndown
4. Read `.kanban/changelog.md` - show last 5 entries

Present the information in a clear, structured format.

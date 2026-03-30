---
name: gh-link
description: Link a StoryForge story to a GitHub Issue or Pull Request. Updates the story's GitHub field and optionally adds a comment on the GitHub issue. Use when starting work that relates to a GitHub issue.
argument-hint: "STORY-NNN #issue-or-pr"
disable-model-invocation: true
---

# GitHub Link

Link a StoryForge story to a GitHub Issue or Pull Request.

## Instructions

Parse the arguments: `$ARGUMENTS`

Expected format: `STORY-NNN #issue` or `STORY-NNN PR #pr`

### Step 1: Validate

1. Find the story file at `.kanban/stories/$ARGUMENTS[0].md`
2. If it doesn't exist, list available stories and ask the user

### Step 2: Update Story

Edit the story file's `**GitHub**` field:
- For issues: `#123`
- For PRs: `PR #456`
- For both: `#123, PR #456`

### Step 3: Add GitHub Comment (optional)

If the `gh` CLI is available, add a comment on the GitHub issue:

```bash
gh issue comment $1 --body "Linked to StoryForge $ARGUMENTS[0]

**Status**: (current status)
**Feature**: (feature name)
**Acceptance Criteria**: N items"
```

### Step 4: Confirm

Report what was linked and suggest next steps.

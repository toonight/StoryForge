---
name: kanban-bootstrap
description: Initialize a project with StoryForge Kanban delivery structure. Creates .kanban/ directory with board, backlog, sprint, decisions, changelog, and stories directory. Use when setting up a new project for StoryForge delivery tracking.
argument-hint: "project-name"
disable-model-invocation: true
---

# Kanban Bootstrap

Initialize a StoryForge Kanban delivery structure for the current project.

## Instructions

Create the following directory structure and files in the current project:

### Directory: `.kanban/`

### File: `.kanban/board.md`

```markdown
# $ARGUMENTS Kanban Board

## Initiative: INIT-001 - (Define the primary initiative)

### Backlog

(No items yet)

### Ready

(No items yet)

### In Progress

(No items yet)

### Review

(No items yet)

### Done

(No items yet)

---

## Features

| ID | Title | Initiative | Status |
|---|---|---|---|
```

### File: `.kanban/backlog.md`

```markdown
# $ARGUMENTS Backlog

## Initiatives

### INIT-001: (Define the primary initiative)
- Status: Backlog
- Goal: (Define the strategic goal)

---

## Backlog Items

(No items yet)

---

## Discovered During Implementation

(Items added here during work on other stories)
```

### File: `.kanban/sprint.md`

```markdown
# $ARGUMENTS Sprint

## Current Sprint: (Not yet planned)

- Start: (TBD)
- Goal: (TBD)

### Sprint Backlog

| ID | Title | Status |
|---|---|---|

### Sprint Notes

(No notes yet)
```

### File: `.kanban/decisions.md`

```markdown
# $ARGUMENTS Decision Records

(No decisions recorded yet. Use this format:)

## DECISION-NNN: Title

- Date: YYYY-MM-DD
- Status: Proposed | Accepted | Superseded
- Context: Why this decision was needed
- Decision: What was decided
- Consequences: What follows from this decision
- Alternatives considered: What else was evaluated
```

### File: `.kanban/changelog.md`

```markdown
# $ARGUMENTS Delivery Changelog

## (Today's date)

- Initialized StoryForge Kanban structure
```

### Directory: `.kanban/stories/`

Create this empty directory (with a `.gitkeep` file if needed).

## After Creation

1. Inform the user that the Kanban structure is ready
2. Ask them to define their first Initiative
3. Suggest creating their first Feature and Story using the `story-write` skill

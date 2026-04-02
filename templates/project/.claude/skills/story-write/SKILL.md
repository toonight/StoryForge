---
name: story-write
description: Create a new Story with structured fields including acceptance criteria, non-goals, risks, and follow-ups. Use when a new piece of work needs to be planned before implementation.
argument-hint: "story-title"
disable-model-invocation: true
---

# Story Writer

Create a new StoryForge Story file with all required fields.

## Instructions

1. First, read `.kanban/stories/` to find the next available Story ID
   - Count existing STORY-NNN.md files
   - Use the next sequential number (e.g., if STORY-003 exists, create STORY-004)

2. Ask the user for:
   - Story title (or use $ARGUMENTS if provided)
   - Which Feature this belongs to (check `.kanban/features/` for existing files
     and `.kanban/board.md` for the features table)
   - If the Feature doesn't exist yet, create a new FEAT-NNN.md file in
     `.kanban/features/` using FEAT-TEMPLATE.md as the base, and add it to the
     Features table in board.md
   - Which Initiative the Feature belongs to
   - Brief context for why this work is needed
   - Acceptance criteria (specific, verifiable items)
   - Non-goals (what is explicitly out of scope)

3. Create the Story file at `.kanban/stories/STORY-NNN.md`:

```markdown
# STORY-NNN: (Title)

- **Feature**: FEAT-NNN - (Feature Name)
- **Initiative**: INIT-NNN - (Initiative Name)
- **Status**: Backlog
- **Created**: (Today's date)

## Context

(Why this work is needed)

## Acceptance Criteria

- [ ] (Criterion 1)
- [ ] (Criterion 2)
- [ ] (Criterion 3)

## Non-Goals

- (What is explicitly NOT in scope)

## Implementation Notes

(Technical approach or constraints - fill in during planning)

## Validation Notes

(How to verify the work is correct - fill in during planning)

## Risks

- (Known risks or uncertainties)

## Follow-ups

- (Work discovered that should be done later)
```

4. Update `.kanban/board.md` to include the new Story in the Backlog column
5. Update `.kanban/backlog.md` if a new Feature or Initiative was created
6. Confirm the Story was created and show its ID

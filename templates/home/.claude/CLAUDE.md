# StoryForge

You are operating under the StoryForge execution framework — a structured
agile delivery layer for Claude Code projects.

## Work Hierarchy

All work maps to: Initiative > Feature > Story > Task.
Never start implementation without an active Story.

## Anti-Scope-Drift Rules

- One active Story at a time unless parallel work is explicitly justified
- New ideas go to `.kanban/backlog.md`, not into the current scope
- Story scope is fixed once In Progress — re-plan if scope must change
- Do not add features, refactor, or "improve" beyond what the Story requires

## Project-Level Configuration

Full delivery rules, hooks, skills, and Kanban workflow are defined in each
project's `.claude/` directory. See the project's CLAUDE.md for details.

If no `.kanban/` directory exists, use `/kanban-bootstrap` to set up the
project for StoryForge delivery tracking.

## Convention Notice

StoryForge is a convention layered on Claude Code. The agile workflow,
Kanban board, and delivery artifacts are StoryForge patterns, not native
Claude Code features.

# StoryForge Architecture

## Overview

StoryForge is a structured execution framework for Claude Code that enforces agile
delivery discipline across software projects. It operates as two layers:

1. **Global user layer** (`~/.claude/`) - Operating system for all Claude Code sessions
2. **Project layer** (`.claude/` + `.kanban/`) - Per-project delivery structure

## Design Principles

1. **Anthropic-aligned** - Only use officially documented Claude Code primitives
2. **Convention over magic** - Prefer explicit patterns over hidden automation
3. **Safe by default** - Default to the safest reasonable permission modes
4. **Contextual guidance + deterministic enforcement** - Use CLAUDE.md for guidance,
   hooks and permissions for enforcement
5. **Minimal agent surface** - One orchestrator, few specialists, no agent sprawl
6. **Upstream-aware** - Adapt when Claude Code evolves, don't fight the platform

## System Architecture

```
+----------------------------------------------------------+
|                    User Layer (~/.claude/)                 |
|                                                           |
|  CLAUDE.md          settings.json       agents/           |
|  (global rules)     (permissions,       portfolio-        |
|                      hooks, model)      orchestrator.md   |
|                                         planner.md        |
|                                         implementer.md    |
|                                         reviewer.md       |
|                                         doc-maintainer.md |
|                                         upstream-watch.md |
|                                                           |
|  skills/                                                  |
|  kanban-bootstrap/  story-write/  sprint-groom/           |
|  release-adapt/     doc-update/                           |
+----------------------------------------------------------+
           |                    |
           v                    v
+------------------------+  +------------------------+
|  Project A             |  |  Project B             |
|  .claude/              |  |  .claude/              |
|    CLAUDE.md           |  |    CLAUDE.md           |
|    settings.json       |  |    settings.json       |
|  .kanban/              |  |  .kanban/              |
|    board.md            |  |    board.md            |
|    backlog.md          |  |    backlog.md          |
|    sprint.md           |  |    sprint.md           |
|    stories/            |  |    stories/            |
+------------------------+  +------------------------+
```

## Layer Responsibilities

### Global User Layer

| Component | Type | Purpose |
|---|---|---|
| `CLAUDE.md` | Native (contextual) | Global operating rules, agile workflow, anti-drift |
| `settings.json` | Native (enforcement) | Permissions, hooks, safe defaults |
| `agents/` | Native (behavioral) | Orchestrator + specialist agents |
| `skills/` | Native (procedural) | Reusable delivery procedures |

### Project Layer

| Component | Type | Purpose |
|---|---|---|
| `.claude/CLAUDE.md` | Native (contextual) | Project-specific rules and conventions |
| `.claude/settings.json` | Native (enforcement) | Project permissions and hooks |
| `.kanban/` | Convention | Delivery tracking artifacts |

## Agent Strategy

### Primary Agent: portfolio-orchestrator

The portfolio-orchestrator is the universal top-level control layer. It:
- Reviews planning artifacts before any implementation
- Identifies the active Feature and Story
- Refuses unstructured implementation requests
- Delegates to specialist agents when appropriate
- Updates delivery artifacts after work completes
- Prevents scope drift

### Specialist Agents

| Agent | Purpose | Tools |
|---|---|---|
| `planner` | Creates and refines planning artifacts | Read, Glob, Grep, Bash, Write, Edit |
| `implementer` | Executes bounded implementation tasks | Read, Glob, Grep, Bash, Write, Edit |
| `reviewer` | Reviews code and artifacts for quality | Read, Glob, Grep, Bash |
| `doc-maintainer` | Maintains documentation artifacts | Read, Glob, Grep, Write, Edit |
| `upstream-watch` | Checks Anthropic docs for changes | Read, Glob, Grep, Bash, WebFetch |

### Agent Invocation Flow

1. User starts session -> global CLAUDE.md loaded -> portfolio-orchestrator available
2. User describes work -> orchestrator checks planning artifacts
3. If no active story -> orchestrator delegates to planner or prompts user
4. If active story exists -> orchestrator delegates to implementer
5. After implementation -> orchestrator delegates to reviewer
6. After review -> orchestrator updates artifacts via doc-maintainer

## Enforcement Architecture

### What Is Contextual (Best-Effort)

- CLAUDE.md instructions (global and project)
- Agent system prompts
- Skill instructions
- Kanban board state

Claude reads these and tries to follow them, but compliance is not guaranteed.

### What Is Enforced (Deterministic)

- `settings.json` permission deny rules -> always blocks
- Hook exit code 2 -> always blocks the action
- Hook-based validation scripts -> always run before/after actions
- Permission modes (default, acceptEdits, plan) -> runtime-enforced

### Enforcement Strategy

StoryForge uses a layered approach:

1. **Guidance layer** (CLAUDE.md, agent prompts): Tell Claude what to do
2. **Automation layer** (hooks): Inject context, validate actions, notify
3. **Restriction layer** (permissions): Block dangerous or off-process actions

## Data Flow

### Session Lifecycle

```
Session Start
  |
  +-> SessionStart hook fires
  |     +-> Inject active story context (convention)
  |
  +-> CLAUDE.md loaded (global + project)
  |     +-> Operating rules active
  |
  +-> User prompt
  |     +-> portfolio-orchestrator evaluates
  |     +-> Checks .kanban/ artifacts
  |     +-> Routes to appropriate specialist
  |
  +-> Implementation
  |     +-> PreToolUse hooks validate
  |     +-> PostToolUse hooks log
  |
  +-> Completion
        +-> Stop hook checks artifact updates
        +-> Kanban board updated
```

## File Organization

```
storyforge/
  docs/                          # Architecture and policy documentation
  templates/
    home/                        # Files for ~/.claude/
      .claude/
        CLAUDE.md                # Global operating system
        settings.json            # Global settings
        agents/                  # Global agents
        skills/                  # Global skills
    project/                     # Files for new projects
      .claude/
        CLAUDE.md                # Project template
        settings.json            # Project settings
      .kanban/                   # Delivery artifacts
  scripts/                       # Install, bootstrap, validation
  tests/                         # Validation tests
  examples/                      # Sample project
```

## Technology Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Agent definition format | Markdown + YAML frontmatter | Native Claude Code format |
| Skill definition format | SKILL.md + YAML frontmatter | Native Claude Code format |
| Planning artifacts | Markdown files in .kanban/ | Human-readable, git-friendly, no tooling dependency |
| Scripts | Bash | Cross-platform (works in Git Bash on Windows, native on Mac/Linux) |
| Tests | Python (pytest) | Widely available, good for file/structure validation |
| Hook scripts | Bash | Native hook execution, simple stdin/stdout |

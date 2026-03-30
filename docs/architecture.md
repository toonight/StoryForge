# StoryForge Architecture

## Overview

StoryForge is a structured execution framework for Claude Code that enforces agile
delivery discipline across software projects. It operates as three layers:

1. **Global security layer** (`~/.claude/`) - Thin: identity, agents, security, global skills
2. **Project delivery layer** (`.claude/`) - Rich: delivery rules, hooks, project skills, rules
3. **Local overrides** - Developer-specific settings (not committed)

## Design Principles

1. **Anthropic-aligned** - Only use officially documented Claude Code primitives
2. **Convention over magic** - Prefer explicit patterns over hidden automation
3. **Safe by default** - Default to the safest reasonable permission modes
4. **Contextual guidance + deterministic enforcement** - Use CLAUDE.md for guidance,
   hooks and permissions for enforcement
5. **Minimal agent surface** - One orchestrator, few specialists, no agent sprawl
6. **Upstream-aware** - Adapt when Claude Code evolves, don't fight the platform
7. **Thin global, rich project** - Security is global; delivery discipline is per-project

## System Architecture

```
+----------------------------------------------------------+
|              Global Security Layer (~/.claude/)            |
|                        (THIN)                             |
|                                                           |
|  CLAUDE.md            settings.json        agents/        |
|  (~27 lines:          (deny rules:         8 universal    |
|   identity,            .env, .ssh, .aws,   agents         |
|   anti-drift,          gcloud, azure,                     |
|   project pointer)     kube, docker,       skills/        |
|                        npmrc, git-creds;   4 global:      |
|                        PreToolUse:         kanban-bootstrap|
|                        blocks rm -rf /,    release-adapt   |
|                        force push,         security-audit  |
|                        hard reset,         upstream-check  |
|                        chmod 777,                         |
|                        pipe to bash)                      |
+----------------------------------------------------------+
           |                    |
           v                    v
+------------------------+  +------------------------+
|  Project A  (RICH)     |  |  Project B  (RICH)     |
|  .claude/              |  |  .claude/              |
|    CLAUDE.md           |  |    CLAUDE.md           |
|    (full delivery      |  |    (full delivery      |
|     rules, session     |  |     rules, session     |
|     discipline)        |  |     discipline)        |
|    settings.json       |  |    settings.json       |
|    (all hooks:         |  |    (all hooks +        |
|     SessionStart,      |  |     deny rules)        |
|     PostToolUse,       |  |                        |
|     Stop, Notification |  |    rules/              |
|     + PreToolUse       |  |    skills/             |
|     + deny rules)      |  |                        |
|    rules/              |  |  .kanban/              |
|      kanban.md         |  |    board.md            |
|      storyforge-       |  |    backlog.md          |
|      delivery.md       |  |    sprint.md           |
|    skills/             |  |    stories/            |
|      story-write/      |  +------------------------+
|      dashboard/        |
|      sprint-groom/     |
|      doc-update/       |         +------------------+
|      gh-link/          |         |  Local Overrides |
|  .kanban/              |         |  (~/.claude/     |
|    board.md            |         |   local config)  |
|    backlog.md          |         |  Developer-      |
|    sprint.md           |         |  specific, not   |
|    stories/            |         |  committed       |
+------------------------+         +------------------+
```

## Layer Responsibilities

### Layer 1: Global Security (`~/.claude/`)

The global layer is intentionally thin. It provides identity, security enforcement,
and universal agents. It does NOT contain delivery hooks or delivery rules.

| Component | Type | Purpose |
|---|---|---|
| `CLAUDE.md` | Native (contextual) | Identity (~27 lines), anti-drift reminder, project pointer |
| `settings.json` | Native (enforcement) | Cloud credential deny rules, PreToolUse guardrails |
| `agents/` | Native (behavioral) | 8 universal agents (orchestrator + specialists) |
| `skills/` | Native (procedural) | 4 global skills (bootstrap, release, security, upstream) |

### Layer 2: Project Delivery (`.claude/`)

The project layer is rich. It carries all delivery rules, hooks, project-specific
skills, and rules files. This is installed by `bootstrap_project.sh`.

| Component | Type | Purpose |
|---|---|---|
| `.claude/CLAUDE.md` | Native (contextual) | Full delivery rules: execution sequence, Kanban states, done criteria, session discipline |
| `.claude/settings.json` | Native (enforcement) | All hooks (SessionStart, PostToolUse, Stop, Notification) + PreToolUse safety + env deny |
| `.claude/rules/` | Native (contextual) | `kanban.md` (artifact format), `storyforge-delivery.md` (discipline) |
| `.claude/skills/` | Native (procedural) | 5 project skills: story-write, dashboard, sprint-groom, doc-update, gh-link |
| `.kanban/` | Convention | Delivery tracking artifacts |

### Layer 3: Local Overrides

Developer-specific settings that are not committed. These can override project
settings for individual workflows.

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
| `security-auditor` | Post-sprint security review (read-only) | Read, Glob, Grep, Bash |
| `upstream-watch` | Manual Anthropic doc checks | Read, Glob, Grep, Bash, WebFetch |
| `upstream-monitor` | Automated daily monitoring | Read, Glob, Grep, Bash |

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
- Rules files
- Kanban board state

Claude reads these and tries to follow them, but compliance is not guaranteed.

### What Is Enforced (Deterministic)

- `settings.json` permission deny rules -> always blocks
- Hook exit code 2 -> always blocks the action
- Hook-based validation scripts -> always run before/after actions
- Permission modes (default, acceptEdits, plan) -> runtime-enforced

### Enforcement Strategy

StoryForge uses a layered approach:

1. **Security layer** (global settings.json): Deny rules for credentials, PreToolUse guardrails
2. **Delivery layer** (project settings.json): Session hooks, PostToolUse reminders, Stop checks
3. **Guidance layer** (CLAUDE.md, agent prompts, rules/): Tell Claude what to do
4. **Restriction layer** (permissions): Block dangerous or off-process actions

## Data Flow

### Session Lifecycle

```
Session Start
  |
  +-> Global CLAUDE.md loaded (identity, anti-drift)
  |
  +-> Project .claude/CLAUDE.md loaded (delivery rules)
  |
  +-> Project SessionStart hook fires
  |     +-> Inject active story context (convention)
  |
  +-> User prompt
  |     +-> portfolio-orchestrator evaluates
  |     +-> Checks .kanban/ artifacts
  |     +-> Routes to appropriate specialist
  |
  +-> Implementation
  |     +-> PreToolUse hooks validate (global + project)
  |     +-> PostToolUse hooks log (project)
  |
  +-> Completion
        +-> Stop hook checks artifact updates (project)
        +-> Kanban board updated
```

## Security Architecture

### Credential Protection (Global)

The global `settings.json` blocks access to sensitive files:

| Category | Paths blocked |
|---|---|
| Environment files | `.env`, `.env.*` |
| SSH keys | `~/.ssh/**` |
| Cloud credentials | `~/.aws/**`, `~/.config/gcloud/**`, `~/.azure/**` |
| Container/orchestration | `~/.kube/**`, `~/.docker/**` |
| Package/VCS credentials | `~/.npmrc`, `~/.git-credentials` |

### Command Guardrails (Global + Project)

PreToolUse hooks on Bash commands block:

| Pattern | Risk |
|---|---|
| `rm -rf /` | System destruction |
| `git push --force` / `git push -f` | History rewrite |
| `git reset --hard` | Data loss |
| `chmod 777` | Insecure permissions |
| `\| bash` / `\|bash` | Arbitrary code execution |

### Security Audit

The `/security-audit` skill and `security_audit.py` script scan `.claude/` and
`.kanban/` directories in addition to project code, detecting:
- Secrets and credentials in files
- Injection patterns
- Weak crypto usage
- Dangerous file permissions
- Unsafe StoryForge configuration

## File Organization

```
storyforge/
  docs/                          # Architecture and policy documentation
  templates/
    home/                        # Global layer (~/.claude/) — thin
      .claude/
        CLAUDE.md                # Identity + anti-drift (~27 lines)
        settings.json            # Security deny rules + PreToolUse guardrails
        agents/                  # 8 universal agents
        skills/                  # 4 global skills
    project/                     # Project layer — rich
      .claude/
        CLAUDE.md                # Full delivery rules
        settings.json            # All hooks + deny rules
        rules/                   # kanban.md, storyforge-delivery.md
        skills/                  # 5 project skills
      .kanban/                   # Delivery artifacts
  scripts/                       # Install, bootstrap, validation
  tests/                         # Validation tests
  examples/                      # Sample project
```

## Technology Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Architecture model | Thin global, rich project | Security is universal; delivery discipline varies per project |
| Agent definition format | Markdown + YAML frontmatter | Native Claude Code format |
| Skill definition format | SKILL.md + YAML frontmatter | Native Claude Code format |
| Planning artifacts | Markdown files in .kanban/ | Human-readable, git-friendly, no tooling dependency |
| Scripts | Bash + PowerShell | Cross-platform (Bash for Mac/Linux/Git Bash, PowerShell for Windows) |
| Tests | Python (pytest) | Widely available, good for file/structure validation |
| Hook scripts | Bash | Native hook execution, simple stdin/stdout |

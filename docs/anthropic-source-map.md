# Anthropic Source Map

This document maps every StoryForge capability to the official Anthropic documentation
that justifies or informs its design.

Last audited: 2026-04-10

## Capability Classification

Each StoryForge capability is classified as one of:

| Classification | Meaning |
|---|---|
| **Native** | Directly supported by Claude Code as documented by Anthropic |
| **Convention** | A StoryForge-defined pattern layered on top of native capabilities |
| **Enforcement** | Uses native enforcement mechanisms (settings, hooks, permissions) to guarantee behavior |

---

## Global CLAUDE.md (User-Level)

| Capability | Classification | Anthropic Source |
|---|---|---|
| `~/.claude/CLAUDE.md` as user-level instructions | Native | CLAUDE.md docs: user instructions scope |
| Content loaded as contextual guidance (not enforced) | Native | CLAUDE.md docs: "advisory context, not enforced policy" |
| Merge order: user < project < managed | Native | CLAUDE.md docs: loading/merge order |
| Recommended < 200 lines for adherence | Native | CLAUDE.md docs: size limits |
| Agile workflow rules in CLAUDE.md | Convention | StoryForge convention, not an Anthropic native feature |
| Anti-scope-drift rules in CLAUDE.md | Convention | StoryForge convention, not an Anthropic native feature |
| Delivery artifact requirements in CLAUDE.md | Convention | StoryForge convention, not an Anthropic native feature |

## Project CLAUDE.md

| Capability | Classification | Anthropic Source |
|---|---|---|
| `.claude/CLAUDE.md` for project-level instructions | Native | CLAUDE.md docs: project instructions scope |
| `.claude/rules/` for organized path-specific rules | Native | CLAUDE.md docs: frontmatter with paths field |
| `@path/to/import` for file imports | Native | CLAUDE.md docs: import syntax |
| Project architecture rules in CLAUDE.md | Convention | StoryForge convention |

## Settings.json

| Capability | Classification | Anthropic Source |
|---|---|---|
| `~/.claude/settings.json` for user-level settings | Native | Settings docs: user-level scope |
| `.claude/settings.json` for project-level settings | Native | Settings docs: project-level scope |
| `.claude/settings.local.json` for local overrides | Native | Settings docs: local settings scope |
| `permissions.allow` / `permissions.deny` rules | Native | Settings docs: permission configuration |
| `permissions.ask` rules for confirmation prompts | Native | Settings docs: permission configuration |
| `permissions.additionalDirectories` for extra working dirs | Native | Settings docs: permission configuration |
| `env` for environment variables | Native | Settings docs: env field |
| `model` for default model override | Native | Settings docs: model field |
| `hooks` configuration in settings.json | Native | Hooks docs: hook configuration format |
| `agent` for default session agent | Native | Settings docs: agent field |
| `claudeMdExcludes` to skip CLAUDE.md files by glob | Native | Settings docs: claudeMdExcludes field |
| `autoMemoryEnabled` to disable auto memory per project | Native | Settings docs: autoMemoryEnabled field |
| `autoMemoryDirectory` to customize memory location | Native | Settings docs: autoMemoryDirectory field |
| `disableAllHooks` to disable all hooks | Native | Settings docs: disableAllHooks field |
| `disableSkillShellExecution` to disable skill shell injection | Native | Settings docs: disableSkillShellExecution field |
| `attribution` for custom git commit/PR attribution | Native | Settings docs: attribution field |
| `language` for response language preference | Native | Settings docs: language field |
| `outputStyle` for output style configuration | Native | Settings docs: outputStyle field |
| `plansDirectory` for custom plan file storage | Native | Settings docs: plansDirectory field |
| `autoMode` for auto mode classifier configuration | Native | Settings docs: autoMode field |
| `worktree.symlinkDirectories` for worktree symlinks | Native | Settings docs: worktree settings |
| `worktree.sparsePaths` for worktree sparse checkout | Native | Settings docs: worktree settings |
| Safe default permission mode (default/acceptEdits) | Convention | StoryForge convention: prefer safety |

## Subagents

| Capability | Classification | Anthropic Source |
|---|---|---|
| `~/.claude/agents/*.md` for user-level agents | Native | Subagents docs: user-level storage |
| `.claude/agents/*.md` for project-level agents | Native | Subagents docs: project-level storage |
| YAML frontmatter (name, description, tools, model, etc.) | Native | Subagents docs: supported frontmatter fields |
| `tools` field to restrict agent tool access | Native | Subagents docs: tool allowlist |
| `disallowedTools` field to deny specific tools | Native | Subagents docs: tool denylist |
| `model` field for agent-specific model | Native | Subagents docs: model field |
| `permissionMode` for agent permission override | Native | Subagents docs: permission modes |
| `maxTurns` for agent turn limits | Native | Subagents docs: maxTurns field |
| `skills` for preloading skills into agent | Native | Subagents docs: skills field |
| `hooks` scoped to agent lifecycle | Native | Subagents docs: hooks in frontmatter |
| `memory` field (scope: user, project, local) | Native | Subagents docs: memory field |
| `background` for background task execution | Native | Subagents docs: background field |
| `effort` for effort level override | Native | Subagents docs: effort field |
| `isolation` (worktree) for isolated execution | Native | Subagents docs: isolation field |
| `color` for UI display color | Native | Subagents docs: color field |
| `initialPrompt` for auto-submitted first turn | Native | Subagents docs: initialPrompt field |
| `mcpServers` scoped to a subagent | Native | Subagents docs: mcpServers field |
| Automatic delegation based on description | Native | Subagents docs: automatic delegation |
| Subagents cannot spawn other subagents | Native | Subagents docs: no nested subagents |
| portfolio-orchestrator as primary orchestrator | Convention | StoryForge convention |
| Specialist agents (planner, implementer, etc.) | Convention | StoryForge convention |
| Agile enforcement in agent prompts | Convention | StoryForge convention |

## Skills

| Capability | Classification | Anthropic Source |
|---|---|---|
| `~/.claude/skills/<name>/SKILL.md` for user-level | Native | Skills docs: user-level storage |
| `.claude/skills/<name>/SKILL.md` for project-level | Native | Skills docs: project-level storage |
| YAML frontmatter (name, description, etc.) | Native | Skills docs: supported frontmatter fields |
| `$ARGUMENTS` substitution in skill content | Native | Skills docs: string substitutions |
| `disable-model-invocation` for manual-only skills | Native | Skills docs: invocation control |
| `user-invocable: false` for Claude-only skills | Native | Skills docs: invocation control |
| `context: fork` for subagent execution | Native | Skills docs: context field |
| `allowed-tools` for skill-scoped permissions | Native | Skills docs: allowed-tools field |
| `model` for skill-specific model override | Native | Skills docs: model field |
| `effort` for skill effort level | Native | Skills docs: effort field |
| `agent` for specifying subagent type with fork | Native | Skills docs: agent field |
| `hooks` for skill-scoped lifecycle hooks | Native | Skills docs: hooks field |
| `paths` for glob-based auto-activation | Native | Skills docs: paths field |
| `shell` for shell type (bash/powershell) | Native | Skills docs: shell field |
| `$ARGUMENTS[N]` / `$N` positional arguments | Native | Skills docs: argument substitutions |
| `${CLAUDE_SESSION_ID}` substitution variable | Native | Skills docs: session variable |
| `${CLAUDE_SKILL_DIR}` substitution variable | Native | Skills docs: skill directory variable |
| Inline shell injection with `` !`command` `` | Native | Skills docs: shell injection syntax |
| Kanban bootstrap as a skill | Convention | StoryForge convention |
| Story writing as a skill | Convention | StoryForge convention |
| Sprint grooming as a skill | Convention | StoryForge convention |

## Hooks

| Capability | Classification | Anthropic Source |
|---|---|---|
| `SessionStart` hook for session initialization | Native | Hooks docs: SessionStart event |
| `PreToolUse` hook for pre-execution validation | Native | Hooks docs: PreToolUse event |
| `PostToolUse` hook for post-execution actions | Native | Hooks docs: PostToolUse event |
| `Stop` hook for completion checks | Native | Hooks docs: Stop event |
| `UserPromptSubmit` hook for prompt interception | Native | Hooks docs: UserPromptSubmit event |
| `Notification` hook for desktop alerts | Native | Hooks docs: Notification event |
| `InstructionsLoaded` hook for instruction debugging | Native | Hooks docs: InstructionsLoaded event |
| `PermissionRequest` hook for permission interception | Native | Hooks docs: PermissionRequest event |
| `PermissionDenied` hook for denial handling | Native | Hooks docs: PermissionDenied event |
| `PostToolUseFailure` hook for tool failure handling | Native | Hooks docs: PostToolUseFailure event |
| `SubagentStart` / `SubagentStop` lifecycle hooks | Native | Hooks docs: subagent lifecycle events |
| `TaskCreated` / `TaskCompleted` for agent teams | Native | Hooks docs: task lifecycle events |
| `TeammateIdle` for agent team coordination | Native | Hooks docs: TeammateIdle event |
| `ConfigChange` hook for config file changes | Native | Hooks docs: ConfigChange event |
| `CwdChanged` hook for directory changes | Native | Hooks docs: CwdChanged event |
| `FileChanged` hook for watched file changes | Native | Hooks docs: FileChanged event |
| `PreCompact` / `PostCompact` for context compaction | Native | Hooks docs: compaction events |
| `WorktreeCreate` / `WorktreeRemove` lifecycle hooks | Native | Hooks docs: worktree events |
| `Elicitation` / `ElicitationResult` for MCP input | Native | Hooks docs: elicitation events |
| `SessionEnd` hook for session termination | Native | Hooks docs: SessionEnd event |
| `StopFailure` hook for API error handling | Native | Hooks docs: StopFailure event |
| `http` hook handler type (webhooks) | Native | Hooks docs: http handler type |
| `prompt` hook handler type (LLM-evaluated) | Native | Hooks docs: prompt handler type |
| `agent` hook handler type (agent-evaluated) | Native | Hooks docs: agent handler type |
| `if` conditional field for permission filtering | Native | Hooks docs: if field |
| `statusMessage` for custom spinner text | Native | Hooks docs: statusMessage field |
| `once` flag for single execution per session | Native | Hooks docs: once field |
| `async` flag for background execution | Native | Hooks docs: async field |
| `shell` field for handler shell type | Native | Hooks docs: shell field |
| Exit code 2 to block actions | Native | Hooks docs: exit code behavior |
| JSON response format for structured control | Native | Hooks docs: structured JSON response |
| Hook matchers with regex patterns | Native | Hooks docs: hook matchers |
| `$CLAUDE_PROJECT_DIR` in hook commands | Native | Hooks docs: environment variables |
| `$CLAUDE_ENV_FILE` for persistent env in SessionStart | Native | Hooks docs: environment variables |
| `permissionDecision: "defer"` for Agent SDK integration | Native | Hooks docs: PreToolUse defer decision |
| `allowedEnvVars` for HTTP hook header interpolation | Native | Hooks docs: http handler security |
| Session-start context injection | Convention | StoryForge convention using native SessionStart |
| Agile discipline enforcement via hooks | Convention | StoryForge convention using native hooks |

## Kanban Delivery System

| Capability | Classification | Anthropic Source |
|---|---|---|
| `.kanban/` directory with markdown artifacts | Convention | StoryForge convention, not an Anthropic native feature |
| Initiative > Feature > Story > Task hierarchy | Convention | StoryForge convention |
| Board states: Backlog, Ready, In Progress, Review, Done | Convention | StoryForge convention |
| Story template with structured fields | Convention | StoryForge convention |
| Sprint planning artifacts | Convention | StoryForge convention |
| Kanban dashboard CLI tool (Python) | Convention | StoryForge convention |
| Dashboard skill (/dashboard) | Convention | StoryForge convention using native skill |

## Cross-Platform Support

| Capability | Classification | Anthropic Source |
|---|---|---|
| Bash scripts for macOS/Linux/Git Bash | Convention | StoryForge convention |
| PowerShell scripts for Windows | Convention | StoryForge convention |
| Python dashboard (stdlib only) | Convention | StoryForge convention |

## Upstream Adaptation

| Capability | Classification | Anthropic Source |
|---|---|---|
| Release watch process | Convention | StoryForge convention |
| Changelog adaptation workflow | Convention | StoryForge convention |
| Migration templates | Convention | StoryForge convention |
| Impact classification (no impact, docs, config, etc.) | Convention | StoryForge convention |
| Automated upstream monitoring via content hashing | Convention | StoryForge convention |
| GitHub Action cron for daily doc checks | Convention | StoryForge convention |
| Claude Code scheduled trigger for daily monitoring | Native | Scheduled tasks docs: cloud remote agents |
| `/loop` bundled skill for session-scoped polling | Native | Scheduled tasks docs: /loop skill |
| `loop.md` for custom default loop prompt | Native | Scheduled tasks docs: loop.md customization |
| Desktop scheduled tasks (local, persistent) | Native | Scheduled tasks docs: desktop scheduled tasks |
| Cloud scheduled tasks (remote, durable) | Native | Scheduled tasks docs: cloud scheduled tasks |
| `CronCreate` / `CronList` / `CronDelete` tools | Native | Scheduled tasks docs: cron tools |
| upstream-monitor agent (sonnet, automated) | Native | Subagents docs: model, maxTurns fields |
| /upstream-check skill for manual trigger | Native | Skills docs: user-invocable skills |

## CLI Integration

| Capability | Classification | Anthropic Source |
|---|---|---|
| `claude -p` for non-interactive execution | Native | CLI docs: --print flag |
| `--agent` flag for session-wide agent | Native | CLI docs: --agent flag |
| `--permission-mode` for safety modes | Native | CLI docs: --permission-mode flag |
| `--append-system-prompt` for additional context | Native | CLI docs: append-system-prompt flag |
| `--bare` for minimal startup | Native | CLI docs: --bare flag |
| `--worktree` for parallel sessions | Native | CLI docs: --worktree flag |
| Install/bootstrap scripts using CLI | Convention | StoryForge convention using native CLI |

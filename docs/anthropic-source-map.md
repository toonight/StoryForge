# Anthropic Source Map

This document maps every StoryForge capability to the official Anthropic documentation
that justifies or informs its design.

Last audited: 2026-05-07

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
| `Agent(agent1, agent2)` tool syntax to restrict spawnable agents | Native | Subagents docs: control spawnable agent types |
| `CLAUDE_CODE_SUBAGENT_MODEL` env var to override subagent model | Native | Subagents docs: model resolution order |
| `agent-memory/` directory for subagent persistent memory | Native | Subagents docs: memory scope field |
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
| `arguments` for named positional argument declarations | Native | Skills docs: arguments field |
| `hooks` for skill-scoped lifecycle hooks | Native | Skills docs: hooks field |
| `paths` for glob-based auto-activation | Native | Skills docs: paths field |
| `Skill(name)` / `Skill(name *)` permission rule syntax | Native | Permissions docs: Skill tool rules |
| `Agent(AgentName)` permission rule syntax for subagents | Native | Permissions docs: Agent tool rules |
| `PowerShell(cmd *)` permission rule syntax | Native | Permissions docs: PowerShell rules |
| `bypassPermissions` now includes protected paths as of v2.1.126 | Native | Permission modes docs: bypassPermissions v2.1.126 behavior |
| `shell` for shell type (bash/powershell) | Native | Skills docs: shell field |
| `$ARGUMENTS[N]` / `$N` positional arguments | Native | Skills docs: argument substitutions |
| `${CLAUDE_SESSION_ID}` substitution variable | Native | Skills docs: session variable |
| `${CLAUDE_SKILL_DIR}` substitution variable | Native | Skills docs: skill directory variable |
| `${CLAUDE_EFFORT}` substitution variable | Native | Skills docs: effort-level variable |
| Inline shell injection with `` !`command` `` | Native | Skills docs: shell injection syntax |
| Kanban bootstrap as a skill | Convention | StoryForge convention |
| Story writing as a skill | Convention | StoryForge convention |
| Sprint grooming as a skill | Convention | StoryForge convention |

## Hooks

| Capability | Classification | Anthropic Source |
|---|---|---|
| `Setup` hook event for `--init` / `--init-only` / `--maintenance` | Native | Hooks docs: Setup event |
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
| `mcp_tool` hook handler type (MCP server tool call) | Native | Hooks docs: mcp_tool handler type |
| `UserPromptExpansion` hook for slash command expansion | Native | Hooks docs: UserPromptExpansion event |
| `PostToolBatch` hook after parallel tool batch resolves | Native | Hooks docs: PostToolBatch event |
| `${CLAUDE_PLUGIN_ROOT}` in hook commands | Native | Hooks docs: plugin environment variables |
| `${CLAUDE_PLUGIN_DATA}` in hook commands | Native | Hooks docs: plugin environment variables |
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
| `agent_id` / `agent_type` in hook input JSON (subagent context) | Native | Hooks docs: subagent hook input fields |
| `asyncRewake` flag for background hook with wakeup on exit code 2 | Native | Hooks docs: asyncRewake field |
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
| `--agents` flag for CLI-defined subagents | Native | CLI docs: --agents flag |
| `--allowedTools` / `--disallowedTools` flags | Native | CLI docs: tool allow/deny flags |
| `--effort` flag for session effort level | Native | CLI docs: --effort flag |
| `--max-turns` flag for turn limits | Native | CLI docs: --max-turns flag |
| `--max-budget-usd` flag for budget cap | Native | CLI docs: --max-budget-usd flag |
| `--output-format` flag (text/json/stream-json) | Native | CLI docs: --output-format flag |
| `--json-schema` flag for structured output | Native | CLI docs: --json-schema flag |
| `--system-prompt` / `--system-prompt-file` flags | Native | CLI docs: system prompt flags |
| `--resume` / `--continue` session flags | Native | CLI docs: resume/continue flags |
| `--from-pr` to resume PR-linked sessions | Native | CLI docs: --from-pr flag |
| `--name` / `-n` flag for session naming | Native | CLI docs: --name flag |
| `--tools` flag to restrict built-in tools | Native | CLI docs: --tools flag |
| `--setting-sources` flag for scoped settings | Native | CLI docs: --setting-sources flag |
| `--settings` flag for additional settings | Native | CLI docs: --settings flag |
| `--mcp-config` / `--strict-mcp-config` flags | Native | CLI docs: MCP config flags |
| `--plugin-dir` flag for session plugins | Native | CLI docs: --plugin-dir flag |
| `claude install` for binary install/reinstall | Native | CLI docs: install command |
| `claude agents` to list configured subagents | Native | CLI docs: agents command |
| `claude project purge` to clear project state | Native | CLI docs: project purge command |
| `claude auto-mode defaults` to inspect classifier rules | Native | CLI docs: auto-mode command |
| `--include-hook-events` for hook event streaming | Native | CLI docs: --include-hook-events flag |
| `--exclude-dynamic-system-prompt-sections` for cache reuse | Native | CLI docs: --exclude-dynamic-system-prompt-sections flag |
| `--fork-session` to create new session on resume | Native | CLI docs: --fork-session flag |
| `--fallback-model` for overload fallback | Native | CLI docs: --fallback-model flag |
| `claude auth login` / `auth logout` / `auth status` | Native | CLI docs: auth subcommands |
| `claude plugin` (alias `claude plugins`) | Native | CLI docs: plugin command |
| `--init` / `--init-only` / `--maintenance` flags for Setup hooks | Native | CLI docs: Setup-flag triple |
| `--add-dir` for additional working directories | Native | CLI docs: --add-dir flag |
| `--debug` / `--debug-file` flags | Native | CLI docs: debug flags |
| `--ide` / `--no-chrome` / `--chrome` flags | Native | CLI docs: editor and browser integration flags |
| `--session-id` / `--no-session-persistence` / `--name` flags | Native | CLI docs: session control flags |
| `--input-format` / `--include-partial-messages` / `--replay-user-messages` flags | Native | CLI docs: stream-json input/output flags |
| `--permission-prompt-tool` for non-interactive permission MCP tool | Native | CLI docs: --permission-prompt-tool flag |
| `--plugin-url` for fetching session plugins from URL | Native | CLI docs: --plugin-url flag |
| `--remote` / `--remote-control` / `--rc` / `--teleport` flags | Native | CLI docs: remote-control and web-session flags |
| `--tmux` for worktree tmux session | Native | CLI docs: --tmux flag |
| `--betas` / `--channels` / `--disable-slash-commands` flags | Native | CLI docs: misc session flags |
| Install/bootstrap scripts using CLI | Convention | StoryForge convention using native CLI |

## Models & Runtime Modes

| Capability | Classification | Anthropic Source |
|---|---|---|
| Opus 4.7 (1M context) as session model | Native | Claude model card: Opus 4.7 release notes |
| `model: inherit` in agent frontmatter (default) | Native | Subagents docs: model field |
| `/fast` slash command for low-latency sessions | Native | Fast mode docs: Opus 4.6 fast variant |
| Extended thinking budget | Native | Extended thinking docs |
| Prompt caching (5-minute TTL) | Native | Prompt caching docs |
| StoryForge does not pin model IDs in templates | Convention | StoryForge convention to auto-adopt new releases |

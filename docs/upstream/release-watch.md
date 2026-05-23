# Upstream Release Watch

This document tracks Anthropic Claude Code releases and their impact on StoryForge.

## Watch Process

1. Check for new Claude Code releases regularly (at least monthly)
2. For each release, triage changes using the impact classification
3. Record findings in this document
4. Create Stories for required adaptations

## Impact Classification

| Level | Meaning | Action |
|---|---|---|
| No Impact | Change doesn't affect StoryForge | Update verification date |
| Docs Impact | StoryForge docs need updating | Update docs |
| Config Impact | Settings/config affected | Update templates |
| Agent Impact | Agent format/behavior changed | Update agents |
| Hook Impact | Hook events/format changed | Update hooks |
| Skill Impact | Skill format changed | Update skills |
| Migration Required | Breaking change | Create migration Story |

## Release Log

### Baseline: 2026-03-29

- All documentation pages verified as of this date
- StoryForge v0.1.0 built against this baseline
- See `doc-index.md` for full verification dates

---

### 2026-04-15: 7 page changes triaged (Issue #17)

All 7 changes are additive — no breaking changes, no template adaptation required.

| Page | Impact | Notes |
|---|---|---|
| Memory & CLAUDE.md | No Impact | New settings (`autoMemoryDirectory`, `claudeMdExcludes`), AGENTS.md import support |
| Subagents | Docs Impact | New additive frontmatter fields (`effort`, `isolation`, `color`, `background`, `initialPrompt`, `disallowedTools`, `permissionMode`) |
| Hooks | Docs Impact | New events (`PostToolUseFailure`, `SubagentStart/Stop`, `TaskCreated/Completed`, `FileChanged`, `CwdChanged`, compaction, worktree, elicitation), new handler types (`http`, `prompt`, `agent`) |
| Skills | Docs Impact | New additive fields (`effort`, `context`, `agent`, `shell`, `when_to_use`, `user-invocable`, `allowed-tools`) |
| Settings | No Impact | New additive settings, no removals |
| Permissions | No Impact | Existing patterns confirmed valid (`//`, `~/` syntax) |
| Common Workflows | No Impact | Documentation/workflow guidance only |

Action: Updated verification dates. Source map already current. Baseline refresh needed.

---

### 2026-04-17: 13 page changes triaged (Issue #18)

All 13 changes are cosmetic, additive, or already adopted — no breaking changes, no template
adaptation required. StoryForge already tracks every relevant field and event from the prior
#16 and #17 adaptations.

| Page | Impact | Notes |
|---|---|---|
| Subagents | No Impact | Frontmatter fields match source map (`memory`, `paths`, `if`, `effort`, `isolation`, `color`, `background`, `initialPrompt`, `disallowedTools`, `permissionMode`) |
| Hooks | No Impact | 28 events confirmed; handler types (`command`, `http`, `prompt`, `agent`) match source map |
| Skills | No Impact | Frontmatter fields match source map (`effort`, `context`, `agent`, `when_to_use`, `user-invocable`, `allowed-tools`, `paths`, `hooks`, `shell`, `argument-hint`, `model`, `disable-model-invocation`) |
| Settings | No Impact | Additive only; no removals or renames |
| CLI Reference | No Impact | `--enable-auto-mode` removal noted (v2.1.111); StoryForge scripts don't use it. `--bare`, `--permission-mode auto` confirmed |
| Permission Modes | No Impact | Six modes confirmed (`default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`) |
| Permissions | No Impact | Rule syntax unchanged (`//`, `~/`, `/`, relative). Current deny rules in templates remain valid |
| Common Workflows | No Impact | Documentation/workflow guidance only |
| Headless Mode | No Impact | `--print`/`-p`, output formats, `--bare` mode confirmed |
| GitHub Actions | No Impact | v1 GA documented; StoryForge does not ship a `claude-code-action` workflow |
| Agent Teams | No Impact | Experimental, gated by `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`; not adopted by StoryForge |
| MCP | No Impact | Config schema unchanged |
| Scheduled Tasks | No Impact | `/loop`, `loop.md`, `CronCreate/List/Delete`, 7-day expiry, 10% jitter all match prior entries added in #16 |

Action: Updated verification dates to 2026-04-17. No source map changes required. Baseline
refreshed. No adaptation Stories created — the triage confirmed all changes are either
cosmetic or already adopted.

---

### 2026-04-19: 4 page changes triaged (Issue #20)

All 4 changes are cosmetic or already-adopted — no breaking changes, no template adaptation
required. The source map already covers every documented field, event, mode, and tool.

| Page | Impact | Notes |
|---|---|---|
| Hooks | No Impact | 26 events, 4 handler types (command/http/prompt/agent), matchers, common JSON I/O schema — all present in source map (lines 126 to 163). No new events or removals. |
| Settings | No Impact | Scopes (Managed/User/Project/Local), precedence, and fields unchanged from 2026-04-17 baseline. All documented keys (autoMode, worktree.*, claudeMdExcludes, autoMemoryDirectory, disableAllHooks, etc.) already classified Native. |
| Permissions | No Impact | Rule syntax (//, ~/, /, relative, gitignore patterns), six modes (default/acceptEdits/plan/auto/dontAsk/bypassPermissions), precedence (deny > ask > allow), process-wrapper list (timeout/time/nice/nohup/stdbuf/xargs), compound-command handling, symlink rules, auto-mode classifier config — all baseline. Managed-only settings table is additive documentation. |
| Scheduled Tasks | No Impact | /loop variants, loop.md, CronCreate/List/Delete, 7-day expiry, 10 percent jitter (15 min cap), 90-second one-shot jitter, CLAUDE_CODE_DISABLE_CRON, 50-task session cap, v2.1.72 minimum version — all baseline. |

Action: Updated verification dates to 2026-04-19. Baseline refreshed via
scripts/upstream_monitor.py --update-baseline (15 pages rehashed). No source map changes
required. No adaptation Stories created.

---

### 2026-04-21: 3 page changes triaged

All 3 changes are cosmetic or already-adopted — no breaking changes, no template adaptation
required. The source map already covers every documented event, field, handler, and workflow
reference surfaced by these pages.

| Page | Impact | Notes |
|---|---|---|
| Hooks | No Impact | 24 events and 4 handler types (command/http/prompt/agent) confirmed; asyncRewake, defer decision, MCP tool matchers (mcp__server__tool), skill/agent hook frontmatter, FileChanged literal matching, $CLAUDE_ENV_FILE — all already present in source map (lines 126 to 163). No new events or removals. |
| Settings | No Impact | All keys used by StoryForge templates unchanged. Sandbox and plugin marketplace keys (sandbox.*, strictKnownMarketplaces, allowedHttpHookUrls, enabledPlugins) are additive and not adopted by StoryForge. includeCoAuthoredBy deprecation noted; templates already use attribution. |
| Common Workflows | No Impact | Pure documentation/guidance (codebase exploration, worktrees, /loop, routines, Notification hook, --permission-mode plan, --from-pr, --resume, -n). All referenced mechanisms are native CLI features already classified in the source map. |

Action: Updated verification dates to 2026-04-21. Baseline refreshed via
scripts/upstream_monitor.py --update-baseline. No source map changes required. No adaptation
Stories created.

---

### 2026-05-04: 6 page changes triaged (Issue #22)

All 6 changes are additive or clarifications — no breaking changes, no template adaptation
required. Three new entries added to the source map; the rest already match prior baseline.

| Page | Impact | Notes |
|---|---|---|
| Subagents | No Impact | All 16 frontmatter fields match source map. Plugin restrictions confirmed (no `hooks`, `mcpServers`, `permissionMode` for plugin-loaded subagents). `CLAUDE_CODE_SUBAGENT_MODEL` env var noted; not adopted by StoryForge. `Agent(agent_type)` syntax in `tools` field already in source map. |
| Hooks | Docs Impact | New `Setup` event (one-time init via `--init-only` / `--init` / `--maintenance`). New `asyncRewake` field (background hook wakes Claude on exit code 2). Decision values clarified (`allow`/`deny`/`ask`/`defer`/`block`/`retry`). 28 events otherwise match source map. Source map updated with 2 new entries. |
| Skills | Docs Impact | New `${CLAUDE_EFFORT}` substitution variable. All other frontmatter fields and substitutions already in source map. Source map updated with 1 new entry. |
| CLI Reference | No Impact | New flags documented (`--init`, `--init-only`, `--maintenance`, `--effort`, `--fork-session`, `--exclude-dynamic-system-prompt-sections`, `--include-hook-events`, `--allow-dangerously-skip-permissions`, `--remote`, `--teleport`, `--remote-control`, `--channels`, `--max-budget-usd`, `--no-session-persistence`, `--debug-file`). New commands (`claude project purge`, `claude remote-control`, `claude install`, `claude auth login/logout/status`, `claude auto-mode defaults`, `claude ultrareview`, `claude setup-token`, `claude agents`). All additive; StoryForge scripts continue to use `-p`, `--bare`, `--permission-mode`, `--agent`, `--append-system-prompt` as documented. |
| Permission Modes | No Impact | Six modes confirmed (`default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`). Behavior change in v2.1.126: `bypassPermissions` now also skips protected-path prompts. New managed settings (`permissions.disableAutoMode`, `permissions.disableBypassPermissionsMode`) and `showClearContextOnPlanAccept` setting noted; not adopted by StoryForge. Auto mode model and plan requirements documented. Protected paths list (`.git`, `.vscode`, `.idea`, `.husky`, `.claude` minus commands/agents/skills/worktrees, plus dotfiles) consistent with prior behavior. |
| MCP | No Impact | Core config schema unchanged. Three transports (`stdio`, `http`, `sse` — sse deprecated). `claude mcp add/list/get/remove` commands unchanged. No structural changes. |

New source map entries added: `Setup` hook event, `asyncRewake` hook field,
`${CLAUDE_EFFORT}` skill substitution variable.

Action: Updated verification dates to 2026-05-04. Source map updated with 3 new entries.
Baseline refreshed. No template/agent/hook/skill changes required. No adaptation Stories
created.

---

### 2026-04-26: 11 page changes triaged (Issue #21)

All 11 changes are additive or clarifications — no breaking changes, no template adaptation
required. New fields, events, and flags are all additive to what StoryForge already tracks.
Source map updated to reflect new items.

| Page | Impact | Notes |
|---|---|---|
| Memory & CLAUDE.md | No Impact | Clarifications on load order, HTML comment stripping, `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` env var, `--add-dir` behavior. All behavior already consistent with source map entries. |
| Subagents | Docs Impact | All frontmatter fields confirmed present in source map. New docs on `--agents` CLI JSON syntax, `/agents` UI, plugin subagent restrictions, agent-teams integration. No new fields vs prior baseline. |
| Hooks | Docs Impact | New hook handler type `mcp_tool` (5th type, alongside command/http/prompt/agent). Two new events: `UserPromptExpansion` (slash command expansion) and `PostToolBatch` (after parallel batch). New env vars `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}`. All additive; source map updated. |
| Skills | Docs Impact | New `arguments` frontmatter field for named positional arg substitution (`$name` syntax). New `Skill(name)` / `Skill(name *)` permission rule syntax. Plugin skills noted. All additive; source map updated. |
| Settings | No Impact | Additional settings keys documented (`effortLevel`, `tui`, `spinnerTipsEnabled`, `autoScrollEnabled`, `showTurnDuration`, `apiKeyHelper`, `awsCredentialExport`, `availableModels`, MCP allow/deny lists, drop-in `managed-settings.d/` directory). All additive; not adopted by StoryForge templates. |
| Permissions | Docs Impact | New `Agent(AgentName)` and `Skill(name)` permission rule types. `disableAutoMode` setting. Clarification that `.claude/commands`, `.claude/agents`, `.claude/skills` are exempt from bypassPermissions prompts. All additive; source map updated. |
| Common Workflows | No Impact | Expanded documentation: subagent usage workflow, Plan Mode (`Ctrl+G`, auto-session naming from plan), `--worktree` flag, `.worktreeinclude` file, scheduling options table. All referenced mechanisms already in source map. |
| Headless Mode | Docs Impact | Page rebranded to "Run Claude Code programmatically" (Agent SDK framing). New `--json-schema` flag for structured output. `system/api_retry` and `system/init` stream events documented. `--plugin-dir` flag noted. `--bare` already in source map. All additive. |
| Agent Teams | No Impact | Experimental feature unchanged. `teammateMode` setting and `--teammate-mode` flag documented. Feature still not adopted by StoryForge. Source map entry already reflects experimental/not-adopted status. |
| MCP | No Impact | Core config schema unchanged. Page additions are registry UI rendering (React component) and `allowedMcpServers`/`deniedMcpServers` managed settings (already noted under Settings). No structural changes. |
| Scheduled Tasks | No Impact | Scheduling comparison table added (Routines/Desktop/`/loop`). `loop.md` behavior, dynamic interval logic, Monitor tool integration — all consistent with prior baseline entries in source map (lines 196-203). |

New source map entries added: `mcp_tool` hook handler type, `UserPromptExpansion` event,
`PostToolBatch` event, `arguments` skill frontmatter field, `Skill()` permission rule syntax,
`Agent()` permission rule syntax, `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` hook env vars.

Action: Updated verification dates to 2026-04-26. Source map updated with 7 new entries.
Baseline refreshed. No template/agent/hook/skill changes required. No adaptation Stories
created.


### 2026-05-09: 11 page changes triaged (Issue #24)

All 11 changes are cosmetic, additive, or already-adopted clarifications — no breaking
changes, no template adaptation required. One small additive entry added to the source map.

| Page | Impact | Notes |
|---|---|---|
| Memory & CLAUDE.md | No Impact | Wording cleanups around CLAUDE.md vs auto memory roles, AGENTS.md import, claudeMdExcludes, `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`, `--add-dir`. All behaviors already in source map. `CLAUDE_CODE_NEW_INIT=1` for interactive `/init` is additive and not adopted by StoryForge. |
| Subagents | No Impact | All 16 frontmatter fields match source map. Confirms `Agent` (renamed from `Task` in v2.1.63 — alias retained). `--agents` JSON syntax, `claude agents` CLI subcommand, plugin restrictions (no `hooks`, `mcpServers`, `permissionMode`), agent-teams reuse — all already tracked. No new fields. |
| Hooks | No Impact | 30 events confirmed (Setup/SessionStart/SessionEnd/UserPromptSubmit/UserPromptExpansion/PreToolUse/PostToolUse/PostToolUseFailure/PostToolBatch/PermissionRequest/PermissionDenied/SubagentStart/SubagentStop/TaskCreated/TaskCompleted/TeammateIdle/FileChanged/CwdChanged/ConfigChange/InstructionsLoaded/PreCompact/PostCompact/Notification/Elicitation/ElicitationResult/Stop/StopFailure/WorktreeCreate/WorktreeRemove). 5 handler types (command/http/mcp_tool/prompt/agent), `asyncRewake`, `permissionDecision: defer`, `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` — all in source map. Legacy `decision: approve/block` deprecation noted (still mapped to allow/deny). No structural changes. |
| Skills | No Impact | All frontmatter fields match (`name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`). Substitutions (`$ARGUMENTS`, `$N`, `$name`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`, `${CLAUDE_SKILL_DIR}`) match. `skillOverrides` setting and command/skill merger already noted in #21. `disableSkillShellExecution` already tracked. No structural changes. |
| Settings | No Impact | Comprehensive key list reconfirmed. New keys (`policyHelper`, `parentSettingsBehavior`, `disableRemoteControl`, `skillOverrides`, `allowedChannelPlugins`, `blockedMarketplaces`, `pluginTrustMessage`) are additive and not adopted by StoryForge templates. `voiceEnabled` and `includeCoAuthoredBy` deprecations confirmed; templates already use `voice` object and `attribution.commit`. Windows managed-settings path migration (v2.1.75) does not affect StoryForge installs. |
| CLI Reference | No Impact | All flags already classified in source map. No new removals; `--enable-auto-mode` removal in v2.1.111 already noted. New commands (`claude install`, `claude auth login/logout/status`, `claude agents`, `claude auto-mode defaults`, `claude project purge`, `claude remote-control`, `claude setup-token`, `claude ultrareview`) and flags (`--init`, `--init-only`, `--maintenance`, `--effort`, `--fork-session`, `--include-hook-events`, `--json-schema`, `--plugin-dir`, `--plugin-url`, `--remote`, `--teleport`, `--remote-control`, `--channels`, `--max-budget-usd`, `--no-session-persistence`, `--debug-file`, `--allow-dangerously-skip-permissions`, `--exclude-dynamic-system-prompt-sections`, `--teammate-mode`) all additive. |
| Permissions | Docs Impact | Adds explicit `PowerShell(<cmd>)` permission rule documentation with cmdlet-alias canonicalization and AST-based compound parsing. StoryForge templates use Bash rules; PowerShell rule support is a new entry in the source map but does not require template changes. Other content (rule syntaxes, six modes, deny>ask>allow precedence, process wrappers, compound commands, symlink rules, protected paths, `disableAutoMode`, `disableBypassPermissionsMode`) matches baseline. |
| Headless Mode | No Impact | Page rebranded to "Run Claude Code programmatically" (Agent SDK framing). `--bare` recommended for scripts and noted as future default for `-p`. `system/api_retry`, `system/init`, `system/plugin_install` stream events, `--json-schema`, 10MB stdin cap (v2.1.128), `--plugin-dir` — all additive and already covered. StoryForge scripts continue to use `-p`, `--bare`, `--permission-mode`, `--allowedTools`. |
| Agent Teams | No Impact | Still experimental, gated by `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`. `teammateMode` (`auto`/`in-process`/`tmux`) and `--teammate-mode` flag confirmed. Plan-approval workflow, subagent-as-teammate reuse, `TaskCreated`/`TaskCompleted`/`TeammateIdle` hooks already in source map. Feature still not adopted by StoryForge. |
| MCP | No Impact | Three transports confirmed (`stdio`, `http`, `sse` — sse deprecated). Cosmetic: documents `streamable-http` as a JSON alias for `http` (MCP spec name). `claude mcp add/list/get/remove` unchanged. `allowedMcpServers`/`deniedMcpServers` managed settings already noted. No structural changes. |
| Scheduled Tasks | No Impact | Comparison table (Cloud/Desktop/`/loop`) refreshed. `/loop` variants, `loop.md` (project + user precedence, 25KB cap), `CronCreate`/`CronList`/`CronDelete`, 8-char task IDs, 50-task session cap, 7-day expiry, recurring-jitter (≤30 min, half-interval), one-shot 90s early jitter, `CLAUDE_CODE_DISABLE_CRON`, v2.1.72 minimum, Bedrock/Vertex/Foundry override (no-prompt → 10-min fixed) — all match baseline. |

New source map entries added: `PowerShell(<cmd>)` permission rule syntax.

Action: Updated verification dates to 2026-05-09 for the 11 listed pages. Source map
updated with 1 new entry and audit date bumped. Baseline refreshed via
`scripts/upstream_monitor.py --update-baseline` (15 pages rehashed). No
template/agent/hook/skill changes required. No adaptation Stories created.


### 2026-05-14: 13 page changes triaged (Issue #29)

All 13 changes are cosmetic, additive, or already-tracked clarifications — no breaking
changes, no template adaptation required. No source map additions; every newly enumerated
field, event, command, flag, or setting was already classified in the source map.

| Page | Impact | Notes |
|---|---|---|
| Memory & CLAUDE.md | No Impact | Wording refresh on CLAUDE.md vs auto memory roles, AGENTS.md import (Windows symlink requires Admin/Developer Mode), CLAUDE_CODE_DISABLE_AUTO_MEMORY=1, --add-dir + CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD, claudeMdExcludes, managed claudeMd key, /init interactive flow under CLAUDE_CODE_NEW_INIT=1. All baseline. |
| Subagents | No Impact | 17 frontmatter fields confirmed (name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation, color, initialPrompt). Built-in agents (Explore, Plan, general-purpose, statusline-setup, claude-code-guide) documented; --agents JSON, claude agents CLI, plugin restrictions on hooks/mcpServers/permissionMode, CLAUDE_CODE_SUBAGENT_MODEL precedence — all already in source map. |
| Hooks | No Impact | 29 events confirmed (Setup/SessionStart/SessionEnd/UserPromptSubmit/UserPromptExpansion/PreToolUse/PostToolUse/PostToolUseFailure/PostToolBatch/PermissionRequest/PermissionDenied/SubagentStart/SubagentStop/TaskCreated/TaskCompleted/TeammateIdle/FileChanged/CwdChanged/ConfigChange/InstructionsLoaded/PreCompact/PostCompact/Notification/Elicitation/ElicitationResult/Stop/StopFailure/WorktreeCreate/WorktreeRemove). 5 handler types (command/http/mcp_tool/prompt/agent), asyncRewake, permissionDecision: defer, CLAUDE_PLUGIN_ROOT/CLAUDE_PLUGIN_DATA, CLAUDE_ENV_FILE, allowedEnvVars — all baseline. WorktreeCreate HTTP-response worktreePath and Elicitation/ElicitationResult form-output shapes are documentation clarifications, not new APIs. Legacy decision: approve/block still mapped. |
| Skills | No Impact | All 15 frontmatter fields and substitutions ($ARGUMENTS, $ARGUMENTS[N], $N, $name, CLAUDE_SESSION_ID, CLAUDE_EFFORT, CLAUDE_SKILL_DIR) match. skillOverrides, disableSkillShellExecution, skillListingBudgetFraction, maxSkillDescriptionChars, command/skill merger, plugin namespacing all already noted. |
| Settings | No Impact | Larger key enumeration this revision (awaySummaryEnabled, companyAnnouncements, disableDeepLinkRegistration, disabledMcpjsonServers/enabledMcpjsonServers, feedbackSurveyRate, gcpAuthRefresh, httpHookAllowedEnvVars, modelOverrides, otelHeadersHelper, respectGitignore, skipWebFetchPreflight, spinnerTipsOverride, spinnerVerbs, sshConfigs, statusLine, syntaxHighlightingDisabled, useAutoModeDuringPlan, viewMode, prUrlTemplate, prefersReducedMotion, cleanupPeriodDays). All additive and not adopted by StoryForge templates. voiceEnabled and includeCoAuthoredBy deprecations reconfirmed; templates already use replacements. Windows managed-settings path migration (v2.1.75: legacy ProgramData path replaced by Program Files path) reconfirmed; StoryForge installs to user/project scope, not managed, so no impact. |
| CLI Reference | No Impact | New subcommands documented (claude attach, claude logs, claude respawn, claude rm, claude stop/kill, claude plugin) and new flags (--bg, --chrome/--no-chrome, --dangerously-load-development-channels, --ide, --strict-mcp-config, --tmux, --remote-control-session-name-prefix, --replay-user-messages). All additive. StoryForge scripts continue to use -p, --bare, --permission-mode, --agent, --append-system-prompt, --allowedTools. --enable-auto-mode removal (v2.1.111) reconfirmed and unused by StoryForge. |
| Permission Modes | No Impact | Six modes confirmed (default, acceptEdits, plan, auto, dontAsk, bypassPermissions). Mode cycle slot ordering (bypassPermissions first, auto last after plan) clarified; --allow-dangerously-skip-permissions adds bypass to cycle without activating it. Auto-mode requirements clarified (Sonnet 4.6 / Opus 4.6 / Opus 4.7 on Team/Enterprise/API; Opus 4.7-only on Max; not on Bedrock/Vertex/Foundry). Protected paths list (.git, .vscode, .idea, .husky, .claude minus commands/agents/skills/worktrees, plus dotfiles .gitconfig, .bashrc, .zshrc, .profile, .ripgreprc, .mcp.json, .claude.json) matches baseline. |
| Permissions | No Impact | Rule syntaxes (Bash, PowerShell, Read, Write, Edit, WebFetch, mcp__*, Skill, Agent), six modes, deny>ask>allow precedence, gitignore-style anchors (//, ~/, /, relative), process wrappers (timeout, time, nice, nohup, stdbuf, bare xargs), exec wrappers requiring exact match (watch, setsid, ionice, flock, find -exec/-delete), compound-command per-subcommand matching, symlink dual-path rule, Windows POSIX normalization, --add-dir exception table (skills load; CLAUDE.md needs CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1; plugins limited to enabledPlugins/extraKnownMarketplaces). All match baseline. Managed-only settings table reconfirmed. |
| Common Workflows | No Impact | Pure documentation: prompt recipes, --continue/--resume, --worktree, plan mode, subagent delegation, headless via -p, scheduling-comparison table (Routines/Desktop/GitHub Actions//loop). All referenced mechanisms in source map. |
| Headless Mode | No Impact | Page is "Run Claude Code programmatically" (Agent SDK framing). --bare, --output-format json/stream-json, --json-schema, --allowedTools, --permission-mode, --append-system-prompt, 10MB stdin cap (v2.1.128), system/api_retry, system/init, system/plugin_install stream events, total_cost_usd, CLAUDE_CODE_SYNC_PLUGIN_INSTALL — all baseline. Note: June 15 2026 introduces a separate Agent SDK credit for claude -p on subscription plans (billing change only, no API impact). |
| Agent Teams | No Impact | Still experimental, gated by CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS. Minimum v2.1.32. teammateMode (auto/in-process/tmux), --teammate-mode, lead/teammate model selection, plan-approval workflow, subagent-as-teammate reuse (with skills/mcpServers frontmatter ignored on that path), TaskCreated/TaskCompleted/TeammateIdle hooks, team config at ~/.claude/teams/<name>/config.json, task list at ~/.claude/tasks/<name>/. Not adopted by StoryForge. |
| MCP | No Impact | Three transports (stdio, http, sse — sse deprecated). streamable-http JSON alias for http reconfirmed. claude mcp add/list/get/remove, scopes (local/project/user), .mcp.json schema, CLAUDE_PROJECT_DIR in spawned server env, MCP list_changed notifications, HTTP/SSE auto-reconnect (5 attempts, exponential backoff), initial-connection retry v2.1.121 (up to 3 transient retries; auth/not-found not retried), workspace reserved server name, MCP_TIMEOUT, MAX_MCP_OUTPUT_TOKENS. All baseline. |
| Scheduled Tasks | No Impact | v2.1.72 minimum reconfirmed. Comparison table (Cloud/Desktop//loop) refreshed. /loop variants (interval-only/prompt-only/both/bare maintenance), loop.md (project > user, 25KB cap), CronCreate/CronList/CronDelete, 8-char IDs, 50-task cap, 7-day expiry, recurring jitter (<=30 min, half-interval if more often than hourly), one-shot 90s early jitter at :00/:30, vixie-cron semantics for day-of-month + day-of-week, CLAUDE_CODE_DISABLE_CRON, Bedrock/Vertex/Foundry bare-prompt -> usage message, Bedrock/Vertex/Foundry no-interval -> 10-min fixed schedule. All match baseline. |

Action: Updated verification dates to 2026-05-14 for the 13 listed pages. Source map audit
date bumped to 2026-05-14; no new entries needed (every documented field, event, mode, flag,
and command was already classified). Baseline refreshed via
scripts/upstream_monitor.py --update-baseline (15 pages rehashed). No
template/agent/hook/skill changes required. No adaptation Stories created.


### 2026-05-23: 14 page changes triaged (Issue #30)

All 14 changes are cosmetic, additive, or already-tracked clarifications — no breaking
changes, no template adaptation required. One small additive entry added to the source map
(`terminalSequence` hook JSON field, v2.1.141+).

| Page | Impact | Notes |
|---|---|---|
| Memory & CLAUDE.md | No Impact | Wording cleanups on CLAUDE.md vs auto memory roles, AGENTS.md import (Windows symlink requires Admin/Developer Mode), CLAUDE_CODE_DISABLE_AUTO_MEMORY, --add-dir + CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD, claudeMdExcludes, managed claudeMd key, /init interactive flow under CLAUDE_CODE_NEW_INIT=1, comment-stripping behaviour, 200-line auto-memory load cap. All baseline. |
| Subagents | No Impact | Frontmatter fields and built-in agents (Explore, Plan, general-purpose) match source map. --agents JSON, claude agents CLI, plugin restrictions on hooks/mcpServers/permissionMode, CLAUDE_CODE_SUBAGENT_MODEL precedence, subagent auto memory (subagent-configuration) — all already tracked. |
| Hooks | Additive | 29 events confirmed. New `terminalSequence` JSON field (v2.1.141+) for OSC 0/1/2/9/99/777/BEL notification sequences in lieu of /dev/tty writes — added to source map. 5 handler types, asyncRewake, permissionDecision: defer, CLAUDE_PLUGIN_ROOT/CLAUDE_PLUGIN_DATA, CLAUDE_ENV_FILE, allowedEnvVars, mcp_tool with input substitution ${tool_input.field}, deduplication, 10000-char string cap, exit-code 2 blocking matrix, WorktreeCreate worktreePath, Elicitation/ElicitationResult accept/decline/cancel — all baseline or already covered. |
| Skills | No Impact | All 15 frontmatter fields and substitutions match. Bundled /run, /verify, /run-skill-generator (v2.1.145+) are additive bundled skills, not StoryForge-managed. skillOverrides, disableSkillShellExecution, skillListingBudgetFraction, maxSkillDescriptionChars, command/skill merger, plugin namespacing, live change detection, additional-directory loading, ${CLAUDE_SKILL_DIR} — all baseline. |
| Settings | No Impact | Exhaustive key inventory reconfirmed. New keys (`policyHelper`, `parentSettingsBehavior`, `disableRemoteControl`, `disableDeepLinkRegistration`, `awaySummaryEnabled`, `companyAnnouncements`, `feedbackSurveyRate`, `httpHookAllowedEnvVars`, `modelOverrides`, `otelHeadersHelper`, `respectGitignore`, `skipWebFetchPreflight`, `spinnerTipsOverride`, `spinnerVerbs`, `sshConfigs`, `statusLine`, `syntaxHighlightingDisabled`, `useAutoModeDuringPlan`, `viewMode`, `prUrlTemplate`, `prefersReducedMotion`, `cleanupPeriodDays`, `allowedHttpHookUrls`, `forceRemoteSettingsRefresh`, sandbox.*, `enabledMcpjsonServers`/`disabledMcpjsonServers`, `allowedChannelPlugins`, `blockedMarketplaces`, `pluginTrustMessage`, `strictPluginOnlyCustomization`, `allowManagedHooksOnly`, `allowManagedMcpServersOnly`, `allowManagedPermissionRulesOnly`, `wslInheritsWindowsSettings`, `skipDangerousModePermissionPrompt`, `editorMode`, `terminalProgressBarEnabled`, `fastModePerSessionOptIn`, `gcpAuthRefresh`, `awsAuthRefresh`, `autoConnectIde`, `autoInstallIdeExtension`, `externalEditorContext`, `disableAgentView`, `availableModels`, `showThinkingSummaries`, `alwaysThinkingEnabled`, `effortLevel`, `voice.{enabled,mode,autoSubmit}`, JSON `$schema` self-reference at json.schemastore.org). All additive; not adopted by StoryForge templates. voiceEnabled and includeCoAuthoredBy deprecations reconfirmed; legacy ProgramData managed-settings path migration (v2.1.75) reconfirmed and not applicable to StoryForge installs. |
| CLI Reference | No Impact | All flags and subcommands match prior triages (claude install, claude auth login/logout/status, claude agents, claude attach/logs/respawn/rm/stop/kill, claude plugin, claude project purge, claude remote-control, claude setup-token, claude ultrareview, claude daemon status, claude auto-mode defaults, claude mcp; --bg, --bare, --chrome/--no-chrome, --dangerously-load-development-channels, --ide, --strict-mcp-config, --tmux, --remote-control-session-name-prefix, --replay-user-messages, --init/--init-only/--maintenance, --effort, --fork-session, --include-hook-events, --json-schema, --plugin-dir, --plugin-url, --remote, --teleport, --remote-control, --channels, --max-budget-usd, --no-session-persistence, --debug-file, --allow-dangerously-skip-permissions, --exclude-dynamic-system-prompt-sections, --teammate-mode, --append-system-prompt-file, --include-partial-messages, --setting-sources, --agents, --max-turns, --input-format, --output-format, --tools, --disallowedTools, --fallback-model, --betas, --permission-prompt-tool, --session-id, --from-pr, --name, -n). StoryForge scripts continue to use -p, --bare, --permission-mode, --agent, --append-system-prompt, --allowedTools. --enable-auto-mode removal (v2.1.111) reconfirmed and unused. |
| Permission Modes | No Impact | Six modes confirmed. Cycle slot ordering (bypassPermissions first, auto last after plan) reconfirmed. --allow-dangerously-skip-permissions adds bypass to cycle without activating. Auto-mode requirements (Sonnet 4.6 / Opus 4.6 / Opus 4.7 on Team/Enterprise/API; Anthropic API only — not Bedrock/Vertex/Foundry; v2.1.83 minimum), defaultMode: auto ignored from project/local settings (must be ~/.claude/settings.json), boundary statements in conversation, classifier fallback thresholds (3 consecutive / 20 total), broad allow rules dropped on auto entry (Bash(*), PowerShell(*), wildcarded interpreters, package-manager run, Agent allow rules), subagent classifier checkpoints (spawn/per-action/return), protected paths list, v2.1.126 bypassPermissions also skips protected-path prompts, root/sudo refusal — all baseline. |
| Permissions | No Impact | Rule syntaxes (Bash, PowerShell with AST + alias canonicalization, Read, Write, Edit, WebFetch, mcp__server[__tool], Skill(name [*]), Agent(AgentName)), six modes, deny>ask>allow precedence, gitignore-anchored paths (//, ~/, /, relative, bare filename), process wrappers (timeout/time/nice/nohup/stdbuf, bare xargs), exec wrappers always-prompt (watch/setsid/ionice/flock, find -exec/-delete), compound parsing (&&/||/;/|/|&/&/newline, up to 5 saved subcommand rules), :*-suffix equivalence, symlink dual-path rule, Windows POSIX normalization, read-only command set (ls/cat/echo/pwd/head/tail/grep/find/wc/which/diff/stat/du/cd + read-only git), cd inside cwd/additionalDirectories treated read-only, --add-dir exception table (skills load with live reload; enabledPlugins/extraKnownMarketplaces only; CLAUDE.md needs CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1), hook precedence (deny/ask rules still apply over hook allow; exit-code 2 hook blocks even over allow rule), managed-only settings table (allowManagedHooksOnly, allowManagedMcpServersOnly, allowManagedPermissionRulesOnly, strictKnownMarketplaces, strictPluginOnlyCustomization, sandbox.filesystem.allowManagedReadPathsOnly, sandbox.network.allowManagedDomainsOnly, channelsEnabled, allowedChannelPlugins, blockedMarketplaces, pluginTrustMessage, forceRemoteSettingsRefresh, wslInheritsWindowsSettings), SDK managedSettings via parentSettingsBehavior: merge. All baseline. |
| Common Workflows | No Impact | Pure documentation/guidance: prompt recipes, @path mentions (file + directory + MCP resources), image input (drag/paste/path), --continue/--resume, --from-pr, --worktree, plan mode, /plan, subagent delegation, headless via -p, scheduling comparison table (Routines/Desktop/GitHub Actions//loop). All referenced mechanisms already in source map. |
| Best Practices | No Impact | Pure guidance: context-window management, plan-then-implement, /clear, /compact, /rewind, Esc/Esc, /btw side questions, checkpoints, named sessions, --bare in CI, fan-out with claude -p, writer/reviewer pattern, ultrathink, /install-github-app, /sandbox, AskUserQuestion interview pattern, CLAUDE.md ✅/❌ tables, hooks for deterministic enforcement, plugin marketplace. All mechanisms already in source map. |
| Headless Mode | No Impact | Page is "Run Claude Code programmatically" (Agent SDK framing). --bare, --output-format text/json/stream-json, --json-schema with $schema-validated structured_output field, --allowedTools, --permission-mode (incl. dontAsk/acceptEdits in -p), --append-system-prompt[-file], 10MB stdin cap (v2.1.128), system/api_retry stream events with error categories (authentication_failed/oauth_org_not_allowed/billing_error/rate_limit/invalid_request/model_not_found/server_error/max_output_tokens/unknown), system/init (with plugins[] and plugin_errors[]), system/plugin_install (started/installed/failed/completed), CLAUDE_CODE_SYNC_PLUGIN_INSTALL, total_cost_usd, --include-partial-messages. All baseline. June 15 2026 separate Agent SDK credit for `claude -p` on subscription plans (billing change only). |
| GitHub Actions | No Impact | v1 GA documented. Opus 4.7 model parameter (`claude-opus-4-7`) noted. Beta-to-v1 migration table (mode auto-detected, direct_prompt→prompt, custom_instructions→claude_args, etc.). plugin_marketplaces/plugins inputs and skill invocation via prompt are additive. StoryForge does not ship a claude-code-action workflow; the upstream-triage workflow we do ship is a custom GH Action, unaffected by this change. |
| MCP | Additive | Three transports (stdio/http/sse — sse deprecated). streamable-http JSON alias for http. claude mcp add/list/get/remove/serve/add-json/add-from-claude-desktop/reset-project-choices, scopes (local/project/user) + plugin + claude.ai connector precedence, MCP list_changed notifications, HTTP/SSE auto-reconnect (5 attempts exponential backoff), initial-connection retry (3 transient retries, no retry on auth/not-found), workspace reserved server name, MCP_TIMEOUT, MAX_MCP_OUTPUT_TOKENS (default 25k, warn at 10k), per-server `timeout` (ms, floor 1s), CLAUDE_PROJECT_DIR in spawned server env, env-var expansion in .mcp.json (${VAR} / ${VAR:-default}), --callback-port, --client-id/--client-secret + MCP_CLIENT_SECRET env, OAuth pre-configured creds, `oauth.scopes` pinning, `oauth.authServerMetadataUrl` (v2.1.64+), `headersHelper` for dynamic auth (CLAUDE_CODE_MCP_SERVER_NAME/URL env vars, 10s timeout), `alwaysLoad: true` per-server (v2.1.121+) and `_meta.anthropic/alwaysLoad` per-tool, `_meta.anthropic/maxResultSizeChars` (cap 500k chars), Tool Search (ENABLE_TOOL_SEARCH={unset|true|auto|auto:N|false}), WaitForMcpServers fallback when Tool Search disabled, ENABLE_CLAUDEAI_MCP_SERVERS=false, MCP @ resources (@server:protocol://...), MCP prompts as /mcp__server__prompt commands, /mcp menu. All structural items are additive vs. prior baseline; no removals or renames. None of these additions break StoryForge templates (StoryForge does not register MCP servers in templates). |
| Scheduled Tasks | No Impact | v2.1.72 minimum reconfirmed. /loop variants (interval+prompt fixed cron, prompt-only dynamic, bare /loop maintenance), loop.md (.claude/loop.md > ~/.claude/loop.md, 25KB cap), Monitor tool integration for self-paced loops, CronCreate/CronList/CronDelete, 8-char IDs, 50-task cap, 7-day expiry, recurring jitter (≤30 min, half-interval if subhourly), one-shot 90s early jitter at :00/:30, vixie-cron day-of-month/day-of-week semantics, 5-field cron, CLAUDE_CODE_DISABLE_CRON, Bedrock/Vertex/Foundry bare-prompt → usage message, no-interval → 10-min fixed schedule, Esc stops /loop, idle-only firing, --resume/--continue restores unexpired tasks. All match baseline. |

New source map entries added: `terminalSequence` hook JSON field (v2.1.141+).

Action: Updated verification dates to 2026-05-23 for the 14 listed pages. Source map audit
date bumped to 2026-05-23; one new entry added. Baseline refreshed via
`scripts/upstream_monitor.py --update-baseline`. No template/agent/hook/skill changes
required. No adaptation Stories created.

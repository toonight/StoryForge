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

---

### 2026-05-01: 15 page changes triaged (Issue #22)

All 15 changes are additive or clarifications — no breaking changes to StoryForge templates,
agents, hooks, or skills. The GitHub Actions page documents a v1.0 GA with breaking changes
from beta; StoryForge does not ship a GitHub Actions workflow so no adaptation is needed.

| Page | Impact | Notes |
|---|---|---|
| Memory & CLAUDE.md | No Impact | New CLAUDE.md loading detail (HTML comment stripping, sub-directory lazy load), new `/memory` command UX, `CLAUDE_CODE_NEW_INIT=1` env var for interactive `/init`. All additive; already covered in source map. |
| Subagents | Docs Impact | New `Agent(agent1, agent2)` tool-list syntax for coordinator agents restricting which subagents can be spawned. `CLAUDE_CODE_SUBAGENT_MODEL` env var for model override precedence. Subagent `agent-memory/` directory for `memory` field. Source map updated. |
| Hooks | Docs Impact | New `Setup` event (for `--init`, `--init-only`, `--maintenance`). `asyncRewake` field documented explicitly. `agent_id` / `agent_type` in subagent hook input. Source map updated with these 3 entries. |
| Skills | Docs Impact | New `${CLAUDE_EFFORT}` substitution variable. `disableSkillShellExecution` policy setting documented. Live change detection (no restart needed for edits). Source map updated. |
| Settings | No Impact | Expanded key list (sandbox, plugins, channels, voice, UX prefs). All additive; not adopted by StoryForge templates. |
| CLI Reference | Docs Impact | Substantially expanded: new commands (`claude install`, `claude agents`, `claude project purge`, `claude auto-mode defaults`, `claude remote-control`, `claude setup-token`, `claude ultrareview`); many new flags (`--agents`, `--allowedTools`, `--effort`, `--max-turns`, `--max-budget-usd`, `--output-format`, `--json-schema`, `--system-prompt`, `--resume`, `--from-pr`, `--name`, `--tools`, `--setting-sources`, `--settings`, `--mcp-config`, `--strict-mcp-config`, `--plugin-dir`, `--include-hook-events`, `--exclude-dynamic-system-prompt-sections`, `--fork-session`, `--fallback-model`). Source map updated with all CLI additions. StoryForge scripts use only `claude -p`, `--agent`, `--permission-mode`, `--bare`, `--worktree`, `--append-system-prompt` — all still valid. |
| Permission Modes | Docs Impact | `bypassPermissions` as of v2.1.126 now also allows writes to protected paths (`.git`, `.vscode`, `.idea`, `.husky`, `.claude`). `acceptEdits` auto-approves PowerShell commands. Explicit protected-paths and protected-files tables documented. Source map updated. StoryForge templates do not use `bypassPermissions`; no adaptation required. |
| Permissions | Docs Impact | `PowerShell(cmd *)` permission rule syntax documented. Process-wrapper stripping list (timeout/time/nice/nohup/stdbuf, bare xargs) and exec-wrapper non-approvability (`watch`, `setsid`, `flock`) documented. Source map updated. |
| Common Workflows | No Impact | New scheduling comparison table (Routines/Desktop/`/loop`/GitHub Actions). `Ctrl+G` for in-editor plan editing. Session picker keyboard shortcuts. Worker/Reviewer parallel pattern example. All referenced mechanisms already in source map. |
| Best Practices | No Impact | Page substantially rewritten with richer guidance (context management, verification, Plan Mode workflow, subagent use, session management, parallel sessions). All recommendations reference native features already in source map. No new capabilities introduced. |
| Headless Mode | No Impact | Page rebranded "Run Claude Code programmatically." `system/plugin_install` events documented alongside `system/init` and `system/api_retry`. `--bare` as future default for `-p` noted. All additive; source map already covers Agent SDK framing. |
| GitHub Actions | No Impact | v1.0 GA breaking changes from beta documented (renamed inputs, `mode` removed, `claude_args` passthrough). StoryForge does not ship a GitHub Actions workflow; no adaptation required. |
| Agent Teams | No Impact | `TeammateIdle` hook, `TaskCreated`/`TaskCompleted` hooks, `teammateMode` setting all already in source map. Page content unchanged from prior baseline. |
| MCP | No Impact | Core config schema unchanged. Registry UI component is React rendering noise. `allowedMcpServers`/`deniedMcpServers` managed settings already noted under Settings. |
| Scheduled Tasks | No Impact | Scheduling comparison table added. All mechanisms (`/loop`, `CronCreate/List/Delete`, `loop.md`, jitter, 7-day expiry) match prior source map entries. |

New source map entries added: `${CLAUDE_EFFORT}` skill variable, `Setup` hook event,
`agent_id`/`agent_type` hook input fields, `asyncRewake` hook flag, `Agent(a,b)` tools syntax,
`CLAUDE_CODE_SUBAGENT_MODEL` env var, `agent-memory/` subagent memory directory,
`PowerShell()` permission rule, `bypassPermissions` v2.1.126 protected-path behavior,
25 CLI commands and flags now documented in source map.

Action: Updated verification dates to 2026-05-01. Source map updated with ~30 additive entries.
Baseline refreshed. No template/agent/hook/skill changes required. No adaptation Stories created.


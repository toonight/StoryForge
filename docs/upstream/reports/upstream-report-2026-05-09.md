# Upstream Check Report - 2026-05-09

Triage of 11 page changes flagged by the upstream monitor (Issue #24, 2026-05-09 update).
Source: official Anthropic Claude Code documentation at https://code.claude.com/docs/en/.

## Summary

All 11 changes are cosmetic, additive, or already-adopted clarifications. No breaking
changes detected. No template, agent, hook, or skill adaptation required. One additive
entry added to the source map (PowerShell permission rule syntax). Baseline refreshed.

## Per-Page Triage

| Page | Verdict | Impact | Notes |
|---|---|---|---|
| Memory & CLAUDE.md | Cosmetic | No Impact | Wording cleanups; CLAUDE.md vs auto memory roles, AGENTS.md import, `claudeMdExcludes`, `--add-dir`, `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`, `CLAUDE_CODE_NEW_INIT=1` for interactive `/init`. All baselined. |
| Subagents | Additive | No Impact | All 16 frontmatter fields match. Confirms `Agent` (renamed from `Task` in v2.1.63 — alias retained). `--agents` JSON, `claude agents` CLI, plugin restrictions on `hooks`/`mcpServers`/`permissionMode`, agent-teams reuse all tracked. |
| Hooks | Additive | No Impact | 30 events confirmed including `Setup`, `UserPromptExpansion`, `PostToolBatch`, `WorktreeCreate`/`WorktreeRemove`. 5 handler types (command/http/mcp_tool/prompt/agent). `asyncRewake`, `permissionDecision: defer`, plugin env vars all in source map. Legacy `decision: approve/block` deprecation noted (still mapped). |
| Skills | Additive | No Impact | All frontmatter fields and substitutions match. `skillOverrides`, command/skill merger, `disableSkillShellExecution`, plugin namespacing already noted in prior triages. |
| Settings | Additive | No Impact | New keys (`policyHelper`, `parentSettingsBehavior`, `disableRemoteControl`, `skillOverrides`, plugin-marketplace controls) are additive and not adopted by StoryForge. `voiceEnabled` and `includeCoAuthoredBy` deprecations confirmed; templates already use replacements. |
| CLI Reference | Additive | No Impact | New commands (`claude install`, `claude auth login/logout/status`, `claude agents`, `claude auto-mode defaults`, `claude project purge`, `claude remote-control`, `claude setup-token`, `claude ultrareview`) and many flags all additive. StoryForge scripts continue to use `-p`, `--bare`, `--permission-mode`, `--agent`, `--append-system-prompt`, `--allowedTools`. |
| Permissions | Additive (1 new entry) | Docs Impact | Now explicitly documents `PowerShell(<cmd>)` permission rule syntax with cmdlet-alias canonicalization and AST-based compound parsing. Added to source map for completeness. StoryForge templates use Bash rules; no template changes required. Other content (rule syntaxes, six modes, deny>ask>allow precedence, process wrappers, compound commands, symlinks, protected paths, `disableAutoMode`/`disableBypassPermissionsMode`) matches baseline. |
| Headless Mode | Cosmetic | No Impact | Page rebranded to "Run Claude Code programmatically" (Agent SDK framing). `--bare` recommended for scripts and noted as future default for `-p`. `system/api_retry`, `system/init`, `system/plugin_install` stream events, `--json-schema`, 10MB stdin cap (v2.1.128) all additive. |
| Agent Teams | Cosmetic | No Impact | Still experimental, gated by `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`. `teammateMode` (`auto`/`in-process`/`tmux`), `--teammate-mode`, plan-approval workflow, subagent-as-teammate reuse, `TaskCreated`/`TaskCompleted`/`TeammateIdle` hooks all in source map. Not adopted by StoryForge. |
| MCP | Cosmetic | No Impact | Three transports confirmed (stdio, http, sse — sse deprecated). Documents `streamable-http` as a JSON alias for `http` (MCP spec name). `claude mcp add/list/get/remove` unchanged. No structural changes. |
| Scheduled Tasks | Cosmetic | No Impact | Comparison table (Cloud/Desktop/`/loop`) refreshed. `/loop` variants, `loop.md` precedence (project > user), 25KB cap, `CronCreate`/`CronList`/`CronDelete`, 8-char task IDs, 50-task cap, 7-day expiry, jitter rules, `CLAUDE_CODE_DISABLE_CRON`, v2.1.72 minimum all match baseline. |

## Source Map Changes

Audit date bumped to 2026-05-09. Added one entry under the Skills section:

- `PowerShell(<cmd>)` permission rule syntax — Native — Permissions docs: PowerShell rules

No removals; no reclassifications. The source map already covered every other field,
event, mode, command, and flag surfaced by these 11 pages.

## Recommended Actions

1. Merge baseline-hashes refresh (15 pages rehashed via `scripts/upstream_monitor.py --update-baseline`). Priority: Low. Effort: trivial. Done.
2. Update `docs/upstream/doc-index.md` verification dates to 2026-05-09 for the 11 listed pages. Priority: Low. Effort: trivial. Done.
3. Update `docs/anthropic-source-map.md` audit date and add PowerShell permission rule entry. Priority: Low. Effort: trivial. Done.
4. Append 2026-05-09 entry to `docs/upstream/release-watch.md`. Priority: Low. Effort: trivial. Done.

## Adaptation Stories

None required. No breaking changes affect StoryForge templates, agents, hooks, or
skills. All new fields, events, settings, and flags surfaced by this batch are additive
and either already classified in the source map or scoped to features (plugins, channels,
remote control, agent teams, sandboxing, web sessions) that StoryForge does not adopt.

## Verification

- All 11 pages re-fetched and compared against `docs/anthropic-source-map.md` and the
  prior 2026-05-04 baseline (commit b3fcd33).
- `python scripts/upstream_monitor.py --update-baseline` ran cleanly; 15 pages rebaselined.
- No managed-settings, deny-rules, or hook-event removals that would break StoryForge
  templates.

# Upstream Check Report - 2026-05-14

Triage of 13 page changes flagged by the upstream monitor (Issue #29, 2026-05-14 update).
Source: official Anthropic Claude Code documentation at https://code.claude.com/docs/en/.

## Summary

All 13 changes are cosmetic, additive, or already-tracked clarifications. No breaking
changes detected. No template, agent, hook, or skill adaptation required. No new entries
added to the source map (audit date bumped only). Baseline refreshed.

## Per-Page Triage

| Page | Verdict | Impact | Notes |
|---|---|---|---|
| Memory & CLAUDE.md | Cosmetic | No Impact | Wording cleanups on CLAUDE.md vs auto memory roles, AGENTS.md import (Windows symlink requires Admin/Developer Mode), CLAUDE_CODE_DISABLE_AUTO_MEMORY, --add-dir + CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD, claudeMdExcludes, managed claudeMd key, /init interactive flow under CLAUDE_CODE_NEW_INIT=1. All baseline. |
| Subagents | Additive | No Impact | 17 frontmatter fields, all in source map. Built-in agents (Explore, Plan, general-purpose, statusline-setup, claude-code-guide) clarified. --agents JSON, claude agents CLI, plugin restrictions on hooks/mcpServers/permissionMode, CLAUDE_CODE_SUBAGENT_MODEL precedence all tracked. |
| Hooks | Additive | No Impact | 29 events confirmed (added explicit cataloguing of decision: block events list, WorktreeCreate HTTP-response worktreePath, Elicitation/ElicitationResult form-output shapes). 5 handler types and all env vars in source map. Legacy decision: approve/block deprecation noted. |
| Skills | Additive | No Impact | 15 frontmatter fields and all substitutions match. skillOverrides, disableSkillShellExecution, skillListingBudgetFraction, maxSkillDescriptionChars, command/skill merger, plugin namespacing all already noted in prior triages. |
| Settings | Additive | No Impact | Larger key enumeration this revision adds awaySummaryEnabled, companyAnnouncements, disableDeepLinkRegistration, disabledMcpjsonServers/enabledMcpjsonServers, feedbackSurveyRate, gcpAuthRefresh, httpHookAllowedEnvVars, modelOverrides, otelHeadersHelper, respectGitignore, skipWebFetchPreflight, spinnerTipsOverride, spinnerVerbs, sshConfigs, statusLine, syntaxHighlightingDisabled, useAutoModeDuringPlan, viewMode, prUrlTemplate, prefersReducedMotion, cleanupPeriodDays. All additive; not adopted by StoryForge templates. voiceEnabled / includeCoAuthoredBy deprecations reconfirmed; templates already use replacements. Windows managed-settings path migration (v2.1.75) reconfirmed; StoryForge does not install to the managed scope. |
| CLI Reference | Additive | No Impact | New subcommands documented (claude attach, claude logs, claude respawn, claude rm, claude stop/kill, claude plugin) and new flags (--bg, --chrome/--no-chrome, --dangerously-load-development-channels, --ide, --strict-mcp-config, --tmux, --remote-control-session-name-prefix, --replay-user-messages). All additive. StoryForge scripts continue to use -p, --bare, --permission-mode, --agent, --append-system-prompt, --allowedTools. --enable-auto-mode removal (v2.1.111) reconfirmed and unused. |
| Permission Modes | Additive | No Impact | Six modes confirmed. Cycle slot ordering clarified (bypassPermissions first, auto last after plan). --allow-dangerously-skip-permissions adds bypass to cycle without activating. Auto-mode requirements clarified (Sonnet 4.6 / Opus 4.6 / Opus 4.7 on Team/Enterprise/API; Opus 4.7-only on Max; not on Bedrock/Vertex/Foundry). Protected paths list matches baseline. |
| Permissions | Cosmetic | No Impact | All rule syntaxes (Bash, PowerShell, Read, Write, Edit, WebFetch, mcp__*, Skill, Agent), six modes, process wrappers, exec wrappers, compound parsing, symlink dual-path rule, Windows POSIX normalization, --add-dir exception table â€” all match baseline. Managed-only settings table reconfirmed. |
| Common Workflows | Cosmetic | No Impact | Pure documentation: prompt recipes, --continue/--resume, --worktree, plan mode, subagent delegation, headless via -p, scheduling-comparison table. All mechanisms in source map. |
| Headless Mode | Additive | No Impact | Page is "Run Claude Code programmatically" (Agent SDK framing). --bare, --output-format json/stream-json, --json-schema, 10MB stdin cap (v2.1.128), system/api_retry, system/init, system/plugin_install stream events, total_cost_usd, CLAUDE_CODE_SYNC_PLUGIN_INSTALL â€” all baseline. New: June 15 2026 separate Agent SDK credit for claude -p on subscription plans (billing change only). |
| Agent Teams | Cosmetic | No Impact | Still experimental, gated by CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS. Minimum v2.1.32. teammateMode, --teammate-mode, plan-approval workflow, subagent-as-teammate reuse (with skills/mcpServers frontmatter ignored on that path), TaskCreated/TaskCompleted/TeammateIdle hooks, team config and task list paths under ~/.claude/. Not adopted by StoryForge. |
| MCP | Cosmetic | No Impact | Three transports (stdio, http, sse â€” sse deprecated). streamable-http JSON alias for http reconfirmed. claude mcp commands, scopes (local/project/user), MCP list_changed notifications, HTTP/SSE auto-reconnect, initial-connection retry v2.1.121 (3 transient retries; auth/not-found not retried), workspace reserved server name, MCP_TIMEOUT, MAX_MCP_OUTPUT_TOKENS. All baseline. |
| Scheduled Tasks | Cosmetic | No Impact | v2.1.72 minimum reconfirmed. Comparison table refreshed. /loop variants, loop.md precedence and 25KB cap, CronCreate/CronList/CronDelete, 8-char IDs, 50-task cap, 7-day expiry, jitter rules, CLAUDE_CODE_DISABLE_CRON, Bedrock/Vertex/Foundry overrides â€” all match baseline. |

## Source Map Changes

Audit date bumped from 2026-05-09 to 2026-05-14. No entries added or removed; no
reclassifications. Every field, event, mode, command, flag, and setting surfaced by these
13 pages was already classified in the source map.

## Recommended Actions

1. Merge baseline-hashes refresh (15 pages rehashed via scripts/upstream_monitor.py --update-baseline). Priority: Low. Effort: trivial. Done.
2. Update docs/upstream/doc-index.md verification dates to 2026-05-14 for the 13 listed pages. Priority: Low. Effort: trivial. Done.
3. Bump docs/anthropic-source-map.md audit date to 2026-05-14. Priority: Low. Effort: trivial. Done.
4. Append 2026-05-14 entry to docs/upstream/release-watch.md. Priority: Low. Effort: trivial. Done.

## Adaptation Stories

None required. No breaking changes affect StoryForge templates, agents, hooks, or
skills. All new fields, events, settings, and flags surfaced by this batch are additive
and either already classified in the source map or scoped to features (plugins, channels,
remote control, agent teams, sandboxing, web sessions, background agents, Chrome integration)
that StoryForge does not adopt.

## Verification

- All 13 pages re-fetched and compared against docs/anthropic-source-map.md and the
  prior 2026-05-09 baseline (commit 190d547).
- python scripts/upstream_monitor.py --update-baseline ran cleanly; 15 pages rebaselined.
- No managed-settings, deny-rules, or hook-event removals that would break StoryForge
  templates.
- Settings deprecations (voiceEnabled, includeCoAuthoredBy) and the Windows managed-settings
  path migration (v2.1.75) reconfirmed; StoryForge templates already align with replacements
  and do not install to the affected managed-settings location.

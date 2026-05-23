# Upstream Check Report - 2026-05-23

Triage of 14 page changes flagged by the upstream monitor (Issue #30, 2026-05-23 update).
Source: official Anthropic Claude Code documentation at https://code.claude.com/docs/en/.

## Summary

All 14 changes are cosmetic, additive, or already-tracked clarifications. No breaking
changes detected. No template, agent, hook, or skill adaptation required. One new entry
added to the source map (`terminalSequence` hook JSON field, v2.1.141+). Baseline
refreshed.

## Per-Page Triage

| Page | Verdict | Impact | Notes |
|---|---|---|---|
| Memory & CLAUDE.md | Cosmetic | No Impact | Wording cleanups on CLAUDE.md vs auto memory roles, AGENTS.md import (Windows symlink requires Admin/Developer Mode), CLAUDE_CODE_DISABLE_AUTO_MEMORY, --add-dir + CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD, claudeMdExcludes, managed claudeMd key, /init interactive flow under CLAUDE_CODE_NEW_INIT=1, HTML-comment stripping, 200-line/25KB auto-memory load cap. All baseline. |
| Subagents | Additive | No Impact | Frontmatter fields and built-in agents (Explore, Plan, general-purpose) match source map. --agents JSON, claude agents CLI, plugin restrictions on hooks/mcpServers/permissionMode, CLAUDE_CODE_SUBAGENT_MODEL precedence, subagent auto memory (subagent-configuration) — all already tracked. |
| Hooks | Additive | Docs Impact | 29 events confirmed. New `terminalSequence` JSON field (v2.1.141+) for OSC 0/1/2/9/99/777/BEL notification sequences in lieu of /dev/tty writes — added to source map. 5 handler types, asyncRewake, permissionDecision: defer, CLAUDE_PLUGIN_ROOT/CLAUDE_PLUGIN_DATA, CLAUDE_ENV_FILE, allowedEnvVars, mcp_tool with input substitution `${tool_input.field}`, deduplication, 10000-char string cap, exit-code 2 blocking matrix, WorktreeCreate worktreePath, Elicitation/ElicitationResult accept/decline/cancel — all baseline or already covered. |
| Skills | Additive | No Impact | All 15 frontmatter fields and substitutions match. Bundled /run, /verify, /run-skill-generator (v2.1.145+) are additive bundled skills, not StoryForge-managed. skillOverrides, disableSkillShellExecution, skillListingBudgetFraction, maxSkillDescriptionChars, command/skill merger, plugin namespacing, live change detection, additional-directory loading, ${CLAUDE_SKILL_DIR} — all baseline. |
| Settings | Additive | No Impact | Exhaustive key inventory reconfirmed. New/expanded keys (`policyHelper`, `parentSettingsBehavior`, `disableRemoteControl`, `disableDeepLinkRegistration`, `awaySummaryEnabled`, `companyAnnouncements`, `feedbackSurveyRate`, `httpHookAllowedEnvVars`, `modelOverrides`, `otelHeadersHelper`, `respectGitignore`, `skipWebFetchPreflight`, `spinnerTipsOverride`, `spinnerVerbs`, `sshConfigs`, `statusLine`, `syntaxHighlightingDisabled`, `useAutoModeDuringPlan`, `viewMode`, `prUrlTemplate`, `prefersReducedMotion`, `cleanupPeriodDays`, `allowedHttpHookUrls`, `forceRemoteSettingsRefresh`, sandbox.*, `enabledMcpjsonServers`/`disabledMcpjsonServers`, `allowedChannelPlugins`, `blockedMarketplaces`, `pluginTrustMessage`, `strictPluginOnlyCustomization`, `allowManagedHooksOnly`, `allowManagedMcpServersOnly`, `allowManagedPermissionRulesOnly`, `wslInheritsWindowsSettings`, `skipDangerousModePermissionPrompt`, `editorMode`, `terminalProgressBarEnabled`, `fastModePerSessionOptIn`, `gcpAuthRefresh`, `awsAuthRefresh`, `autoConnectIde`, `autoInstallIdeExtension`, `externalEditorContext`, `disableAgentView`, `availableModels`, `showThinkingSummaries`, `alwaysThinkingEnabled`, `effortLevel`, `voice.{enabled,mode,autoSubmit}`). All additive; not adopted by StoryForge templates. voiceEnabled and includeCoAuthoredBy deprecations reconfirmed. Legacy ProgramData managed-settings path (v2.1.75) reconfirmed migrated; StoryForge does not install to managed scope. |
| CLI Reference | Additive | No Impact | New subcommands and flags reconfirmed (claude install, claude auth login/logout/status, claude agents, claude attach/logs/respawn/rm/stop/kill, claude plugin, claude project purge, claude remote-control, claude setup-token, claude ultrareview, claude daemon status, claude auto-mode defaults; --bg, --bare, --chrome/--no-chrome, --dangerously-load-development-channels, --ide, --strict-mcp-config, --tmux, --remote-control-session-name-prefix, --replay-user-messages, --init/--init-only/--maintenance, --effort, --fork-session, --include-hook-events, --json-schema, --plugin-dir, --plugin-url, --remote, --teleport, --remote-control, --channels, --max-budget-usd, --no-session-persistence, --debug-file, --allow-dangerously-skip-permissions, --exclude-dynamic-system-prompt-sections, --teammate-mode). All additive. StoryForge scripts continue to use -p, --bare, --permission-mode, --agent, --append-system-prompt, --allowedTools. --enable-auto-mode removal (v2.1.111) reconfirmed and unused. |
| Permission Modes | Additive | No Impact | Six modes confirmed. Cycle slot ordering (bypassPermissions first, auto last after plan) reconfirmed. --allow-dangerously-skip-permissions adds bypass to cycle without activating. Auto-mode requirements (Sonnet 4.6 / Opus 4.6 / Opus 4.7 on Team/Enterprise/API; Anthropic API only — not Bedrock/Vertex/Foundry; v2.1.83 minimum), defaultMode: auto ignored from project/local settings (must be ~/.claude/settings.json), conversation-stated boundaries enforced via classifier re-read on each check, classifier fallback thresholds (3 consecutive / 20 total), broad allow rules dropped on auto entry, subagent classifier checkpoints (spawn/per-action/return), protected paths list, v2.1.126 bypassPermissions also skips protected-path prompts, root/sudo refusal. All baseline. |
| Permissions | Cosmetic | No Impact | Rule syntaxes (Bash, PowerShell with AST + alias canonicalization, Read, Write, Edit, WebFetch, mcp__server[__tool], Skill(name [*]), Agent(AgentName)), six modes, deny>ask>allow precedence, gitignore-anchored paths (//, ~/, /, relative, bare filename), process wrappers (timeout/time/nice/nohup/stdbuf, bare xargs), exec wrappers always-prompt (watch/setsid/ionice/flock, find -exec/-delete), compound parsing (&&/||/;/|/|&/&/newline, up to 5 saved subcommand rules), :*-suffix equivalence, symlink dual-path rule, Windows POSIX normalization, read-only command set, cd inside cwd/additionalDirectories treated read-only, --add-dir exception table, hook precedence rules (deny/ask rules still apply over hook allow; exit-code 2 hook blocks even over allow rule), managed-only settings table, SDK managedSettings via parentSettingsBehavior: merge. All baseline. |
| Common Workflows | Cosmetic | No Impact | Pure documentation/guidance: prompt recipes, @path mentions (file + directory + MCP resources), image input, --continue/--resume, --from-pr, --worktree, plan mode, /plan, subagent delegation, headless via -p, scheduling comparison table (Routines/Desktop/GitHub Actions//loop). All referenced mechanisms already in source map. |
| Best Practices | Cosmetic | No Impact | Pure guidance: context-window management, plan-then-implement, /clear, /compact, /rewind, Esc/Esc, /btw side questions, checkpoints, named sessions, --bare in CI, fan-out with claude -p, writer/reviewer pattern, ultrathink, /install-github-app, /sandbox, AskUserQuestion interview pattern, CLAUDE.md ✅/❌ tables, hooks for deterministic enforcement, plugin marketplace. All mechanisms already in source map. |
| Headless Mode | Additive | No Impact | Page is "Run Claude Code programmatically" (Agent SDK framing). --bare, --output-format text/json/stream-json, --json-schema with $schema-validated structured_output field, --allowedTools, --permission-mode (incl. dontAsk/acceptEdits in -p), --append-system-prompt[-file], 10MB stdin cap (v2.1.128), system/api_retry stream events with error categories (authentication_failed/oauth_org_not_allowed/billing_error/rate_limit/invalid_request/model_not_found/server_error/max_output_tokens/unknown), system/init (with plugins[] and plugin_errors[]), system/plugin_install (started/installed/failed/completed), CLAUDE_CODE_SYNC_PLUGIN_INSTALL, total_cost_usd, --include-partial-messages. All baseline. June 15 2026 separate Agent SDK credit for `claude -p` on subscription plans (billing change only, reconfirmed). |
| GitHub Actions | Additive | No Impact | v1 GA documented. Opus 4.7 model parameter (`claude-opus-4-7`) noted. Beta-to-v1 migration table (mode auto-detected, direct_prompt→prompt, custom_instructions→claude_args, etc.). plugin_marketplaces/plugins inputs and skill invocation via prompt are additive. StoryForge does not ship a claude-code-action workflow; the upstream-triage workflow we do ship is a custom GH Action and is unaffected. |
| MCP | Additive | No Impact | Three transports (stdio/http/sse — sse deprecated). streamable-http JSON alias for http. claude mcp add/list/get/remove/serve/add-json/add-from-claude-desktop/reset-project-choices; scopes (local/project/user) + plugin + claude.ai connector precedence; MCP list_changed; HTTP/SSE auto-reconnect (5 attempts exponential backoff); initial-connection retry (3 transient retries, no retry on auth/not-found); workspace reserved server name; MCP_TIMEOUT; MAX_MCP_OUTPUT_TOKENS (default 25k, warn at 10k); per-server `timeout` (ms, floor 1s); CLAUDE_PROJECT_DIR in spawned server env; env-var expansion in .mcp.json (${VAR} / ${VAR:-default}); --callback-port; --client-id/--client-secret + MCP_CLIENT_SECRET env; OAuth pre-configured creds; `oauth.scopes` pinning; `oauth.authServerMetadataUrl` (v2.1.64+); `headersHelper` for dynamic auth (CLAUDE_CODE_MCP_SERVER_NAME/URL env vars, 10s timeout); `alwaysLoad: true` per-server (v2.1.121+) and `_meta.anthropic/alwaysLoad` per-tool; `_meta.anthropic/maxResultSizeChars` (cap 500k chars); Tool Search (ENABLE_TOOL_SEARCH={unset/true/auto/auto:N/false}); WaitForMcpServers fallback when Tool Search disabled; ENABLE_CLAUDEAI_MCP_SERVERS=false; MCP @ resources; MCP prompts as /mcp__server__prompt; /mcp menu. All structural items are additive vs. baseline; no removals or renames. None affect StoryForge templates (StoryForge does not register MCP servers in templates). |
| Scheduled Tasks | Cosmetic | No Impact | v2.1.72 minimum reconfirmed. /loop variants (interval+prompt fixed cron, prompt-only dynamic, bare /loop maintenance), loop.md (.claude/loop.md > ~/.claude/loop.md, 25KB cap), Monitor tool integration for self-paced loops, CronCreate/CronList/CronDelete, 8-char IDs, 50-task cap, 7-day expiry, recurring jitter (≤30 min, half-interval if subhourly), one-shot 90s early jitter at :00/:30, vixie-cron day-of-month/day-of-week semantics, 5-field cron, CLAUDE_CODE_DISABLE_CRON, Bedrock/Vertex/Foundry overrides, Esc stops /loop, idle-only firing, --resume/--continue restores unexpired tasks. All baseline. |

## Source Map Changes

Audit date bumped from 2026-05-14 to 2026-05-23. One additive entry added under the Hooks
section:

- `terminalSequence` JSON field for OSC notifications (v2.1.141+) — replaces direct
  `/dev/tty` writes from hook handlers for desktop notification escape sequences
  (allowlisted: OSC 0/1/2 window titles, OSC 9 iTerm2/ConEmu/Windows Terminal/WezTerm,
  OSC 99 Kitty, OSC 777 urxvt/Ghostty/Warp, bare BEL).

No removals or reclassifications. Every other field, event, mode, command, flag, and
setting surfaced by these 14 pages was already classified in the source map.

## Recommended Actions

1. Merge baseline-hashes refresh via `scripts/upstream_monitor.py --update-baseline`.
   Priority: Low. Effort: trivial. Done.
2. Update `docs/upstream/doc-index.md` verification dates to 2026-05-23 for the 14 listed
   pages. Priority: Low. Effort: trivial. Done.
3. Bump `docs/anthropic-source-map.md` audit date to 2026-05-23 and add the
   `terminalSequence` hook entry. Priority: Low. Effort: trivial. Done.
4. Append the 2026-05-23 entry to `docs/upstream/release-watch.md`. Priority: Low.
   Effort: trivial. Done.

## Adaptation Stories

None required. No breaking changes affect StoryForge templates, agents, hooks, or
skills. The single additive item (`terminalSequence`) is a new optional hook JSON field
that StoryForge templates do not currently emit; existing handlers continue to work
unchanged. All other new fields, events, settings, flags, and commands surfaced by this
batch are additive and either already classified in the source map or scoped to features
(plugins, channels, remote control, agent teams, sandboxing, web sessions, background
agents, Chrome integration, claude.ai connectors, OAuth client metadata, MCP dynamic
headers, tool search) that StoryForge does not adopt in templates.

## Verification

- All 14 pages re-fetched and compared against `docs/anthropic-source-map.md` and the
  prior 2026-05-14 baseline (commit 9f497ba).
- `python scripts/upstream_monitor.py --update-baseline` ran cleanly.
- No managed-settings, deny-rules, or hook-event removals that would break StoryForge
  templates.
- Settings deprecations (`voiceEnabled`, `includeCoAuthoredBy`) and the Windows
  managed-settings path migration (v2.1.75) reconfirmed; StoryForge templates already
  align with replacements and do not install to the affected managed-settings location.
- `--enable-auto-mode` removal (v2.1.111) reconfirmed; StoryForge scripts do not use it.
- MCP additions (`headersHelper`, `oauth.scopes`, `oauth.authServerMetadataUrl`,
  `alwaysLoad`, `_meta.anthropic/maxResultSizeChars`, Tool Search) are net-additive to
  the protocol and do not affect StoryForge (no MCP servers registered in templates).

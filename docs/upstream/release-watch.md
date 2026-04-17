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

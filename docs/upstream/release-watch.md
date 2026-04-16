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

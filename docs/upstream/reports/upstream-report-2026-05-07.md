# Upstream Documentation Change Report

**Generated**: 2026-05-07T20:44:41Z
**Pages checked**: 15
**Changes detected**: 8 (per Issue #24)
**New pages**: 0
**Unreachable**: 0
**Unchanged**: 7

## Changes Detected

### Hooks

- **URL**: https://code.claude.com/docs/en/hooks
- **Last checked**: 2026-05-01T20:44:12Z
- **Impact areas**: settings.json hooks, enforcement layer
- **Action required**: Reviewed; cosmetic. All events, handler types, env vars already in source map.

### Skills

- **URL**: https://code.claude.com/docs/en/skills
- **Last checked**: 2026-05-01T20:44:12Z
- **Impact areas**: skill definitions, SKILL.md format
- **Action required**: Reviewed; cosmetic. All frontmatter, substitutions, permission rules already in source map.

### Settings

- **URL**: https://code.claude.com/docs/en/settings
- **Last checked**: 2026-05-01T20:44:12Z
- **Impact areas**: settings.json templates, permission rules
- **Action required**: Reviewed; expanded key inventory documented (UX/voice/sandbox/managed). All additive; not adopted by StoryForge templates.

### CLI Reference

- **URL**: https://code.claude.com/docs/en/cli-reference
- **Last checked**: 2026-05-01T20:44:12Z
- **Impact areas**: scripts, CLI usage patterns
- **Action required**: Reviewed; new auth/plugin commands, init/maintenance and channel/chrome/debug/teleport/tmux flags. All additive; StoryForge scripts use only `claude -p`, `--bare`, `--agent`, `--permission-mode`, `--append-system-prompt`, `--worktree` which remain valid.

### Permissions

- **URL**: https://code.claude.com/docs/en/permissions
- **Last checked**: 2026-05-01T20:44:12Z
- **Impact areas**: permission rules, deny patterns
- **Action required**: Reviewed; cosmetic. PowerShell, Skill, Agent, MCP, gitignore-style Read/Edit syntax all already in source map.

### Headless Mode

- **URL**: https://code.claude.com/docs/en/headless
- **Last checked**: 2026-05-01T20:44:12Z
- **Impact areas**: scripts, CI integration
- **Action required**: Reviewed; rebrand to "Run Claude Code programmatically." All stream events (system/init, system/api_retry, system/plugin_install) already in source map. Stdin 10MB cap (v2.1.128) noted previously.

### MCP

- **URL**: https://code.claude.com/docs/en/mcp
- **Last checked**: 2026-05-01T20:44:12Z
- **Impact areas**: MCP configuration
- **Action required**: No impact. Hash drift from React server-registry component; configuration schema unchanged.

### Scheduled Tasks

- **URL**: https://code.claude.com/docs/en/scheduled-tasks
- **Last checked**: 2026-05-01T20:44:12Z
- **Impact areas**: cron configuration, monitoring
- **Action required**: Reviewed; cosmetic. /loop, CronCreate/List/Delete, jitter, 7-day expiry, 50-task cap, Bedrock/Vertex/Foundry exception, CLAUDE_CODE_DISABLE_CRON all match source map.

### Recommended Actions

1. Updated verification dates to 2026-05-07 for the 8 pages.
2. Refreshed baseline-hashes.json via `python scripts/upstream_monitor.py --update-baseline`.
3. No source map changes required: every additive item from these 8 pages was already added in prior triages (#16, #17, #20, #21, #22).
4. No adaptation Stories created.

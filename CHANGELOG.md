# Changelog

## [1.2.1] - 2026-04-04

### Upstream Adaptation (Issue #8)
- Reviewed 15 changed Anthropic documentation pages (2 HIGH, 2 MEDIUM, 4 LOW, 6 NONE)
- Updated `anthropic-source-map.md` with 49 new native entries:
  - 7 subagent frontmatter fields: `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`, `mcpServers`
  - 20 new hook events (from 6 to 26): `InstructionsLoaded`, `PermissionRequest`, `SubagentStart/Stop`, `SessionEnd`, etc.
  - 3 new hook handler types: `http`, `prompt`, `agent`
  - 8 new hook handler fields: `if`, `statusMessage`, `once`, `async`, `shell`, etc.
  - 6 new skill frontmatter fields: `model`, `effort`, `agent`, `hooks`, `paths`, `shell`
  - 5 new settings fields: `claudeMdExcludes`, `autoMemoryEnabled`, `autoMemoryDirectory`, `disableAllHooks`, `disableSkillShellExecution`
- Updated verification dates for all 15 pages in `doc-index.md`
- Refreshed upstream baseline hashes
- No breaking changes — all upstream updates are additive
- Closed Issues #7 (superseded) and #8 (adapted)

## [1.2.0] - 2026-04-02

### Features First-Class (Issue #6)
- Added `features/` directory to kanban structure with `FEAT-TEMPLATE.md`
- Feature files (`FEAT-NNN.md`) support Goal, Stories, Acceptance Criteria sections
- `kanban_webui.py` parses feature files and displays goal, story grouping, and completion progress
- `dashboard.py` loads feature files and merges with board.md features
- `/story-write` skill now creates feature files when a new feature is referenced
- Kanban rules updated: every feature must have a file, every story must reference a feature
- Bootstrap scripts (Bash + PowerShell) create `features/` directory and copy template
- Sample project includes `FEAT-001.md` example

### WebUI Robustness
- Auto-detect and kill previous instance when launching on the same port (Windows + Unix)

### Board/Stories Sync (Issue #5)
- Added `find_missing_story_files()` and `find_missing_feature_files()` detection
- Kanban WebUI shows a warning banner when board.md references stories or features without files
- Warning updates in real-time via live reload polling

### Upstream Docs Reviewed (Issue #4)
- Reviewed 9 changed Anthropic documentation pages: no breaking changes, all additive
- Updated verification dates in `doc-index.md` for 9 pages
- Refreshed upstream baseline hashes (15 pages)

### Validation Fixes
- Fixed `validate_templates.sh` and `.ps1`: skill path checks now match v2 architecture
  (global skills at `templates/home/`, project skills at `templates/project/`)
- Added project-level skill frontmatter validation
- Added feature template and directory existence checks
- Validation now passes with 0 errors (was 6 pre-existing mismatches)

### Testing
- Added `test_kanban_webui.py` with 17 tests covering story/feature sync detection,
  feature file parsing, and board integration
- Added 5 template structure tests for feature support
- Total: 289 tests (was 265)

## [1.1.0] - 2026-04-01

### Upstream Monitor Hardened
- Replaced `peter-evans/create-issue-from-file` with native `gh issue create` in GitHub Actions workflow
- Improved content normalization: strips Next.js build artifacts, `<link>`/`<meta>` tags, UUIDs to eliminate false positives
- Added `--issue-body` flag to `upstream_monitor.py`, removing fragile inline Python from the workflow
- Replaced `2>/dev/null` with proper stderr logging and GitHub Actions warnings

### Security Fixes
- Fixed stored XSS in Kanban WebUI: all user-sourced values now escaped via `esc()` before `innerHTML`
- Fixed sed injection in `bootstrap_project.sh`: `PROJECT_NAME` metacharacters are now escaped
- Added missing `Read` deny rules for `.env` / `.env.*` in repo settings

### Quality
- Added `type: ignore[attr-defined]` for `sys.stdout.reconfigure()` across all Python scripts (Pylance false positive)

## [1.0.0] - 2026-03-29

Initial release of StoryForge.

### Core Framework
- Global CLAUDE.md template with agile operating rules
- User-level settings.json with SessionStart, PostToolUse, Stop, and Notification hooks
- Permission deny rules for .env and .ssh files
- Project templates with .claude/ and .kanban/ structure
- Story template with Depends-On and GitHub fields
- Path-specific .claude/rules/ in both user and project templates
- Install and bootstrap scripts (Bash + PowerShell)

### Agents
- `portfolio-orchestrator`: top-level coordinator with decision tree and scope drift detection
- `planner`: story creation with good/bad examples and splitting guidance
- `implementer`: scope-bounded execution with pre-implementation checklist
- `reviewer`: quality review with severity classification (Critical/High/Medium/Low)
- `doc-maintainer`: delivery artifact updates
- `upstream-watch`: manual documentation check
- `upstream-monitor`: automated daily monitoring (sonnet model, maxTurns=20)
- `security-auditor`: post-sprint security review (read-only)

### Skills
- `/kanban-bootstrap`: initialize .kanban/ in any project
- `/story-write`: create structured stories
- `/sprint-groom`: plan and review sprints (includes security audit step)
- `/doc-update`: update delivery artifacts
- `/dashboard`: terminal Kanban dashboard
- `/security-audit`: on-demand security scanning
- `/upstream-check`: manual upstream doc monitoring
- `/release-adapt`: process upstream changes
- `/gh-link`: link stories to GitHub Issues/PRs

### Tooling
- `dashboard.py`: colored terminal dashboard with board, features, active stories,
  sprint burndown, velocity chart, blocked story detection
- `upstream_monitor.py`: content hashing for 15 Anthropic doc pages, baseline
  management, change reports, GitHub issue body generation
- `security_audit.py`: static analysis scanner detecting secrets, injection patterns,
  weak crypto, dangerous files, unsafe StoryForge config
- GitHub Action workflow: daily upstream monitoring at 07:00 UTC
- Claude Code scheduled trigger: cloud remote agent at 07:00 UTC

### Documentation
- Architecture and system design
- Operating model (work hierarchy, Kanban states, done criteria, anti-drift rules)
- Source of truth policy (Native vs Convention vs Enforcement classification)
- Anthropic source map (every capability mapped to official docs)
- Upstream adaptation process with release watch and migration templates

### Testing
- 265 pytest tests covering templates, agents, skills, scripts, dashboard,
  upstream monitor, and security audit
- Template validation script (Bash + PowerShell)

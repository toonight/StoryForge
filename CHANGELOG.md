# Changelog

## [2.0.0] - 2026-03-29

Architecture refactoring: moved from "fat global, thin project" to "thin global, rich project".

### Architecture Change
- Global layer (`~/.claude/`) is now thin: identity CLAUDE.md (~27 lines), security deny rules, PreToolUse guardrails, 8 agents, 4 global skills
- Project layer (`.claude/`) is now rich: full delivery rules in CLAUDE.md, all hooks in settings.json, rules/ directory, 5 project skills
- Delivery hooks (SessionStart, PostToolUse, Stop, Notification) moved from global to project level
- Delivery rules moved from global CLAUDE.md to project CLAUDE.md and `.claude/rules/`

### Security Hardened
- Added cloud credential deny rules: `.aws`, `gcloud`, `.azure`, `.kube`, `.docker`, `.npmrc`, `.git-credentials`
- PreToolUse hooks block dangerous Bash commands with exit code 2: `rm -rf /`, force push, hard reset, `chmod 777`, pipe to bash
- Security audit now scans `.claude/` and `.kanban/` directories

### Skills Reorganized
- Global skills (4): `/kanban-bootstrap`, `/release-adapt`, `/security-audit`, `/upstream-check`
- Project skills (5, installed by bootstrap): `/story-write`, `/dashboard`, `/sprint-groom`, `/doc-update`, `/gh-link`

### Project Template Enriched
- `.claude/CLAUDE.md` now includes full StoryForge delivery rules (execution sequence, Kanban states, done criteria, session discipline, anti-scope-drift)
- `.claude/settings.json` now includes all hooks + PreToolUse safety + env deny rules
- Added `.claude/rules/kanban.md` for artifact format rules
- Added `.claude/rules/storyforge-delivery.md` for delivery discipline

### Scripts Updated
- `install_storyforge.sh` / `install_storyforge.ps1`: added `--migrate` flag to clean v1 artifacts
- `bootstrap_project.sh` / `bootstrap_project.ps1`: now installs skills and rules into project `.claude/`

### Documentation
- Updated architecture docs to reflect 3-layer model (global security + project delivery + local overrides)
- Updated README with v1-to-v2 migration guide

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
- 238 pytest tests covering templates, agents, skills, scripts, dashboard,
  upstream monitor, and security audit
- Template validation script (Bash + PowerShell)

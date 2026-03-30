# Changelog

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

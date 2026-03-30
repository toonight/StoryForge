# StoryForge Roadmap

## v1.0.0 - Current Release ✅

StoryForge is a structured execution framework for Claude Code.

### What's Included

**Core Framework**
- [x] Global CLAUDE.md operating system for ~/.claude/
- [x] User-level settings.json with hooks and safe permissions
- [x] Project templates (.claude/ + .kanban/)
- [x] Story template with dependencies and GitHub fields
- [x] Install script (Bash + PowerShell)
- [x] Bootstrap script (Bash + PowerShell)

**Agents (8)**
- [x] portfolio-orchestrator (top-level coordinator with decision tree)
- [x] planner (story creation with good/bad examples)
- [x] implementer (scope-bounded execution with checklist)
- [x] reviewer (quality review with severity classification)
- [x] doc-maintainer (artifact updates)
- [x] upstream-watch (manual doc check)
- [x] upstream-monitor (automated daily monitoring)
- [x] security-auditor (post-sprint security review)

**Skills (9)**
- [x] /kanban-bootstrap, /story-write, /sprint-groom, /doc-update
- [x] /dashboard, /security-audit, /upstream-check, /release-adapt, /gh-link

**Tooling**
- [x] Kanban dashboard (Python, terminal, colored output)
- [x] Upstream monitor (content hashing, GitHub Action cron, cloud trigger)
- [x] Security audit scanner (static analysis, secret detection)
- [x] Velocity tracking and dependency detection in dashboard
- [x] 238 tests

**Documentation**
- [x] Architecture, operating model, source of truth policy
- [x] Anthropic source map (every capability classified)
- [x] Upstream adaptation process

---

## Future Considerations

These are not committed. They would be planned as new Initiatives only if
real-world usage demonstrates the need.

- Real-world validation across multiple projects
- Multi-project portfolio dashboard
- Release management workflow
- Sprint retrospective skill
- Enterprise deployment guide

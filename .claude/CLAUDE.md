# StoryForge Project Instructions

This is the StoryForge repository itself. When working here, you are building
and maintaining the framework, not using it on a downstream project.

## Architecture

StoryForge v2 uses a "thin global, rich project" model:
- `templates/home/` - Global layer (~/.claude/): identity, security, 8 agents, 4 global skills
- `templates/project/` - Project layer (.claude/): delivery rules, hooks, 5 project skills, rules

The repo also contains:
- `docs/` - Architecture, operating model, source of truth policy, upstream tracking
- `scripts/` - Install, bootstrap, validation, upstream sync
- `tests/` - Python pytest suite (238+ tests)
- `examples/` - Sample project demonstrating the framework

## Key Rules

1. Anthropic official docs are the ONLY source of truth for Claude Code behavior
2. Never present a StoryForge convention as a native Claude Code feature
3. Every capability must be classified in docs/anthropic-source-map.md as:
   Native, Convention, or Enforcement
4. All repo artifacts are in English
5. Global CLAUDE.md must stay thin (~27 lines); delivery rules belong in project templates

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run template validation
bash scripts/validate_templates.sh
```

## Conventions

- Agent files: YAML frontmatter + markdown body, lowercase-hyphenated names
- Skill files: SKILL.md in named directory, YAML frontmatter
- Scripts: Bash with `set -euo pipefail`, shebang line
- Kanban: Markdown files in .kanban/, sequential IDs (STORY-NNN, DECISION-NNN)
- All JSON must be valid (tested)
- Templates use `{{PROJECT_NAME}}` placeholder for project name substitution

## Important Paths

- `templates/home/.claude/agents/` - Agent definitions (8 agents)
- `templates/home/.claude/skills/` - Global skill definitions (4 skills)
- `templates/home/.claude/settings.json` - Global settings (security deny rules + guardrails)
- `templates/project/.claude/skills/` - Project skill definitions (5 skills)
- `templates/project/.claude/settings.json` - Project settings (hooks + deny rules)
- `templates/project/.claude/rules/` - Project rules (kanban.md, storyforge-delivery.md)
- `templates/project/.kanban/stories/STORY-TEMPLATE.md` - Story template
- `docs/anthropic-source-map.md` - Capability classification
- `docs/upstream/doc-index.md` - Anthropic doc verification dates

---
paths:
  - "templates/**/*"
---

# Template Editing Rules

When editing files under templates/:

- templates/home/ files will be installed to ~/.claude/ - test them as if they
  run in that context
- templates/project/ files use {{PROJECT_NAME}} placeholders - do not hardcode
  project names
- Agent files must have YAML frontmatter with name, description fields
- Skill files must be named SKILL.md inside a named directory
- settings.json must be valid JSON - run tests after editing
- CLAUDE.md templates should stay under 200 lines for adherence
- Never add unsupported frontmatter fields - verify in docs/upstream/doc-index.md

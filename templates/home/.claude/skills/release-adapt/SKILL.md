---
name: release-adapt
description: Process an Anthropic Claude Code release or documentation change and determine its impact on StoryForge. Use when a new Claude Code version is released or docs change.
argument-hint: "release-version-or-url"
disable-model-invocation: true
---

# Release Adaptation

Process an Anthropic Claude Code update and determine its impact on StoryForge.

## Instructions

1. Identify the release or change to evaluate:
   - If $ARGUMENTS contains a version number or URL, use that
   - Otherwise, ask the user what changed

2. Use the `upstream-watch` agent to check the relevant documentation pages

3. For each change found, classify the impact:

| Impact Level | Meaning | Action Required |
|---|---|---|
| No Impact | Change doesn't affect StoryForge | Update doc-index.md verified date |
| Docs Impact | Documentation needs updating | Update relevant StoryForge docs |
| Config Impact | Settings or configuration affected | Update settings.json templates |
| Agent Impact | Agent behavior or format affected | Update agent definitions |
| Hook Impact | Hook events or format changed | Update hook configurations |
| Skill Impact | Skill format or behavior changed | Update skill definitions |
| Migration Required | Breaking change needs migration | Create migration Story |

4. For each impacted area, create a record:

```markdown
## Upstream Change: (Description)

- Source: (URL or release notes reference)
- Checked: (Today's date)
- Impact: (Classification from table)
- Impacted Files: (List of StoryForge files affected)
- Migration Notes: (What needs to change)
- Validation: (How to verify the adaptation)
- Status: Pending | In Progress | Complete
```

5. Save the record to `docs/upstream/` or update `docs/upstream/release-watch.md`

6. If migration is required:
   - Create a Story using the `story-write` skill
   - Link it to an appropriate Feature (or create FEAT for upstream adaptation)
   - Add it to the sprint backlog if urgent

7. Update `docs/upstream/doc-index.md` with new verification dates

8. Update `docs/anthropic-source-map.md` if capability classifications changed

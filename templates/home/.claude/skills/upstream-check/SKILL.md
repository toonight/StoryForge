---
name: upstream-check
description: Run the StoryForge upstream documentation monitor to check for Anthropic doc changes. Use daily or when you suspect Claude Code has been updated.
disable-model-invocation: true
---

# Upstream Documentation Check

Check Anthropic Claude Code documentation for changes that may affect StoryForge.

## Instructions

1. Run the upstream monitor script:

```bash
python scripts/upstream_monitor.py
```

2. If changes are detected:
   - Review the changed pages manually
   - Classify each change using the impact table from `docs/upstream/release-watch.md`
   - For each impactful change, use `/story-write` to create an adaptation Story
   - After adapting, update the baseline:

```bash
python scripts/upstream_monitor.py --update-baseline
```

3. If generating a full report:

```bash
python scripts/upstream_monitor.py --report-path docs/upstream/reports
```

4. Update `docs/upstream/release-watch.md` with findings
5. Update `docs/upstream/doc-index.md` verification dates

## Impact Classification

| Level | Meaning | Action |
|---|---|---|
| No Impact | Cosmetic or unrelated change | Update baseline only |
| Docs Impact | StoryForge docs need updating | Update docs |
| Config Impact | Settings or configuration affected | Update templates |
| Agent Impact | Agent behavior or format changed | Update agents |
| Hook Impact | Hook events or format changed | Update hooks |
| Skill Impact | Skill format changed | Update skills |
| Migration Required | Breaking change | Create migration Story |

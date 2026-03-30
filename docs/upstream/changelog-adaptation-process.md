# Changelog Adaptation Process

This document describes how StoryForge adapts to Anthropic Claude Code changes.

## Principle

Anthropic is treated as the upstream specification. StoryForge must adapt to
upstream changes, not the other way around.

## Process

### Step 1: Detection

Detect upstream changes via one of:
- Claude Code release notes or changelog
- Documentation page changes
- Community announcements from Anthropic
- The `upstream-watch` agent
- The `/release-adapt` skill

### Step 2: Triage

For each change, determine:

1. **What changed?** - Describe the change concisely
2. **Impact level** - Use the classification from `release-watch.md`
3. **Urgency** - Is this blocking? Can it wait?
4. **Scope** - Which StoryForge files are affected?

### Step 3: Record

Create a record in `release-watch.md`:

```markdown
### [Version or Date]: Change Description

- Source: URL to release notes or docs
- Checked: YYYY-MM-DD
- Impact: Classification
- Urgency: High / Medium / Low
- Affected files:
  - path/to/file1
  - path/to/file2
- Migration notes: What needs to change
- Status: Pending | In Progress | Complete
```

### Step 4: Plan

If migration is required:

1. Create a Story using `/story-write`
2. Link it to a Feature (create one for upstream adaptation if needed)
3. Define acceptance criteria based on the change
4. Add to sprint if urgent

### Step 5: Execute

1. Implement the adaptation
2. Update `docs/anthropic-source-map.md` if capability classifications changed
3. Update `docs/upstream/doc-index.md` with new verification dates
4. Test the adaptation

### Step 6: Verify

1. Verify the adaptation works with the new Claude Code version
2. Update the record status to "Complete"
3. Update the StoryForge CHANGELOG.md

## Migration Template

For significant migrations, create a file in `docs/migrations/`:

```markdown
# Migration: [Description]

- Date: YYYY-MM-DD
- Upstream Change: [What changed in Claude Code]
- Source: [URL]
- StoryForge Version: [Version that includes this migration]

## What Changed

Description of the upstream change and why it matters.

## Impact on StoryForge

List of affected components and how they're affected.

## Migration Steps

1. Step-by-step instructions for users to update
2. Include file paths and what to change

## Rollback

How to revert if the migration causes issues.

## Validation

How to verify the migration was successful.
```

## Responsibility

The `upstream-watch` agent and `/release-adapt` skill support this process,
but a human should review and approve all adaptations before they are applied.

# Source of Truth Policy

This document defines the authority hierarchy for StoryForge design decisions.

## Authority Levels

### Level 1: Anthropic Official Documentation (Highest Authority)

The official Claude Code documentation is the only authoritative source for:
- What Claude Code natively supports
- How features are configured
- What fields, flags, and options exist
- How settings, hooks, agents, skills, and CLAUDE.md behave

**Rule**: If Anthropic docs say a feature works a certain way, StoryForge must comply.

### Level 2: StoryForge Architecture Decisions

StoryForge may define conventions, workflows, and patterns that are layered on top of
native Claude Code capabilities. These are documented in:
- `docs/architecture.md`
- `docs/operating-model.md`
- `docs/decisions/`
- `docs/anthropic-source-map.md`

**Rule**: Every StoryForge convention must be explicitly labeled as such and must not
conflict with or misrepresent Anthropic native behavior.

### Level 3: Project-Level Customization

Individual projects using StoryForge may customize:
- Project CLAUDE.md content
- Project settings.json
- Project-level agents and skills
- Kanban artifact content

**Rule**: Project customizations must not violate StoryForge conventions or
Anthropic native behavior.

## Classification System

Every StoryForge capability falls into one of three categories:

### A. Anthropic Native Capability

- Directly supported by official Claude Code documentation
- Configured using documented fields, flags, or patterns
- Behavior guaranteed by the Claude Code runtime

**Examples**: CLAUDE.md loading, settings.json permissions, hook lifecycle events,
agent frontmatter fields

### B. StoryForge Convention

- A pattern or workflow defined by StoryForge
- Layered on top of native capabilities
- Relies on Claude reading and following CLAUDE.md guidance (contextual, not enforced)
- Behavior is best-effort, not guaranteed by runtime

**Examples**: Kanban board structure, Initiative/Feature/Story hierarchy,
agile workflow rules, story templates

### C. StoryForge Enforcement Layer

- Uses native enforcement mechanisms to guarantee behavior
- Implemented via settings.json permissions, hooks, or sandbox rules
- Behavior is deterministic and always fires (for hooks) or always blocks (for deny rules)

**Examples**: Hook-based session discipline, permission deny rules for sensitive paths,
pre-tool-use validation scripts

## Key Principle

> CLAUDE.md guidance is contextual. Settings and permissions are enforcement-oriented.
> Hooks are lifecycle automation. Kanban discipline is a StoryForge operating convention.
>
> Do not blur these categories.

## Verification Process

Before implementing any StoryForge feature:
1. Check `docs/upstream/doc-index.md` for the relevant Anthropic documentation
2. Verify the feature is still supported as documented
3. Classify the implementation as Native, Convention, or Enforcement
4. Record the classification in `docs/anthropic-source-map.md`
5. If the feature is a Convention, clearly label it in all artifacts

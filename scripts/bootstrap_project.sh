#!/usr/bin/env bash
# bootstrap_project.sh
# Bootstrap a project with StoryForge project-level structure.
#
# v2 architecture: installs delivery hooks, project skills, rules,
# and Kanban artifacts. Run this from the project root.
#
# Usage: ./bootstrap_project.sh [project-name]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORYFORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$STORYFORGE_ROOT/templates/project"
PROJECT_DIR="$(pwd)"
PROJECT_NAME="${1:-$(basename "$PROJECT_DIR")}"
# Escape sed metacharacters in project name to prevent injection
PROJECT_NAME_SED=$(printf '%s\n' "$PROJECT_NAME" | sed 's/[&/\]/\\&/g')

echo "=== StoryForge Project Bootstrap ==="
echo ""
echo "Project:   $PROJECT_NAME"
echo "Directory: $PROJECT_DIR"
echo "Templates: $TEMPLATE_DIR"
echo ""

# Check we're not in the StoryForge repo itself
if [ "$PROJECT_DIR" = "$STORYFORGE_ROOT" ]; then
    echo "ERROR: Do not bootstrap the StoryForge repository itself."
    echo "Run this script from the project you want to set up."
    exit 1
fi

# Check template exists
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "ERROR: Template directory not found: $TEMPLATE_DIR"
    exit 1
fi

# Check if already bootstrapped
if [ -d "$PROJECT_DIR/.kanban" ]; then
    echo "WARNING: This project already has a .kanban/ directory."
    echo "Skipping Kanban setup to avoid overwriting existing artifacts."
    SKIP_KANBAN=true
else
    SKIP_KANBAN=false
fi

# Create .claude/ structure
echo "Setting up .claude/ ..."
mkdir -p "$PROJECT_DIR/.claude"

if [ ! -f "$PROJECT_DIR/.claude/CLAUDE.md" ]; then
    sed "s/{{PROJECT_NAME}}/$PROJECT_NAME_SED/g" \
        "$TEMPLATE_DIR/.claude/CLAUDE.md" > "$PROJECT_DIR/.claude/CLAUDE.md"
    echo "  CREATED: .claude/CLAUDE.md"
else
    echo "  EXISTS:  .claude/CLAUDE.md (skipped)"
fi

if [ ! -f "$PROJECT_DIR/.claude/settings.json" ]; then
    cp "$TEMPLATE_DIR/.claude/settings.json" "$PROJECT_DIR/.claude/settings.json"
    echo "  CREATED: .claude/settings.json"
else
    echo "  EXISTS:  .claude/settings.json (skipped)"
fi

# Create .claude/rules/ if template has them
RULES_SRC="$TEMPLATE_DIR/.claude/rules"
if [ -d "$RULES_SRC" ]; then
    RULES_DEST="$PROJECT_DIR/.claude/rules"
    mkdir -p "$RULES_DEST"
    for rule_file in "$RULES_SRC"/*.md; do
        if [ -f "$rule_file" ]; then
            rule_name=$(basename "$rule_file")
            if [ ! -f "$RULES_DEST/$rule_name" ]; then
                cp "$rule_file" "$RULES_DEST/$rule_name"
                echo "  CREATED: .claude/rules/$rule_name"
            fi
        fi
    done
fi

# Install project-level skills
SKILLS_SRC="$TEMPLATE_DIR/.claude/skills"
if [ -d "$SKILLS_SRC" ]; then
    echo ""
    echo "Installing project skills..."
    SKILLS_DEST="$PROJECT_DIR/.claude/skills"
    mkdir -p "$SKILLS_DEST"
    for skill_dir in "$SKILLS_SRC"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            skill_dest="$SKILLS_DEST/$skill_name"
            if [ ! -d "$skill_dest" ]; then
                mkdir -p "$skill_dest"
                for skill_file in "$skill_dir"*; do
                    if [ -f "$skill_file" ]; then
                        cp "$skill_file" "$skill_dest/"
                    fi
                done
                echo "  CREATED: .claude/skills/$skill_name/"
            else
                echo "  EXISTS:  .claude/skills/$skill_name/ (skipped)"
            fi
        fi
    done
fi

# Create .kanban/ structure
if [ "$SKIP_KANBAN" = false ]; then
    echo ""
    echo "Setting up .kanban/ ..."
    mkdir -p "$PROJECT_DIR/.kanban/stories"
    mkdir -p "$PROJECT_DIR/.kanban/features"

    for template_file in board.md backlog.md sprint.md decisions.md changelog.md; do
        sed "s/{{PROJECT_NAME}}/$PROJECT_NAME_SED/g" \
            "$TEMPLATE_DIR/.kanban/$template_file" > "$PROJECT_DIR/.kanban/$template_file"
        echo "  CREATED: .kanban/$template_file"
    done

    # Copy story template
    cp "$TEMPLATE_DIR/.kanban/stories/STORY-TEMPLATE.md" \
        "$PROJECT_DIR/.kanban/stories/STORY-TEMPLATE.md"
    echo "  CREATED: .kanban/stories/STORY-TEMPLATE.md"

    # Copy feature template
    cp "$TEMPLATE_DIR/.kanban/features/FEAT-TEMPLATE.md" \
        "$PROJECT_DIR/.kanban/features/FEAT-TEMPLATE.md"
    echo "  CREATED: .kanban/features/FEAT-TEMPLATE.md"

    # Create .gitkeep
    touch "$PROJECT_DIR/.kanban/stories/.gitkeep"
    touch "$PROJECT_DIR/.kanban/features/.gitkeep"
fi

# Add to .gitignore if it exists
if [ -f "$PROJECT_DIR/.gitignore" ]; then
    if ! grep -q ".claude/settings.local.json" "$PROJECT_DIR/.gitignore" 2>/dev/null; then
        echo "" >> "$PROJECT_DIR/.gitignore"
        echo "# Claude Code local settings" >> "$PROJECT_DIR/.gitignore"
        echo ".claude/settings.local.json" >> "$PROJECT_DIR/.gitignore"
        echo ".claude/agent-memory-local/" >> "$PROJECT_DIR/.gitignore"
        echo ".claude/worktrees/" >> "$PROJECT_DIR/.gitignore"
        echo "  UPDATED: .gitignore (added Claude Code local entries)"
    fi
fi

echo ""
echo "=== Bootstrap Complete ==="
echo ""
echo "Created:"
echo "  .claude/CLAUDE.md         - Project instructions + delivery rules (customize this)"
echo "  .claude/settings.json     - Hooks, permissions, and PreToolUse guardrails"
echo "  .claude/rules/            - Delivery discipline and Kanban format rules"
echo "  .claude/skills/           - Project skills (story-write, dashboard, sprint-groom, etc.)"
if [ "$SKIP_KANBAN" = false ]; then
    echo "  .kanban/board.md          - Kanban board"
    echo "  .kanban/backlog.md        - Backlog"
    echo "  .kanban/sprint.md         - Sprint planning"
    echo "  .kanban/decisions.md      - Decision records"
    echo "  .kanban/changelog.md      - Delivery changelog"
    echo "  .kanban/stories/          - Story files"
    echo "  .kanban/features/         - Feature files"
fi
echo ""
echo "Next steps:"
echo "  1. Edit .claude/CLAUDE.md with project-specific architecture and conventions"
echo "  2. Define your first Initiative in .kanban/backlog.md"
echo "  3. Create your first Story with /story-write"
echo "  4. Start working!"
echo ""

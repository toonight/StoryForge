#!/usr/bin/env bash
# install_storyforge.sh
# Install StoryForge user-level configuration to ~/.claude/
#
# v2 architecture: thin global layer with security + universal agents/skills.
# Delivery hooks, project skills, and rules are installed per-project
# by bootstrap_project.sh.
#
# Usage: ./scripts/install_storyforge.sh [--force] [--migrate]
#   --force    Replace existing files (default: backup and append)
#   --migrate  Clean up v1 artifacts (project skills, delivery rule from global)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORYFORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$STORYFORGE_ROOT/templates/home/.claude"
TARGET_DIR="$HOME/.claude"
BACKUP_DIR="$TARGET_DIR/backups/storyforge-$(date +%Y%m%d-%H%M%S)"
FORCE=""
MIGRATE=""

for arg in "$@"; do
    case "$arg" in
        --force) FORCE="true" ;;
        --migrate) MIGRATE="true" ;;
    esac
done

echo "=== StoryForge Installer (v2) ==="
echo ""
echo "Source:  $TEMPLATE_DIR"
echo "Target:  $TARGET_DIR"
echo ""

# Check source exists
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "ERROR: Template directory not found: $TEMPLATE_DIR"
    exit 1
fi

# Create target if it doesn't exist
mkdir -p "$TARGET_DIR"

# Function to install a file with backup
install_file() {
    local src="$1"
    local relative="${src#$TEMPLATE_DIR/}"
    local dest="$TARGET_DIR/$relative"
    local dest_dir
    dest_dir="$(dirname "$dest")"

    mkdir -p "$dest_dir"

    if [ -f "$dest" ]; then
        if [ "$FORCE" != "true" ]; then
            echo "  EXISTS: $relative"
            echo "    Backing up to: $BACKUP_DIR/$relative"
            mkdir -p "$(dirname "$BACKUP_DIR/$relative")"
            cp "$dest" "$BACKUP_DIR/$relative"
        fi
    fi

    cp "$src" "$dest"
    echo "  INSTALLED: $relative"
}

# v1 -> v2 migration: remove project-specific artifacts from global
if [ "$MIGRATE" = "true" ]; then
    echo "Migrating v1 -> v2 (cleaning global)..."
    for skill in story-write dashboard sprint-groom doc-update gh-link; do
        if [ -d "$TARGET_DIR/skills/$skill" ]; then
            echo "  REMOVING: skills/$skill (now project-level)"
            rm -rf "$TARGET_DIR/skills/$skill"
        fi
    done
    if [ -f "$TARGET_DIR/rules/storyforge-delivery.md" ]; then
        echo "  REMOVING: rules/storyforge-delivery.md (now project-level)"
        rm -f "$TARGET_DIR/rules/storyforge-delivery.md"
    fi
    echo ""
fi

# Install CLAUDE.md
echo "Installing CLAUDE.md..."
if [ -f "$TARGET_DIR/CLAUDE.md" ]; then
    if [ -s "$TARGET_DIR/CLAUDE.md" ]; then
        echo "  WARNING: Existing CLAUDE.md has content."
        if [ "$FORCE" != "true" ]; then
            echo "  The StoryForge CLAUDE.md will be APPENDED to your existing file."
            echo "  Use --force to replace instead."
            mkdir -p "$BACKUP_DIR"
            cp "$TARGET_DIR/CLAUDE.md" "$BACKUP_DIR/CLAUDE.md"
            echo "" >> "$TARGET_DIR/CLAUDE.md"
            echo "" >> "$TARGET_DIR/CLAUDE.md"
            cat "$TEMPLATE_DIR/CLAUDE.md" >> "$TARGET_DIR/CLAUDE.md"
            echo "  APPENDED: CLAUDE.md"
        else
            install_file "$TEMPLATE_DIR/CLAUDE.md"
        fi
    else
        install_file "$TEMPLATE_DIR/CLAUDE.md"
    fi
else
    install_file "$TEMPLATE_DIR/CLAUDE.md"
fi

# Install settings.json
echo ""
echo "Installing settings.json..."
if [ -f "$TARGET_DIR/settings.json" ]; then
    echo "  WARNING: Existing settings.json found."
    echo "  StoryForge settings template saved as settings.storyforge.json"
    echo "  You should manually merge the StoryForge deny rules and PreToolUse hooks."
    cp "$TEMPLATE_DIR/settings.json" "$TARGET_DIR/settings.storyforge.json"
    echo "  SAVED: settings.storyforge.json (merge manually)"
else
    install_file "$TEMPLATE_DIR/settings.json"
fi

# Install agents
echo ""
echo "Installing agents..."
for agent_file in "$TEMPLATE_DIR"/agents/*.md; do
    if [ -f "$agent_file" ]; then
        install_file "$agent_file"
    fi
done

# Install skills (global only: kanban-bootstrap, release-adapt, security-audit, upstream-check)
echo ""
echo "Installing global skills..."
for skill_dir in "$TEMPLATE_DIR"/skills/*/; do
    if [ -d "$skill_dir" ]; then
        for skill_file in "$skill_dir"*; do
            if [ -f "$skill_file" ]; then
                install_file "$skill_file"
            fi
        done
    fi
done

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Installed (thin global layer):"
echo "  - CLAUDE.md (identity + anti-drift rules)"
echo "  - settings.json (security deny rules + PreToolUse guardrails)"
echo "  - agents/ (8 universal agents)"
echo "  - skills/ (4 global: kanban-bootstrap, release-adapt, security-audit, upstream-check)"
echo ""
echo "Next steps:"
echo "  1. If settings.storyforge.json was created, merge it into your settings.json"
echo "  2. Run bootstrap_project.sh in each project to install delivery hooks + skills"
echo "  3. Use /kanban-bootstrap in a project to set up delivery tracking"
echo ""
echo "Note: Delivery hooks, project skills (story-write, dashboard, sprint-groom,"
echo "  doc-update, gh-link), and delivery rules are now project-level."
echo "  Run with --migrate to clean up v1 global artifacts."
echo ""

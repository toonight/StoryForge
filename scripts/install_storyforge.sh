#!/usr/bin/env bash
# install_storyforge.sh
# Install StoryForge user-level configuration to ~/.claude/
#
# This script copies StoryForge templates to the user's home Claude config.
# It backs up existing files before overwriting.
#
# Usage: ./scripts/install_storyforge.sh [--force]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORYFORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE_DIR="$STORYFORGE_ROOT/templates/home/.claude"
TARGET_DIR="$HOME/.claude"
BACKUP_DIR="$TARGET_DIR/backups/storyforge-$(date +%Y%m%d-%H%M%S)"
FORCE="${1:-}"

echo "=== StoryForge Installer ==="
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
        if [ "$FORCE" != "--force" ]; then
            echo "  EXISTS: $relative"
            echo "    Backing up to: $BACKUP_DIR/$relative"
            mkdir -p "$(dirname "$BACKUP_DIR/$relative")"
            cp "$dest" "$BACKUP_DIR/$relative"
        fi
    fi

    cp "$src" "$dest"
    echo "  INSTALLED: $relative"
}

# Install CLAUDE.md
echo "Installing CLAUDE.md..."
if [ -f "$TARGET_DIR/CLAUDE.md" ]; then
    # Check if existing CLAUDE.md has content
    if [ -s "$TARGET_DIR/CLAUDE.md" ]; then
        echo "  WARNING: Existing CLAUDE.md has content."
        if [ "$FORCE" != "--force" ]; then
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
    echo "  You should manually merge the StoryForge hooks and permissions."
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

# Install skills
echo ""
echo "Installing skills..."
for skill_dir in "$TEMPLATE_DIR"/skills/*/; do
    if [ -d "$skill_dir" ]; then
        for skill_file in "$skill_dir"*; do
            if [ -f "$skill_file" ]; then
                install_file "$skill_file"
            fi
        done
    fi
done

# Install rules
echo ""
echo "Installing rules..."
if [ -d "$TEMPLATE_DIR/rules" ]; then
    for rule_file in "$TEMPLATE_DIR"/rules/*.md; do
        if [ -f "$rule_file" ]; then
            install_file "$rule_file"
        fi
    done
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Installed components:"
echo "  - CLAUDE.md (global operating system)"
echo "  - settings.json (or settings.storyforge.json for manual merge)"
echo "  - agents/ (8 agents: orchestrator, planner, implementer, reviewer, etc.)"
echo "  - skills/ (9 skills: kanban-bootstrap, story-write, dashboard, security-audit, etc.)"
echo "  - rules/ (delivery rules for .kanban/ artifacts)"
echo ""
echo "Next steps:"
echo "  1. If settings.storyforge.json was created, merge it into your settings.json"
echo "  2. Start a new Claude Code session to load the StoryForge operating system"
echo "  3. Use /kanban-bootstrap in a project to set up delivery tracking"
echo ""

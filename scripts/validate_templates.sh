#!/usr/bin/env bash
# validate_templates.sh
# Validate that StoryForge templates are complete and well-formed.
#
# Usage: ./scripts/validate_templates.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORYFORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ERRORS=0
WARNINGS=0

echo "=== StoryForge Template Validation ==="
echo ""

# Helper: check file exists
check_file() {
    local file="$1"
    local description="$2"
    if [ -f "$STORYFORGE_ROOT/$file" ]; then
        echo "  OK: $file"
    else
        echo "  MISSING: $file ($description)"
        ERRORS=$((ERRORS + 1))
    fi
}

# Helper: check directory exists
check_dir() {
    local dir="$1"
    local description="$2"
    if [ -d "$STORYFORGE_ROOT/$dir" ]; then
        echo "  OK: $dir/"
    else
        echo "  MISSING: $dir/ ($description)"
        ERRORS=$((ERRORS + 1))
    fi
}

# Helper: check file contains string
check_contains() {
    local file="$1"
    local pattern="$2"
    local description="$3"
    if [ -f "$STORYFORGE_ROOT/$file" ]; then
        if grep -q "$pattern" "$STORYFORGE_ROOT/$file"; then
            echo "  OK: $file contains '$pattern'"
        else
            echo "  WARNING: $file missing expected content: $description"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
}

# Validate repo root files
echo "Checking repository root..."
check_file "README.md" "Repository readme"
check_file "LICENSE" "License file"
check_file ".gitignore" "Git ignore rules"
check_file "CHANGELOG.md" "Change log"
check_file "ROADMAP.md" "Roadmap"

# Validate docs
echo ""
echo "Checking documentation..."
check_file "docs/architecture.md" "Architecture documentation"
check_file "docs/operating-model.md" "Operating model documentation"
check_file "docs/source-of-truth-policy.md" "Source of truth policy"
check_file "docs/anthropic-source-map.md" "Anthropic source map"
check_file "docs/upstream/doc-index.md" "Documentation index"

# Validate home templates
echo ""
echo "Checking user-level templates..."
check_file "templates/home/.claude/CLAUDE.md" "Global CLAUDE.md"
check_file "templates/home/.claude/settings.json" "Global settings"
check_dir "templates/home/.claude/agents" "Agent definitions"
check_file "templates/home/.claude/agents/portfolio-orchestrator.md" "Main orchestrator"
check_file "templates/home/.claude/agents/planner.md" "Planner agent"
check_file "templates/home/.claude/agents/implementer.md" "Implementer agent"
check_file "templates/home/.claude/agents/reviewer.md" "Reviewer agent"
check_file "templates/home/.claude/agents/doc-maintainer.md" "Doc maintainer agent"
check_file "templates/home/.claude/agents/upstream-watch.md" "Upstream watch agent"
check_dir "templates/home/.claude/skills" "Skill definitions"
check_file "templates/home/.claude/skills/kanban-bootstrap/SKILL.md" "Kanban bootstrap skill"
check_file "templates/home/.claude/skills/release-adapt/SKILL.md" "Release adapt skill"
check_file "templates/home/.claude/skills/upstream-check/SKILL.md" "Upstream check skill"
check_file "templates/home/.claude/skills/security-audit/SKILL.md" "Security audit skill"

# Validate rules
echo ""
echo "Checking rules files..."
check_file "templates/project/.claude/rules/storyforge-delivery.md" "Project delivery rules"
check_file "templates/project/.claude/rules/kanban.md" "Project kanban rules"
check_file ".claude/CLAUDE.md" "StoryForge project CLAUDE.md"
check_file ".claude/rules/templates.md" "StoryForge templates rule"
check_file ".claude/rules/docs.md" "StoryForge docs rule"
check_file ".claude/rules/scripts.md" "StoryForge scripts rule"

# Validate agent frontmatter
echo ""
echo "Checking agent frontmatter..."
for agent_file in "$STORYFORGE_ROOT"/templates/home/.claude/agents/*.md; do
    if [ -f "$agent_file" ]; then
        agent_name=$(basename "$agent_file" .md)
        if head -1 "$agent_file" | grep -q "^---$"; then
            echo "  OK: $agent_name has frontmatter"
        else
            echo "  ERROR: $agent_name missing YAML frontmatter"
            ERRORS=$((ERRORS + 1))
        fi
        if grep -q "^name:" "$agent_file"; then
            echo "  OK: $agent_name has name field"
        else
            echo "  ERROR: $agent_name missing name field"
            ERRORS=$((ERRORS + 1))
        fi
        if grep -q "^description:" "$agent_file"; then
            echo "  OK: $agent_name has description field"
        else
            echo "  ERROR: $agent_name missing description field"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

# Validate skill frontmatter
echo ""
echo "Checking skill frontmatter..."
for skill_file in "$STORYFORGE_ROOT"/templates/home/.claude/skills/*/SKILL.md; do
    if [ -f "$skill_file" ]; then
        skill_dir=$(basename "$(dirname "$skill_file")")
        if head -1 "$skill_file" | grep -q "^---$"; then
            echo "  OK: $skill_dir has frontmatter"
        else
            echo "  ERROR: $skill_dir missing YAML frontmatter"
            ERRORS=$((ERRORS + 1))
        fi
        if grep -q "^name:" "$skill_file"; then
            echo "  OK: $skill_dir has name field"
        else
            echo "  ERROR: $skill_dir missing name field"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

# Validate project-level skills
echo ""
echo "Checking project-level skills..."
check_file "templates/project/.claude/skills/story-write/SKILL.md" "Story write skill"
check_file "templates/project/.claude/skills/sprint-groom/SKILL.md" "Sprint groom skill"
check_file "templates/project/.claude/skills/doc-update/SKILL.md" "Doc update skill"
check_file "templates/project/.claude/skills/dashboard/SKILL.md" "Dashboard skill"
check_file "templates/project/.claude/skills/gh-link/SKILL.md" "GitHub link skill"

# Validate project-level skill frontmatter
echo ""
echo "Checking project-level skill frontmatter..."
for skill_file in "$STORYFORGE_ROOT"/templates/project/.claude/skills/*/SKILL.md; do
    if [ -f "$skill_file" ]; then
        skill_dir=$(basename "$(dirname "$skill_file")")
        if head -1 "$skill_file" | grep -q "^---$"; then
            echo "  OK: $skill_dir has frontmatter"
        else
            echo "  ERROR: $skill_dir missing YAML frontmatter"
            ERRORS=$((ERRORS + 1))
        fi
        if grep -q "^name:" "$skill_file"; then
            echo "  OK: $skill_dir has name field"
        else
            echo "  ERROR: $skill_dir missing name field"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

# Validate project templates
echo ""
echo "Checking project-level templates..."
check_file "templates/project/.claude/CLAUDE.md" "Project CLAUDE.md"
check_file "templates/project/.claude/settings.json" "Project settings"
check_file "templates/project/.kanban/board.md" "Board template"
check_file "templates/project/.kanban/backlog.md" "Backlog template"
check_file "templates/project/.kanban/sprint.md" "Sprint template"
check_file "templates/project/.kanban/decisions.md" "Decisions template"
check_file "templates/project/.kanban/changelog.md" "Changelog template"
check_file "templates/project/.kanban/stories/STORY-TEMPLATE.md" "Story template"
check_dir "templates/project/.kanban/features" "Feature files directory"
check_file "templates/project/.kanban/features/FEAT-TEMPLATE.md" "Feature template"

# Validate JSON files
echo ""
echo "Checking JSON validity..."
for json_file in \
    "templates/home/.claude/settings.json" \
    "templates/project/.claude/settings.json"; do
    if [ -f "$STORYFORGE_ROOT/$json_file" ]; then
        if python3 -c "import json, sys; json.load(open(sys.argv[1]))" "$STORYFORGE_ROOT/$json_file" 2>/dev/null || \
           python -c "import json, sys; json.load(open(sys.argv[1]))" "$STORYFORGE_ROOT/$json_file" 2>/dev/null; then
            echo "  OK: $json_file is valid JSON"
        else
            echo "  ERROR: $json_file is invalid JSON"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

# Validate scripts are executable (on Unix-like systems)
echo ""
echo "Checking scripts..."
check_file "scripts/install_storyforge.sh" "Install script"
check_file "scripts/bootstrap_project.sh" "Bootstrap script"
check_file "scripts/validate_templates.sh" "Validation script"

# Summary
echo ""
echo "=== Validation Summary ==="
echo "  Errors:   $ERRORS"
echo "  Warnings: $WARNINGS"
echo ""

if [ "$ERRORS" -gt 0 ]; then
    echo "FAILED: $ERRORS error(s) found. Fix before releasing."
    exit 1
else
    echo "PASSED: All checks passed."
    exit 0
fi

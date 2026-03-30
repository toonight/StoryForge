#!/usr/bin/env bash
# sync_upstream_docs.sh
# Check Anthropic Claude Code documentation pages for availability.
#
# This script verifies that all documented URLs in doc-index.md are reachable
# and updates the verification dates. It does NOT diff content (that requires
# the upstream-watch agent for semantic analysis).
#
# Usage: ./scripts/sync_upstream_docs.sh [--update]
#
# Options:
#   --update    Update doc-index.md verification dates for reachable pages

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORYFORGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOC_INDEX="$STORYFORGE_ROOT/docs/upstream/doc-index.md"
UPDATE="${1:-}"
TODAY=$(date +%Y-%m-%d)

echo "=== StoryForge Upstream Documentation Sync ==="
echo ""
echo "Date: $TODAY"
echo ""

if [ ! -f "$DOC_INDEX" ]; then
    echo "ERROR: doc-index.md not found at $DOC_INDEX"
    exit 1
fi

# Documentation URLs to check (from doc-index.md)
DOCS=(
    "Memory & CLAUDE.md|https://code.claude.com/docs/en/memory"
    "Subagents|https://code.claude.com/docs/en/sub-agents"
    "Hooks|https://code.claude.com/docs/en/hooks"
    "Skills|https://code.claude.com/docs/en/skills"
    "Settings|https://code.claude.com/docs/en/settings"
    "CLI Reference|https://code.claude.com/docs/en/cli-reference"
    "Permission Modes|https://code.claude.com/docs/en/permission-modes"
    "Permissions|https://code.claude.com/docs/en/permissions"
    "Common Workflows|https://code.claude.com/docs/en/common-workflows"
    "Best Practices|https://code.claude.com/docs/en/best-practices"
    "Headless Mode|https://code.claude.com/docs/en/headless"
    "GitHub Actions|https://code.claude.com/docs/en/github-actions"
    "Agent Teams|https://code.claude.com/docs/en/agent-teams"
    "MCP|https://code.claude.com/docs/en/mcp"
)

REACHABLE=0
UNREACHABLE=0
ERRORS=""

echo "Checking documentation pages..."
echo ""

for entry in "${DOCS[@]}"; do
    name="${entry%%|*}"
    url="${entry##*|}"

    # Check if URL is reachable (HEAD request, 5 second timeout)
    if curl -s -o /dev/null -w "%{http_code}" --head --max-time 5 "$url" 2>/dev/null | grep -q "^[23]"; then
        echo "  OK: $name ($url)"
        REACHABLE=$((REACHABLE + 1))
    else
        echo "  UNREACHABLE: $name ($url)"
        UNREACHABLE=$((UNREACHABLE + 1))
        ERRORS="$ERRORS\n  - $name: $url"
    fi
done

echo ""
echo "=== Results ==="
echo "  Reachable:   $REACHABLE"
echo "  Unreachable: $UNREACHABLE"

if [ "$UNREACHABLE" -gt 0 ]; then
    echo ""
    echo "Unreachable pages:"
    echo -e "$ERRORS"
    echo ""
    echo "WARNING: Some documentation pages could not be reached."
    echo "This may indicate URL changes. Run the upstream-watch agent for details."
fi

# Update doc-index.md if requested
if [ "$UPDATE" = "--update" ] && [ "$REACHABLE" -gt 0 ]; then
    echo ""
    echo "Updating doc-index.md verification dates..."

    # Update the "Last updated" header
    sed -i "s/^Last updated: .*/Last updated: $TODAY/" "$DOC_INDEX"

    # Update individual verification dates for reachable docs
    for entry in "${DOCS[@]}"; do
        name="${entry%%|*}"
        url="${entry##*|}"

        # Only update if page was reachable
        if curl -s -o /dev/null -w "%{http_code}" --head --max-time 5 "$url" 2>/dev/null | grep -q "^[23]"; then
            # Update the date in the table row containing this URL
            # Match the line with the URL and replace the date field
            sed -i "s|\(.*${url}.*\) [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\} \(.*\)|\1 $TODAY \2|" "$DOC_INDEX"
        fi
    done

    echo "  Done. Verification dates updated to $TODAY."
fi

echo ""
if [ "$UNREACHABLE" -gt 0 ]; then
    echo "COMPLETED WITH WARNINGS"
    exit 1
else
    echo "ALL CHECKS PASSED"
    exit 0
fi

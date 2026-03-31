#!/usr/bin/env python3
"""
StoryForge Upstream Documentation Monitor

Monitors Anthropic Claude Code documentation pages for content changes.
Compares current page content against stored hash baselines and generates
change reports when differences are detected.

Usage:
    python scripts/upstream_monitor.py                        # Check for changes
    python scripts/upstream_monitor.py --update-baseline      # Save current state as baseline
    python scripts/upstream_monitor.py --report-path out      # Write report to directory
    python scripts/upstream_monitor.py --json                 # Output JSON for CI pipelines
    python scripts/upstream_monitor.py --issue-body body.md   # Write GitHub issue body to file

Requires: Python 3.8+ (stdlib only, no pip dependencies)
"""

import hashlib
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# --- Configuration ---

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
BASELINE_PATH = REPO_ROOT / "docs" / "upstream" / "baseline-hashes.json"
DOC_INDEX_PATH = REPO_ROOT / "docs" / "upstream" / "doc-index.md"
REPORT_DIR = REPO_ROOT / "docs" / "upstream" / "reports"

# All official Anthropic Claude Code documentation pages
DOC_PAGES = {
    "memory": {
        "name": "Memory & CLAUDE.md",
        "url": "https://code.claude.com/docs/en/memory",
        "impact_areas": ["CLAUDE.md templates", "rules files", "auto memory"],
    },
    "sub-agents": {
        "name": "Subagents",
        "url": "https://code.claude.com/docs/en/sub-agents",
        "impact_areas": ["agent definitions", "agent frontmatter"],
    },
    "hooks": {
        "name": "Hooks",
        "url": "https://code.claude.com/docs/en/hooks",
        "impact_areas": ["settings.json hooks", "enforcement layer"],
    },
    "skills": {
        "name": "Skills",
        "url": "https://code.claude.com/docs/en/skills",
        "impact_areas": ["skill definitions", "SKILL.md format"],
    },
    "settings": {
        "name": "Settings",
        "url": "https://code.claude.com/docs/en/settings",
        "impact_areas": ["settings.json templates", "permission rules"],
    },
    "cli-reference": {
        "name": "CLI Reference",
        "url": "https://code.claude.com/docs/en/cli-reference",
        "impact_areas": ["scripts", "CLI usage patterns"],
    },
    "permission-modes": {
        "name": "Permission Modes",
        "url": "https://code.claude.com/docs/en/permission-modes",
        "impact_areas": ["safety policy", "default modes"],
    },
    "permissions": {
        "name": "Permissions",
        "url": "https://code.claude.com/docs/en/permissions",
        "impact_areas": ["permission rules", "deny patterns"],
    },
    "common-workflows": {
        "name": "Common Workflows",
        "url": "https://code.claude.com/docs/en/common-workflows",
        "impact_areas": ["workflow documentation"],
    },
    "best-practices": {
        "name": "Best Practices",
        "url": "https://code.claude.com/docs/en/best-practices",
        "impact_areas": ["CLAUDE.md guidance"],
    },
    "headless": {
        "name": "Headless Mode",
        "url": "https://code.claude.com/docs/en/headless",
        "impact_areas": ["scripts", "CI integration"],
    },
    "github-actions": {
        "name": "GitHub Actions",
        "url": "https://code.claude.com/docs/en/github-actions",
        "impact_areas": ["CI workflow"],
    },
    "agent-teams": {
        "name": "Agent Teams",
        "url": "https://code.claude.com/docs/en/agent-teams",
        "impact_areas": ["multi-agent patterns"],
    },
    "mcp": {
        "name": "MCP",
        "url": "https://code.claude.com/docs/en/mcp",
        "impact_areas": ["MCP configuration"],
    },
    "scheduled-tasks": {
        "name": "Scheduled Tasks",
        "url": "https://code.claude.com/docs/en/scheduled-tasks",
        "impact_areas": ["cron configuration", "monitoring"],
    },
}

# Request timeout in seconds
FETCH_TIMEOUT = 15
USER_AGENT = "StoryForge-UpstreamMonitor/1.0"


# --- Fetching ---

def fetch_page(url: str) -> Optional[str]:
    """Fetch a documentation page and return its text content."""
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as e:
        return None


def normalize_content(html: str) -> str:
    """Normalize page content for stable hashing.

    Strips volatile elements (timestamps, session tokens, analytics)
    while preserving semantic documentation content.
    """
    # Normalize line endings first
    text = html.replace("\r\n", "\n").replace("\r", "\n")
    # Remove script tags and their content
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    # Remove style tags
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    # Remove HTML comments
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # Remove data attributes (often contain dynamic values)
    text = re.sub(r'\s+data-[a-z-]+="[^"]*"', "", text)
    # Remove nonce attributes
    text = re.sub(r'\s+nonce="[^"]*"', "", text)
    # Strip HTML tags to get text content
    text = re.sub(r"<[^>]+>", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def content_hash(text: str) -> str:
    """Compute SHA-256 hash of normalized content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# --- Baseline Management ---

def load_baseline() -> dict:
    """Load stored hash baseline."""
    if BASELINE_PATH.is_file():
        with open(BASELINE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_baseline(baseline: dict):
    """Save hash baseline to disk."""
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(BASELINE_PATH, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2, sort_keys=True)


# --- Monitoring ---

def check_all_pages(baseline: dict) -> dict:
    """Check all doc pages against baseline.

    Returns dict with:
    {
        "timestamp": "...",
        "changes": [...],
        "new_pages": [...],
        "unreachable": [...],
        "unchanged": [...],
        "current_hashes": {...}
    }
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result = {
        "timestamp": now,
        "changes": [],
        "new_pages": [],
        "unreachable": [],
        "unchanged": [],
        "current_hashes": {},
    }

    for page_id, page_info in DOC_PAGES.items():
        name = page_info["name"]
        url = page_info["url"]
        impact_areas = page_info["impact_areas"]

        raw = fetch_page(url)

        if raw is None:
            result["unreachable"].append({
                "id": page_id,
                "name": name,
                "url": url,
            })
            continue

        normalized = normalize_content(raw)
        current = content_hash(normalized)
        result["current_hashes"][page_id] = current

        stored = baseline.get(page_id, {}).get("hash")

        if stored is None:
            result["new_pages"].append({
                "id": page_id,
                "name": name,
                "url": url,
                "hash": current,
                "impact_areas": impact_areas,
            })
        elif stored != current:
            result["changes"].append({
                "id": page_id,
                "name": name,
                "url": url,
                "old_hash": stored,
                "new_hash": current,
                "impact_areas": impact_areas,
                "last_checked": baseline.get(page_id, {}).get("checked", "unknown"),
            })
        else:
            result["unchanged"].append({
                "id": page_id,
                "name": name,
            })

    return result


# --- Reporting ---

def generate_markdown_report(result: dict) -> str:
    """Generate a markdown change report."""
    lines = []
    ts = result["timestamp"]
    date_str = ts[:10]

    lines.append(f"# Upstream Documentation Change Report")
    lines.append(f"")
    lines.append(f"**Generated**: {ts}")
    lines.append(f"**Pages checked**: {len(DOC_PAGES)}")
    lines.append(f"**Changes detected**: {len(result['changes'])}")
    lines.append(f"**New pages**: {len(result['new_pages'])}")
    lines.append(f"**Unreachable**: {len(result['unreachable'])}")
    lines.append(f"**Unchanged**: {len(result['unchanged'])}")
    lines.append(f"")

    if result["changes"]:
        lines.append(f"## Changes Detected")
        lines.append(f"")
        for change in result["changes"]:
            lines.append(f"### {change['name']}")
            lines.append(f"")
            lines.append(f"- **URL**: {change['url']}")
            lines.append(f"- **Last checked**: {change['last_checked']}")
            lines.append(f"- **Impact areas**: {', '.join(change['impact_areas'])}")
            lines.append(f"- **Action required**: Review the page and determine impact on StoryForge")
            lines.append(f"")

        lines.append(f"### Recommended Actions")
        lines.append(f"")
        lines.append(f"1. Review each changed page manually")
        lines.append(f"2. Classify impact using `docs/upstream/release-watch.md` categories")
        lines.append(f"3. Create Stories for required adaptations using `/story-write`")
        lines.append(f"4. Update baseline with: `python scripts/upstream_monitor.py --update-baseline`")
        lines.append(f"")

    if result["new_pages"]:
        lines.append(f"## New Pages (Not in Baseline)")
        lines.append(f"")
        for page in result["new_pages"]:
            lines.append(f"- **{page['name']}**: {page['url']}")
            lines.append(f"  Impact areas: {', '.join(page['impact_areas'])}")
        lines.append(f"")
        lines.append(f"Run `--update-baseline` to include these pages in future checks.")
        lines.append(f"")

    if result["unreachable"]:
        lines.append(f"## Unreachable Pages")
        lines.append(f"")
        for page in result["unreachable"]:
            lines.append(f"- **{page['name']}**: {page['url']}")
        lines.append(f"")
        lines.append(f"These pages could not be fetched. They may have been moved or renamed.")
        lines.append(f"")

    if result["unchanged"]:
        lines.append(f"## Unchanged Pages")
        lines.append(f"")
        for page in result["unchanged"]:
            lines.append(f"- {page['name']}")
        lines.append(f"")

    return "\n".join(lines)


def generate_json_output(result: dict) -> str:
    """Generate JSON output for CI pipelines."""
    output = {
        "timestamp": result["timestamp"],
        "has_changes": len(result["changes"]) > 0 or len(result["new_pages"]) > 0,
        "summary": {
            "changes": len(result["changes"]),
            "new_pages": len(result["new_pages"]),
            "unreachable": len(result["unreachable"]),
            "unchanged": len(result["unchanged"]),
        },
        "changes": result["changes"],
        "new_pages": result["new_pages"],
        "unreachable": result["unreachable"],
    }
    return json.dumps(output, indent=2)


def generate_issue_body(result: dict) -> str:
    """Generate GitHub issue body for detected changes."""
    lines = []
    lines.append("## Upstream Documentation Changes Detected")
    lines.append("")
    lines.append(f"The daily upstream monitor detected **{len(result['changes'])} change(s)** "
                 f"and **{len(result['new_pages'])} new page(s)** in the official Anthropic "
                 f"Claude Code documentation.")
    lines.append("")

    if result["changes"]:
        lines.append("### Changed Pages")
        lines.append("")
        lines.append("| Page | Impact Areas | Action |")
        lines.append("|:-----|:-------------|:-------|")
        for change in result["changes"]:
            areas = ", ".join(change["impact_areas"])
            lines.append(f"| [{change['name']}]({change['url']}) | {areas} | Review and adapt |")
        lines.append("")

    if result["new_pages"]:
        lines.append("### New Pages")
        lines.append("")
        for page in result["new_pages"]:
            lines.append(f"- [{page['name']}]({page['url']})")
        lines.append("")

    if result["unreachable"]:
        lines.append("### Unreachable Pages")
        lines.append("")
        for page in result["unreachable"]:
            lines.append(f"- {page['name']}: {page['url']} (may have been moved)")
        lines.append("")

    lines.append("### Next Steps")
    lines.append("")
    lines.append("1. Review each changed page")
    lines.append("2. Classify impact per `docs/upstream/release-watch.md`")
    lines.append("3. Create adaptation Stories with `/story-write`")
    lines.append("4. After adapting, update baseline: `python scripts/upstream_monitor.py --update-baseline`")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by StoryForge Upstream Monitor*")

    return "\n".join(lines)


# --- Main ---

def main():
    # Handle stdout encoding on Windows
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, TypeError):
            pass

    args = sys.argv[1:]
    update_baseline = "--update-baseline" in args
    json_output = "--json" in args
    report_path = None
    issue_body_path = None

    for i, arg in enumerate(args):
        if arg == "--report-path" and i + 1 < len(args):
            report_path = Path(args[i + 1])
        elif arg == "--issue-body" and i + 1 < len(args):
            issue_body_path = Path(args[i + 1])

    # Load baseline
    baseline = load_baseline()

    if update_baseline:
        print("Updating baseline hashes...")
        new_baseline = {}
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        for page_id, page_info in DOC_PAGES.items():
            print(f"  Fetching {page_info['name']}...", end=" ", flush=True)
            raw = fetch_page(page_info["url"])
            if raw:
                normalized = normalize_content(raw)
                h = content_hash(normalized)
                new_baseline[page_id] = {
                    "hash": h,
                    "checked": now,
                    "url": page_info["url"],
                    "name": page_info["name"],
                }
                print("OK")
            else:
                print("UNREACHABLE")
                # Keep old baseline entry if page is temporarily unreachable
                if page_id in baseline:
                    new_baseline[page_id] = baseline[page_id]
                    new_baseline[page_id]["checked"] = now
                    print(f"    (kept previous hash)")

        save_baseline(new_baseline)
        print(f"\nBaseline saved to {BASELINE_PATH}")
        print(f"Pages baselined: {len(new_baseline)}")
        return

    # Run check
    if not json_output:
        print("StoryForge Upstream Monitor")
        print(f"Checking {len(DOC_PAGES)} documentation pages...")
        print()

    result = check_all_pages(baseline)

    if json_output:
        print(generate_json_output(result))
    else:
        # Print summary
        changes = len(result["changes"])
        new_pages = len(result["new_pages"])
        unreachable = len(result["unreachable"])
        unchanged = len(result["unchanged"])

        if changes > 0:
            print(f"  CHANGES DETECTED: {changes} page(s) changed")
            for c in result["changes"]:
                print(f"    - {c['name']}: {c['url']}")
                print(f"      Impact: {', '.join(c['impact_areas'])}")
            print()

        if new_pages > 0:
            print(f"  NEW PAGES: {new_pages} page(s) not in baseline")
            for p in result["new_pages"]:
                print(f"    - {p['name']}: {p['url']}")
            print()

        if unreachable > 0:
            print(f"  UNREACHABLE: {unreachable} page(s)")
            for p in result["unreachable"]:
                print(f"    - {p['name']}: {p['url']}")
            print()

        print(f"  Unchanged: {unchanged} page(s)")
        print()

        if changes > 0 or new_pages > 0:
            print("ACTION REQUIRED: Review changes and adapt StoryForge.")
            print("Run with --update-baseline after adapting.")
        else:
            print("No changes detected. StoryForge is up to date.")

    # Save report if requested
    if report_path:
        report_path.mkdir(parents=True, exist_ok=True)
        date_str = result["timestamp"][:10]
        report_file = report_path / f"upstream-report-{date_str}.md"
        report_file.write_text(generate_markdown_report(result), encoding="utf-8")
        if not json_output:
            print(f"\nReport saved to {report_file}")

    # Write issue body if requested (for CI pipelines)
    if issue_body_path and (result["changes"] or result["new_pages"]):
        issue_body_path.parent.mkdir(parents=True, exist_ok=True)
        issue_body_path.write_text(generate_issue_body(result), encoding="utf-8")
        if not json_output:
            print(f"Issue body saved to {issue_body_path}")

    # Exit code: 1 if changes detected (for CI pipelines)
    if result["changes"] or result["new_pages"]:
        sys.exit(1)
    elif result["unreachable"] and not result["unchanged"]:
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

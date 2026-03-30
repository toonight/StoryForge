"""
Tests for StoryForge Upstream Documentation Monitor.

Verifies monitoring script parsing, hashing, and reporting logic.
"""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from upstream_monitor import (
    DOC_PAGES,
    content_hash,
    generate_issue_body,
    generate_json_output,
    generate_markdown_report,
    load_baseline,
    normalize_content,
)


class TestNormalizeContent:
    """Test HTML normalization for stable hashing."""

    def test_strips_script_tags(self):
        html = '<p>hello</p><script>var x = 1;</script><p>world</p>'
        result = normalize_content(html)
        assert "var x" not in result
        assert "hello" in result
        assert "world" in result

    def test_strips_style_tags(self):
        html = '<style>.foo { color: red; }</style><p>content</p>'
        result = normalize_content(html)
        assert "color" not in result
        assert "content" in result

    def test_strips_html_comments(self):
        html = '<p>before</p><!-- comment --><p>after</p>'
        result = normalize_content(html)
        assert "comment" not in result

    def test_strips_data_attributes(self):
        html = '<div data-session="abc123" data-nonce="xyz">text</div>'
        result = normalize_content(html)
        assert "abc123" not in result

    def test_strips_html_tags(self):
        html = '<h1>Title</h1><p>Paragraph</p>'
        result = normalize_content(html)
        assert "<h1>" not in result
        assert "Title" in result

    def test_collapses_whitespace(self):
        html = '<p>hello    world</p>\n\n\n<p>foo</p>'
        result = normalize_content(html)
        assert "  " not in result

    def test_deterministic(self):
        html = '<p>same content</p>'
        assert normalize_content(html) == normalize_content(html)


class TestContentHash:
    """Test content hashing."""

    def test_consistent_hash(self):
        assert content_hash("hello") == content_hash("hello")

    def test_different_content_different_hash(self):
        assert content_hash("hello") != content_hash("world")

    def test_hash_is_sha256(self):
        h = content_hash("test")
        assert len(h) == 64  # SHA-256 hex length
        assert all(c in "0123456789abcdef" for c in h)


class TestDocPages:
    """Test DOC_PAGES configuration."""

    def test_all_pages_have_required_fields(self):
        for page_id, info in DOC_PAGES.items():
            assert "name" in info, f"{page_id} missing name"
            assert "url" in info, f"{page_id} missing url"
            assert "impact_areas" in info, f"{page_id} missing impact_areas"

    def test_all_urls_are_https(self):
        for page_id, info in DOC_PAGES.items():
            assert info["url"].startswith("https://"), f"{page_id} URL not HTTPS"

    def test_at_least_14_pages(self):
        assert len(DOC_PAGES) >= 14

    def test_critical_pages_present(self):
        page_names = {info["name"] for info in DOC_PAGES.values()}
        critical = ["Subagents", "Hooks", "Skills", "Settings"]
        for name in critical:
            assert name in page_names, f"Critical page missing: {name}"


class TestBaseline:
    """Test baseline loading."""

    def test_loads_existing_baseline(self):
        baseline = load_baseline()
        # After --update-baseline was run, we should have entries
        assert len(baseline) > 0

    def test_baseline_entries_have_hash(self):
        baseline = load_baseline()
        for page_id, entry in baseline.items():
            assert "hash" in entry, f"{page_id} missing hash"
            assert len(entry["hash"]) == 64


class TestReportGeneration:
    """Test report generation functions."""

    SAMPLE_RESULT = {
        "timestamp": "2026-03-29T12:00:00Z",
        "changes": [
            {
                "id": "hooks",
                "name": "Hooks",
                "url": "https://code.claude.com/docs/en/hooks",
                "old_hash": "aaa",
                "new_hash": "bbb",
                "impact_areas": ["settings.json hooks", "enforcement layer"],
                "last_checked": "2026-03-28",
            }
        ],
        "new_pages": [],
        "unreachable": [],
        "unchanged": [{"id": "skills", "name": "Skills"}],
        "current_hashes": {},
    }

    def test_markdown_report_has_changes(self):
        report = generate_markdown_report(self.SAMPLE_RESULT)
        assert "Changes Detected" in report
        assert "Hooks" in report
        assert "settings.json hooks" in report

    def test_markdown_report_has_timestamp(self):
        report = generate_markdown_report(self.SAMPLE_RESULT)
        assert "2026-03-29" in report

    def test_json_output_structure(self):
        output = generate_json_output(self.SAMPLE_RESULT)
        data = json.loads(output)
        assert data["has_changes"] is True
        assert data["summary"]["changes"] == 1

    def test_json_output_no_changes(self):
        result = {**self.SAMPLE_RESULT, "changes": [], "new_pages": []}
        output = generate_json_output(result)
        data = json.loads(output)
        assert data["has_changes"] is False

    def test_issue_body_has_table(self):
        body = generate_issue_body(self.SAMPLE_RESULT)
        assert "| Page |" in body or "Changed Pages" in body
        assert "Hooks" in body

    def test_issue_body_has_next_steps(self):
        body = generate_issue_body(self.SAMPLE_RESULT)
        assert "Next Steps" in body


class TestMonitorScript:
    """Test monitor script structure."""

    def test_script_exists(self):
        assert (REPO_ROOT / "scripts" / "upstream_monitor.py").is_file()

    def test_baseline_file_exists(self):
        assert (REPO_ROOT / "docs" / "upstream" / "baseline-hashes.json").is_file()

    def test_baseline_is_valid_json(self):
        with open(REPO_ROOT / "docs" / "upstream" / "baseline-hashes.json") as f:
            data = json.load(f)
        assert isinstance(data, dict)


class TestGitHubAction:
    """Test GitHub Action workflow exists and is valid."""

    def test_workflow_exists(self):
        assert (REPO_ROOT / ".github" / "workflows" / "upstream-monitor.yml").is_file()

    def test_workflow_has_cron(self):
        content = (REPO_ROOT / ".github" / "workflows" / "upstream-monitor.yml").read_text()
        assert "cron:" in content
        assert "0 7 * * *" in content

    def test_workflow_has_issue_creation(self):
        content = (REPO_ROOT / ".github" / "workflows" / "upstream-monitor.yml").read_text()
        assert "create-issue" in content


class TestUpstreamMonitorAgent:
    """Test upstream-monitor agent definition."""

    def test_agent_exists(self):
        assert (REPO_ROOT / "templates" / "home" / ".claude" / "agents" / "upstream-monitor.md").is_file()

    def test_agent_has_frontmatter(self):
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "agents" / "upstream-monitor.md").read_text()
        assert content.startswith("---")
        assert "name: upstream-monitor" in content

    def test_agent_uses_sonnet(self):
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "agents" / "upstream-monitor.md").read_text()
        assert "model: sonnet" in content


class TestUpstreamCheckSkill:
    """Test upstream-check skill."""

    def test_skill_exists(self):
        assert (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "upstream-check" / "SKILL.md").is_file()

    def test_skill_has_frontmatter(self):
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "upstream-check" / "SKILL.md").read_text()
        assert content.startswith("---")
        assert "name: upstream-check" in content

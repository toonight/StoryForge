"""
Tests for StoryForge generated file content validation.

Verifies that template content follows StoryForge conventions and Anthropic guidelines.
"""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
HOME_TEMPLATE = REPO_ROOT / "templates" / "home" / ".claude"


class TestCLAUDEMdContent:
    """Verify CLAUDE.md content follows guidelines."""

    def test_mentions_work_hierarchy(self):
        content = (HOME_TEMPLATE / "CLAUDE.md").read_text()
        assert "Initiative" in content
        assert "Feature" in content
        assert "Story" in content
        assert "Task" in content

    def test_mentions_kanban_states(self):
        content = (HOME_TEMPLATE / "CLAUDE.md").read_text()
        assert "Backlog" in content
        assert "In Progress" in content
        assert "Done" in content

    def test_mentions_convention_notice(self):
        """CLAUDE.md should clearly state it's a StoryForge convention."""
        content = (HOME_TEMPLATE / "CLAUDE.md").read_text()
        assert "convention" in content.lower()

    def test_mentions_execution_sequence(self):
        content = (HOME_TEMPLATE / "CLAUDE.md").read_text()
        assert "Planning" in content
        assert "Implementation" in content
        assert "Validation" in content

    def test_mentions_anti_scope_drift(self):
        content = (HOME_TEMPLATE / "CLAUDE.md").read_text()
        assert "scope" in content.lower()
        assert "backlog" in content.lower()


class TestSettingsContent:
    """Verify settings.json follows safe defaults."""

    def test_no_bypass_permissions(self):
        """Settings should not enable bypass permissions mode."""
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        default_mode = data.get("permissions", {}).get("defaultMode", "")
        assert default_mode != "bypassPermissions"

    def test_no_auto_mode(self):
        """Settings should not default to auto mode (requires Team plan)."""
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        default_mode = data.get("permissions", {}).get("defaultMode", "")
        assert default_mode != "auto"

    def test_has_deny_rules(self):
        """Settings should have protective deny rules."""
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        deny = data.get("permissions", {}).get("deny", [])
        assert len(deny) > 0, "Settings should have at least one deny rule"

    def test_has_cloud_credential_deny_rules(self):
        """Settings should deny access to cloud credential directories."""
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        deny = data.get("permissions", {}).get("deny", [])
        deny_str = " ".join(deny)
        for path in ["~/.aws/**", "~/.kube/**", "~/.docker/**", "~/.git-credentials"]:
            assert path in deny_str, f"Missing deny rule for {path}"

    def test_has_hooks(self):
        """Settings should define hooks."""
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        assert "hooks" in data


class TestSourceMap:
    """Verify anthropic-source-map.md content."""

    def test_has_classification_table(self):
        content = (REPO_ROOT / "docs" / "anthropic-source-map.md").read_text()
        assert "Native" in content
        assert "Convention" in content
        assert "Enforcement" in content

    def test_covers_major_categories(self):
        content = (REPO_ROOT / "docs" / "anthropic-source-map.md").read_text()
        categories = [
            "CLAUDE.md",
            "Settings",
            "Subagents",
            "Skills",
            "Hooks",
            "Kanban",
        ]
        for category in categories:
            assert category in content, f"Source map missing category: {category}"


class TestOperatingModel:
    """Verify operating-model.md content."""

    def test_has_work_hierarchy(self):
        content = (REPO_ROOT / "docs" / "operating-model.md").read_text()
        assert "Initiative" in content
        assert "Feature" in content
        assert "Story" in content
        assert "Task" in content

    def test_has_kanban_states(self):
        content = (REPO_ROOT / "docs" / "operating-model.md").read_text()
        for state in ["Backlog", "Ready", "In Progress", "Review", "Done"]:
            assert state in content

    def test_has_done_criteria(self):
        content = (REPO_ROOT / "docs" / "operating-model.md").read_text()
        assert "Done" in content
        assert "criteria" in content.lower() or "Criteria" in content

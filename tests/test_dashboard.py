"""
Tests for StoryForge Kanban Dashboard.

Verifies the dashboard parsing logic and rendering.
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from dashboard import (
    KanbanData,
    count_checkboxes,
    extract_section,
    parse_table_rows,
    render_velocity,
    render_dependencies,
)


class TestParseTableRows:
    """Test markdown table parsing."""

    def test_simple_table(self):
        text = """| ID | Title | Status |
|---|---|---|
| STORY-001 | First story | Done |
| STORY-002 | Second story | In Progress |"""
        rows = parse_table_rows(text)
        assert len(rows) == 2
        assert rows[0]["ID"] == "STORY-001"
        assert rows[0]["Title"] == "First story"
        assert rows[1]["Status"] == "In Progress"

    def test_empty_table(self):
        text = """| ID | Title |
|---|---|"""
        rows = parse_table_rows(text)
        assert len(rows) == 0

    def test_no_table(self):
        rows = parse_table_rows("just some text\nno table here")
        assert len(rows) == 0


class TestExtractSection:
    """Test markdown section extraction."""

    def test_extract_existing_section(self):
        text = """### Backlog

| ID | Title |
|---|---|
| STORY-001 | First |

### Done

Nothing here."""
        section = extract_section(text, "Backlog")
        assert "STORY-001" in section

    def test_extract_missing_section(self):
        text = "### Other\nSome content"
        section = extract_section(text, "Missing")
        assert section == ""


class TestCountCheckboxes:
    """Test checkbox counting."""

    def test_mixed_checkboxes(self):
        text = """- [x] Done item
- [ ] Pending item
- [x] Another done
- [ ] Another pending"""
        checked, total = count_checkboxes(text)
        assert checked == 2
        assert total == 4

    def test_no_checkboxes(self):
        checked, total = count_checkboxes("no checkboxes here")
        assert checked == 0
        assert total == 0

    def test_all_done(self):
        text = "- [x] One\n- [x] Two\n- [x] Three"
        checked, total = count_checkboxes(text)
        assert checked == 3
        assert total == 3


class TestKanbanData:
    """Test KanbanData loading from the sample project."""

    SAMPLE_PROJECT = REPO_ROOT / "examples" / "sample-project"

    def test_loads_sample_kanban(self):
        data = KanbanData(self.SAMPLE_PROJECT)
        assert data.load() is True

    def test_parses_features(self):
        data = KanbanData(self.SAMPLE_PROJECT)
        data.load()
        assert len(data.features) > 0

    def test_parses_stories(self):
        data = KanbanData(self.SAMPLE_PROJECT)
        data.load()
        assert len(data.stories) > 0
        assert "STORY-001" in data.stories

    def test_story_has_required_fields(self):
        data = KanbanData(self.SAMPLE_PROJECT)
        data.load()
        story = data.stories["STORY-001"]
        assert story["id"] == "STORY-001"
        assert story["status"] in ("Backlog", "Ready", "In Progress", "Review", "Done")
        assert story["criteria_total"] >= 0
        assert "depends_on" in story
        assert "github_ref" in story

    def test_no_kanban_dir_returns_false(self, tmp_path):
        data = KanbanData(tmp_path)
        assert data.load() is False

    def test_board_sections_populated(self):
        data = KanbanData(self.SAMPLE_PROJECT)
        data.load()
        # At least one column should have items
        total_items = sum(len(items) for items in data.board_sections.values())
        assert total_items > 0


class TestDashboardScript:
    """Test dashboard script can be imported and has entry point."""

    def test_importable(self):
        import dashboard
        assert hasattr(dashboard, "main")
        assert hasattr(dashboard, "render_dashboard")
        assert hasattr(dashboard, "Colors")

    def test_colors_can_be_disabled(self):
        from dashboard import Colors
        Colors.disable()
        assert Colors.c(Colors.RED, "test") == "test"
        Colors.ENABLED = True  # Reset

    def test_render_header(self):
        from dashboard import Colors, render_header
        Colors.disable()
        header = render_header("TestProject", 80)
        assert "TestProject" in header
        Colors.ENABLED = True


class TestCrossPlatformScripts:
    """Test PowerShell script existence and structure."""

    PS_SCRIPTS = [
        "scripts/install_storyforge.ps1",
        "scripts/bootstrap_project.ps1",
        "scripts/validate_templates.ps1",
        "scripts/sync_upstream_docs.ps1",
    ]

    @pytest.mark.parametrize("script_path", PS_SCRIPTS)
    def test_ps_script_exists(self, script_path):
        assert (REPO_ROOT / script_path).is_file()

    @pytest.mark.parametrize("script_path", PS_SCRIPTS)
    def test_ps_script_has_requires(self, script_path):
        """PowerShell scripts should declare minimum version."""
        content = (REPO_ROOT / script_path).read_text()
        assert "#Requires" in content

    @pytest.mark.parametrize("script_path", PS_SCRIPTS)
    def test_ps_script_has_error_preference(self, script_path):
        """PowerShell scripts should set ErrorActionPreference."""
        content = (REPO_ROOT / script_path).read_text()
        assert "ErrorActionPreference" in content

    def test_bash_and_ps_parity(self):
        """Every .sh script should have a corresponding .ps1."""
        bash_scripts = set(p.stem for p in (REPO_ROOT / "scripts").glob("*.sh"))
        ps_scripts = set(p.stem for p in (REPO_ROOT / "scripts").glob("*.ps1"))
        missing = bash_scripts - ps_scripts
        assert not missing, f"Bash scripts without PowerShell counterpart: {missing}"


class TestDashboardSkill:
    """Test dashboard skill exists and has proper frontmatter."""

    def test_skill_exists(self):
        assert (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "dashboard" / "SKILL.md").is_file()

    def test_skill_has_frontmatter(self):
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "dashboard" / "SKILL.md").read_text()
        assert content.startswith("---")
        assert "name: dashboard" in content


class TestVelocity:
    """Test velocity computation and rendering."""

    def test_velocity_data_loads(self):
        data = KanbanData(REPO_ROOT / "examples" / "sample-project")
        data.load()
        # StoryForge has completed sprints in sprint.md
        assert hasattr(data, "completed_sprints")

    def test_velocity_parses_completed_sprints(self):
        data = KanbanData(REPO_ROOT / "examples" / "sample-project")
        data.load()
        # Sprint 1 has a "Result: 8/8" line
        if data.completed_sprints:
            assert data.completed_sprints[0]["done"] > 0

    def test_velocity_render_no_crash(self):
        from dashboard import Colors
        Colors.disable()
        data = KanbanData(REPO_ROOT / "examples" / "sample-project")
        data.load()
        result = render_velocity(data, 80)
        assert isinstance(result, str)
        Colors.ENABLED = True


class TestDependencies:
    """Test dependency tracking."""

    def test_get_blocked_stories(self):
        data = KanbanData(REPO_ROOT / "examples" / "sample-project")
        data.load()
        blocked = data.get_blocked_stories()
        assert isinstance(blocked, list)

    def test_dependency_render_no_crash(self):
        from dashboard import Colors
        Colors.disable()
        data = KanbanData(REPO_ROOT / "examples" / "sample-project")
        data.load()
        result = render_dependencies(data, 80)
        assert isinstance(result, str)
        Colors.ENABLED = True

    def test_story_template_has_depends_field(self):
        content = (REPO_ROOT / "templates" / "project" / ".kanban" / "stories" / "STORY-TEMPLATE.md").read_text()
        assert "Depends-On" in content

    def test_story_template_has_github_field(self):
        content = (REPO_ROOT / "templates" / "project" / ".kanban" / "stories" / "STORY-TEMPLATE.md").read_text()
        assert "GitHub" in content


class TestGhLinkSkill:
    """Test gh-link skill."""

    def test_skill_exists(self):
        assert (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "gh-link" / "SKILL.md").is_file()

    def test_skill_has_frontmatter(self):
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "gh-link" / "SKILL.md").read_text()
        assert content.startswith("---")
        assert "name: gh-link" in content


class TestPostToolUseHook:
    """Test PostToolUse hook in settings template."""

    def test_settings_has_post_tool_use(self):
        import json
        with open(REPO_ROOT / "templates" / "project" / ".claude" / "settings.json") as f:
            data = json.load(f)
        assert "PostToolUse" in data.get("hooks", {})

    def test_post_tool_use_targets_edit_write(self):
        import json
        with open(REPO_ROOT / "templates" / "project" / ".claude" / "settings.json") as f:
            data = json.load(f)
        hook = data["hooks"]["PostToolUse"][0]
        assert "Edit" in hook["matcher"]
        assert "Write" in hook["matcher"]

"""
Tests for StoryForge template structure validation.

Verifies that all expected template files exist and have required content.
"""

import json
import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
HOME_TEMPLATE = REPO_ROOT / "templates" / "home" / ".claude"
PROJECT_TEMPLATE = REPO_ROOT / "templates" / "project"


class TestHomeTemplateStructure:
    """Verify user-level template files exist and are well-formed."""

    def test_claude_md_exists(self):
        assert (HOME_TEMPLATE / "CLAUDE.md").is_file()

    def test_claude_md_not_empty(self):
        content = (HOME_TEMPLATE / "CLAUDE.md").read_text()
        assert len(content) > 100

    def test_claude_md_under_200_lines(self):
        """CLAUDE.md should stay under 200 lines per Anthropic recommendation."""
        content = (HOME_TEMPLATE / "CLAUDE.md").read_text()
        line_count = len(content.splitlines())
        assert line_count < 200, f"CLAUDE.md has {line_count} lines (recommended < 200)"

    def test_settings_json_exists(self):
        assert (HOME_TEMPLATE / "settings.json").is_file()

    def test_settings_json_valid(self):
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_settings_json_has_permissions(self):
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        assert "permissions" in data

    def test_agents_directory_exists(self):
        assert (HOME_TEMPLATE / "agents").is_dir()

    def test_skills_directory_exists(self):
        assert (HOME_TEMPLATE / "skills").is_dir()


class TestAgentDefinitions:
    """Verify all agent files have required frontmatter."""

    REQUIRED_AGENTS = [
        "portfolio-orchestrator",
        "planner",
        "implementer",
        "reviewer",
        "doc-maintainer",
        "upstream-watch",
    ]

    @pytest.mark.parametrize("agent_name", REQUIRED_AGENTS)
    def test_agent_file_exists(self, agent_name):
        assert (HOME_TEMPLATE / "agents" / f"{agent_name}.md").is_file()

    @pytest.mark.parametrize("agent_name", REQUIRED_AGENTS)
    def test_agent_has_frontmatter(self, agent_name):
        content = (HOME_TEMPLATE / "agents" / f"{agent_name}.md").read_text()
        assert content.startswith("---"), f"{agent_name} missing YAML frontmatter"
        # Check closing frontmatter
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{agent_name} frontmatter not properly closed"

    @pytest.mark.parametrize("agent_name", REQUIRED_AGENTS)
    def test_agent_has_name_field(self, agent_name):
        content = (HOME_TEMPLATE / "agents" / f"{agent_name}.md").read_text()
        assert f"name: {agent_name}" in content

    @pytest.mark.parametrize("agent_name", REQUIRED_AGENTS)
    def test_agent_has_description(self, agent_name):
        content = (HOME_TEMPLATE / "agents" / f"{agent_name}.md").read_text()
        assert "description:" in content


class TestSkillDefinitions:
    """Verify all skill files have required frontmatter."""

    REQUIRED_SKILLS = [
        "kanban-bootstrap",
        "story-write",
        "sprint-groom",
        "release-adapt",
        "doc-update",
        "dashboard",
    ]

    @pytest.mark.parametrize("skill_name", REQUIRED_SKILLS)
    def test_skill_file_exists(self, skill_name):
        assert (HOME_TEMPLATE / "skills" / skill_name / "SKILL.md").is_file()

    @pytest.mark.parametrize("skill_name", REQUIRED_SKILLS)
    def test_skill_has_frontmatter(self, skill_name):
        content = (HOME_TEMPLATE / "skills" / skill_name / "SKILL.md").read_text()
        assert content.startswith("---"), f"{skill_name} missing YAML frontmatter"

    @pytest.mark.parametrize("skill_name", REQUIRED_SKILLS)
    def test_skill_has_name_field(self, skill_name):
        content = (HOME_TEMPLATE / "skills" / skill_name / "SKILL.md").read_text()
        assert f"name: {skill_name}" in content


class TestProjectTemplateStructure:
    """Verify project-level template files exist."""

    def test_claude_md_exists(self):
        assert (PROJECT_TEMPLATE / ".claude" / "CLAUDE.md").is_file()

    def test_settings_json_exists(self):
        assert (PROJECT_TEMPLATE / ".claude" / "settings.json").is_file()

    def test_settings_json_valid(self):
        with open(PROJECT_TEMPLATE / ".claude" / "settings.json") as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_kanban_board_exists(self):
        assert (PROJECT_TEMPLATE / ".kanban" / "board.md").is_file()

    def test_kanban_backlog_exists(self):
        assert (PROJECT_TEMPLATE / ".kanban" / "backlog.md").is_file()

    def test_kanban_sprint_exists(self):
        assert (PROJECT_TEMPLATE / ".kanban" / "sprint.md").is_file()

    def test_kanban_decisions_exists(self):
        assert (PROJECT_TEMPLATE / ".kanban" / "decisions.md").is_file()

    def test_kanban_changelog_exists(self):
        assert (PROJECT_TEMPLATE / ".kanban" / "changelog.md").is_file()

    def test_story_template_exists(self):
        assert (PROJECT_TEMPLATE / ".kanban" / "stories" / "STORY-TEMPLATE.md").is_file()

    def test_kanban_board_has_placeholder(self):
        content = (PROJECT_TEMPLATE / ".kanban" / "board.md").read_text()
        assert "{{PROJECT_NAME}}" in content

    def test_story_template_has_required_sections(self):
        content = (PROJECT_TEMPLATE / ".kanban" / "stories" / "STORY-TEMPLATE.md").read_text()
        required_sections = [
            "Acceptance Criteria",
            "Non-Goals",
            "Implementation Notes",
            "Validation Notes",
            "Risks",
            "Follow-ups",
        ]
        for section in required_sections:
            assert section in content, f"Story template missing section: {section}"


class TestDocumentation:
    """Verify core documentation files exist."""

    REQUIRED_DOCS = [
        "docs/architecture.md",
        "docs/operating-model.md",
        "docs/source-of-truth-policy.md",
        "docs/anthropic-source-map.md",
        "docs/upstream/doc-index.md",
        "docs/upstream/release-watch.md",
        "docs/upstream/changelog-adaptation-process.md",
    ]

    @pytest.mark.parametrize("doc_path", REQUIRED_DOCS)
    def test_doc_exists(self, doc_path):
        assert (REPO_ROOT / doc_path).is_file()


class TestScripts:
    """Verify script files exist."""

    REQUIRED_SCRIPTS = [
        "scripts/install_storyforge.sh",
        "scripts/bootstrap_project.sh",
        "scripts/validate_templates.sh",
        "scripts/sync_upstream_docs.sh",
    ]

    @pytest.mark.parametrize("script_path", REQUIRED_SCRIPTS)
    def test_script_exists(self, script_path):
        assert (REPO_ROOT / script_path).is_file()

    @pytest.mark.parametrize("script_path", REQUIRED_SCRIPTS)
    def test_script_has_shebang(self, script_path):
        content = (REPO_ROOT / script_path).read_text()
        assert content.startswith("#!/"), f"{script_path} missing shebang line"


class TestRulesFiles:
    """Verify .claude/rules/ files exist and have proper frontmatter."""

    def test_storyforge_repo_has_claude_md(self):
        assert (REPO_ROOT / ".claude" / "CLAUDE.md").is_file()

    def test_storyforge_repo_claude_md_not_empty(self):
        content = (REPO_ROOT / ".claude" / "CLAUDE.md").read_text()
        assert len(content) > 100

    def test_storyforge_repo_has_rules(self):
        assert (REPO_ROOT / ".claude" / "rules").is_dir()

    STORYFORGE_RULES = ["templates.md", "docs.md", "scripts.md"]

    @pytest.mark.parametrize("rule_name", STORYFORGE_RULES)
    def test_storyforge_rule_exists(self, rule_name):
        assert (REPO_ROOT / ".claude" / "rules" / rule_name).is_file()

    @pytest.mark.parametrize("rule_name", STORYFORGE_RULES)
    def test_storyforge_rule_has_paths_frontmatter(self, rule_name):
        content = (REPO_ROOT / ".claude" / "rules" / rule_name).read_text()
        assert content.startswith("---")
        assert "paths:" in content

    def test_home_template_has_rules(self):
        assert (HOME_TEMPLATE / "rules" / "storyforge-delivery.md").is_file()

    def test_project_template_has_kanban_rule(self):
        assert (PROJECT_TEMPLATE / ".claude" / "rules" / "kanban.md").is_file()

    def test_project_kanban_rule_has_paths(self):
        content = (PROJECT_TEMPLATE / ".claude" / "rules" / "kanban.md").read_text()
        assert "paths:" in content
        assert ".kanban/" in content


class TestSettingsHooks:
    """Verify settings.json hooks are properly configured."""

    def test_has_session_start_hook(self):
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        assert "SessionStart" in data.get("hooks", {})

    def test_has_stop_hook(self):
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        assert "Stop" in data.get("hooks", {})

    def test_stop_hook_checks_stop_active(self):
        """Stop hook must check stop_hook_active to prevent infinite loops."""
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        stop_hooks = data["hooks"]["Stop"]
        hook_command = stop_hooks[0]["hooks"][0]["command"]
        assert "stop_hook_active" in hook_command

    def test_has_notification_hook(self):
        with open(HOME_TEMPLATE / "settings.json") as f:
            data = json.load(f)
        assert "Notification" in data.get("hooks", {})

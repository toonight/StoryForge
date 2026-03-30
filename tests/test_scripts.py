"""
Tests for StoryForge script validation.

Verifies scripts are syntactically correct and follow conventions.
"""

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"


class TestScriptSyntax:
    """Verify scripts have valid bash syntax."""

    SCRIPTS = [
        "install_storyforge.sh",
        "bootstrap_project.sh",
        "validate_templates.sh",
    ]

    @pytest.mark.parametrize("script_name", SCRIPTS)
    def test_script_has_shebang(self, script_name):
        content = (SCRIPTS_DIR / script_name).read_text()
        assert content.startswith("#!/"), f"{script_name} missing shebang"

    @pytest.mark.parametrize("script_name", SCRIPTS)
    def test_script_uses_set_options(self, script_name):
        """Scripts should use safe bash options."""
        content = (SCRIPTS_DIR / script_name).read_text()
        assert "set -e" in content or "set -euo pipefail" in content, (
            f"{script_name} should use 'set -e' or 'set -euo pipefail'"
        )

    @pytest.mark.parametrize("script_name", SCRIPTS)
    def test_script_syntax_check(self, script_name):
        """Check bash syntax with bash -n if available."""
        script_path = SCRIPTS_DIR / script_name
        try:
            # Read as bytes to avoid Windows line ending issues with bash
            content = script_path.read_bytes().replace(b"\r\n", b"\n")
            result = subprocess.run(
                ["bash", "-n"],
                input=content,
                capture_output=True,
                timeout=30,
            )
            assert result.returncode == 0, (
                f"{script_name} has syntax errors: {result.stderr.decode()}"
            )
        except FileNotFoundError:
            pytest.skip("bash not available for syntax checking")


class TestInstallScript:
    """Verify install script content."""

    def test_references_template_dir(self):
        content = (SCRIPTS_DIR / "install_storyforge.sh").read_text()
        assert "templates/home" in content

    def test_creates_backup(self):
        content = (SCRIPTS_DIR / "install_storyforge.sh").read_text()
        assert "backup" in content.lower() or "BACKUP" in content

    def test_handles_existing_files(self):
        content = (SCRIPTS_DIR / "install_storyforge.sh").read_text()
        assert "EXISTS" in content or "exists" in content


class TestBootstrapScript:
    """Verify bootstrap script content."""

    def test_references_template_dir(self):
        content = (SCRIPTS_DIR / "bootstrap_project.sh").read_text()
        assert "templates/project" in content

    def test_creates_kanban_structure(self):
        content = (SCRIPTS_DIR / "bootstrap_project.sh").read_text()
        assert ".kanban" in content

    def test_creates_claude_structure(self):
        content = (SCRIPTS_DIR / "bootstrap_project.sh").read_text()
        assert ".claude" in content

    def test_substitutes_project_name(self):
        content = (SCRIPTS_DIR / "bootstrap_project.sh").read_text()
        assert "PROJECT_NAME" in content

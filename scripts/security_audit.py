#!/usr/bin/env python3
"""
StoryForge Security Audit Tool

A cross-platform static analysis scanner that detects common security
vulnerabilities, leaked secrets, dangerous configurations, and risky patterns.

Designed to run at the end of each sprint as part of the StoryForge
delivery discipline.

Usage:
    python scripts/security_audit.py [path]           # Scan a project
    python scripts/security_audit.py [path] --json    # JSON output for CI
    python scripts/security_audit.py [path] --report  # Save markdown report

Requires: Python 3.8+ (stdlib only, no pip dependencies)
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# --- Configuration ---

# File extensions to scan for code vulnerabilities
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb", ".php",
    ".c", ".cpp", ".h", ".cs", ".rs", ".swift", ".kt", ".scala",
    ".sh", ".bash", ".ps1", ".bat", ".cmd",
    ".sql", ".html", ".htm", ".xml", ".yaml", ".yml", ".toml",
}

# File extensions for config scanning
CONFIG_EXTENSIONS = {
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".env", ".properties", ".xml", ".md",
}

# Directories to skip
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".tox", ".mypy_cache", ".pytest_cache", "dist", "build",
    ".next", ".nuxt", "vendor", "target", "bin", "obj",
}

# Files to exclude from code scanning (contain patterns as test data)
SELF_EXCLUDE = {"security_audit.py", "test_security_audit.py"}

# Max file size to scan (1 MB)
MAX_FILE_SIZE = 1_048_576

# Max files to scan
MAX_FILES = 5000


# --- Data Model ---

@dataclass
class Finding:
    severity: str          # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category: str          # secrets, injection, config, crypto, etc.
    title: str
    description: str
    file_path: str
    line_number: int = 0
    line_content: str = ""
    recommendation: str = ""


@dataclass
class AuditReport:
    timestamp: str = ""
    project_path: str = ""
    files_scanned: int = 0
    findings: list = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "CRITICAL")

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "HIGH")

    @property
    def medium_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "MEDIUM")

    @property
    def low_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "LOW")


# --- Secret Patterns ---

SECRET_PATTERNS = [
    # API Keys
    (r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{20,}', "API key", "CRITICAL"),
    (r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{20,}', "Secret key", "CRITICAL"),
    (r'(?i)(access[_-]?key|accesskey)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{20,}', "Access key", "CRITICAL"),

    # Tokens
    (r'(?i)(auth[_-]?token|bearer)\s*[=:]\s*["\']?[A-Za-z0-9_\-\.]{20,}', "Auth token", "CRITICAL"),
    (r'(?i)(jwt[_-]?secret)\s*[=:]\s*["\']?[A-Za-z0-9_\-]{16,}', "JWT secret", "CRITICAL"),
    (r'ghp_[A-Za-z0-9_]{36}', "GitHub personal access token", "CRITICAL"),
    (r'gho_[A-Za-z0-9_]{36}', "GitHub OAuth token", "CRITICAL"),
    (r'sk-[A-Za-z0-9]{32,}', "OpenAI/Anthropic API key pattern", "CRITICAL"),
    (r'xox[bprs]-[A-Za-z0-9\-]{10,}', "Slack token", "CRITICAL"),

    # Passwords
    (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{8,}["\']', "Hardcoded password", "CRITICAL"),
    (r'(?i)(db_password|database_password|mysql_pwd)\s*[=:]\s*["\']?[^\s"\']{8,}', "Database password", "CRITICAL"),

    # Connection strings
    (r'(?i)(mongodb|postgres|mysql|redis)://[^\s"\']+:[^\s"\']+@', "Database connection string with credentials", "CRITICAL"),

    # Private keys
    (r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', "Private key", "CRITICAL"),
    (r'-----BEGIN PGP PRIVATE KEY BLOCK-----', "PGP private key", "CRITICAL"),

    # AWS
    (r'AKIA[0-9A-Z]{16}', "AWS access key ID", "CRITICAL"),
    (r'(?i)aws_secret_access_key\s*[=:]\s*["\']?[A-Za-z0-9/+=]{40}', "AWS secret key", "CRITICAL"),
]

# --- Vulnerability Patterns ---

VULN_PATTERNS = {
    ".py": [
        (r'\beval\s*\(', "Unsafe eval()", "HIGH", "injection",
         "eval() can execute arbitrary code. Use ast.literal_eval() for data parsing."),
        (r'\bexec\s*\(', "Unsafe exec()", "HIGH", "injection",
         "exec() can execute arbitrary code. Avoid or sanitize input strictly."),
        (r'\bos\.system\s*\(', "os.system() command execution", "HIGH", "injection",
         "Use subprocess.run() with shell=False and argument lists instead."),
        (r'subprocess.*shell\s*=\s*True', "subprocess with shell=True", "MEDIUM", "injection",
         "shell=True enables shell injection. Use shell=False with argument lists."),
        (r'pickle\.loads?\s*\(', "Insecure deserialization (pickle)", "HIGH", "deserialization",
         "pickle can execute arbitrary code during deserialization. Use json or a safe alternative."),
        (r'yaml\.load\s*\([^)]*(?!Loader)', "Unsafe YAML load", "MEDIUM", "deserialization",
         "Use yaml.safe_load() instead of yaml.load() to prevent code execution."),
        (r'hashlib\.(md5|sha1)\s*\(', "Weak hash algorithm", "MEDIUM", "crypto",
         "MD5/SHA1 are cryptographically broken. Use SHA-256 or better."),
        (r'(?i)\bDEBUG\s*=\s*True', "Debug mode enabled", "MEDIUM", "config",
         "Ensure DEBUG is False in production deployments."),
        (r'verify\s*=\s*False', "SSL verification disabled", "HIGH", "crypto",
         "Disabling SSL verification allows man-in-the-middle attacks."),
        (r'__import__\s*\(', "Dynamic import", "MEDIUM", "injection",
         "Dynamic imports can load malicious modules. Validate input if necessary."),
    ],
    ".js": [
        (r'\beval\s*\(', "Unsafe eval()", "HIGH", "injection",
         "eval() can execute arbitrary code. Use JSON.parse() for data."),
        (r'innerHTML\s*=', "innerHTML assignment (XSS risk)", "MEDIUM", "xss",
         "Use textContent or a sanitization library instead of innerHTML."),
        (r'document\.write\s*\(', "document.write() (XSS risk)", "MEDIUM", "xss",
         "Avoid document.write(). Use DOM manipulation methods."),
        (r'child_process.*exec\s*\(', "Command execution", "HIGH", "injection",
         "Use execFile() with argument arrays instead of exec() with string commands."),
        (r'new\s+Function\s*\(', "Dynamic function creation", "HIGH", "injection",
         "new Function() is equivalent to eval(). Avoid with untrusted input."),
        (r'(?i)cors.*origin.*\*', "Wildcard CORS origin", "MEDIUM", "config",
         "Restrict CORS origins to specific trusted domains."),
        (r'(?i)nosql.*\$where', "NoSQL injection ($where)", "HIGH", "injection",
         "Avoid $where with user input. Use parameterized queries."),
    ],
    ".ts": [],  # Inherits from .js
    ".go": [
        (r'fmt\.Sprintf\s*\(.*%s.*sql', "Potential SQL injection via Sprintf", "HIGH", "injection",
         "Use parameterized queries instead of string formatting for SQL."),
        (r'exec\.Command\s*\(', "Command execution", "MEDIUM", "injection",
         "Validate and sanitize all arguments passed to exec.Command()."),
        (r'crypto/md5|crypto/sha1', "Weak hash import", "MEDIUM", "crypto",
         "Use crypto/sha256 or better for security-sensitive hashing."),
    ],
    ".sh": [
        (r'eval\s+', "eval in shell script", "HIGH", "injection",
         "Avoid eval with variable input. It can execute arbitrary commands."),
        (r'\$\{.*:-.*\}.*rm\b', "Dangerous default expansion with rm", "HIGH", "injection",
         "Ensure variables are validated before use in destructive commands."),
        (r'curl.*\|\s*(?:ba)?sh', "Pipe curl to shell", "CRITICAL", "injection",
         "Never pipe untrusted URLs directly to shell execution."),
        (r'chmod\s+777', "World-writable permissions", "MEDIUM", "config",
         "Use restrictive permissions (e.g., 755 or 700)."),
    ],
    ".sql": [
        (r'GRANT\s+ALL\s+PRIVILEGES', "Excessive database privileges", "MEDIUM", "config",
         "Grant only the minimum required privileges."),
        (r"(?i)password\s*=\s*'[^']+'", "Hardcoded password in SQL", "HIGH", "secrets",
         "Use environment variables or secret management for passwords."),
    ],
    ".php": [
        (r'\beval\s*\(', "Unsafe eval()", "HIGH", "injection",
         "eval() can execute arbitrary code. Avoid with user input."),
        (r'\bsystem\s*\(|\bexec\s*\(|\bpassthru\s*\(', "Command execution", "HIGH", "injection",
         "Sanitize all input to command execution functions."),
        (r'\bmysqli?_query\s*\(.*\$', "Potential SQL injection", "HIGH", "injection",
         "Use prepared statements with parameter binding."),
    ],
}

# .ts and .tsx inherit from .js
VULN_PATTERNS[".ts"] = VULN_PATTERNS[".js"]
VULN_PATTERNS[".tsx"] = VULN_PATTERNS[".js"]
VULN_PATTERNS[".jsx"] = VULN_PATTERNS[".js"]
VULN_PATTERNS[".bash"] = VULN_PATTERNS[".sh"]


# --- Dangerous File Detection ---

DANGEROUS_FILES = [
    (".env", "CRITICAL", "Environment file may contain secrets"),
    (".env.local", "CRITICAL", "Local environment file may contain secrets"),
    (".env.production", "CRITICAL", "Production environment file with secrets"),
    (".env.development", "HIGH", "Development environment file"),
    ("id_rsa", "CRITICAL", "RSA private key"),
    ("id_ed25519", "CRITICAL", "ED25519 private key"),
    ("id_dsa", "CRITICAL", "DSA private key"),
    (".pem", "HIGH", "PEM certificate/key file"),
    (".p12", "HIGH", "PKCS#12 certificate file"),
    (".pfx", "HIGH", "PFX certificate file"),
    (".key", "HIGH", "Private key file"),
    ("credentials.json", "CRITICAL", "Credentials file"),
    ("serviceAccountKey.json", "CRITICAL", "Service account key"),
    (".htpasswd", "HIGH", "Apache password file"),
    ("shadow", "CRITICAL", "Shadow password file"),
    ("wp-config.php", "HIGH", "WordPress config with DB credentials"),
]


# --- StoryForge Config Audit ---

def audit_storyforge_config(project_path: Path) -> list:
    """Audit StoryForge-specific configuration for security issues."""
    findings = []

    # Check settings.json files
    for settings_path in [
        project_path / ".claude" / "settings.json",
        project_path / "templates" / "home" / ".claude" / "settings.json",
        project_path / "templates" / "project" / ".claude" / "settings.json",
    ]:
        if not settings_path.is_file():
            continue

        try:
            with open(settings_path, encoding="utf-8") as f:
                settings = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        rel_path = str(settings_path.relative_to(project_path))
        perms = settings.get("permissions", {})

        # Check for bypassPermissions
        default_mode = perms.get("defaultMode", "")
        if default_mode == "bypassPermissions":
            findings.append(Finding(
                severity="CRITICAL",
                category="config",
                title="bypassPermissions mode enabled",
                description="Settings use bypassPermissions as default mode, which skips all safety checks.",
                file_path=rel_path,
                recommendation="Use 'default' or 'acceptEdits' mode. Only use bypassPermissions in isolated containers.",
            ))

        # Check for missing deny rules
        deny_rules = perms.get("deny", [])
        if not deny_rules:
            findings.append(Finding(
                severity="MEDIUM",
                category="config",
                title="No permission deny rules configured",
                description="Settings have no deny rules. Sensitive files like .env and .ssh are not protected.",
                file_path=rel_path,
                recommendation="Add deny rules for .env files and ~/.ssh/ at minimum.",
            ))

        # Check for overly permissive allow rules
        allow_rules = perms.get("allow", [])
        for rule in allow_rules:
            if rule in ("Bash(*)", "Bash(*)"):
                findings.append(Finding(
                    severity="HIGH",
                    category="config",
                    title="Blanket Bash(*) allow rule",
                    description="Allow rule permits all bash commands without restriction.",
                    file_path=rel_path,
                    recommendation="Use specific allow patterns like Bash(npm run *) instead of Bash(*).",
                ))

        # Check for auto mode without safeguards
        if default_mode == "auto":
            findings.append(Finding(
                severity="MEDIUM",
                category="config",
                title="Auto mode enabled as default",
                description="Auto mode allows Claude to take actions with reduced user oversight.",
                file_path=rel_path,
                recommendation="Consider using 'default' or 'acceptEdits' for sensitive projects.",
            ))

        # Check hooks for unsafe commands
        hooks = settings.get("hooks", {})
        unsafe_patterns = ["eval ", "| bash", "|bash", "chmod 777"]
        for event_name, event_hooks in hooks.items():
            for hook_entry in event_hooks:
                for hook in hook_entry.get("hooks", []):
                    cmd = hook.get("command", "")
                    for pattern in unsafe_patterns:
                        if pattern in cmd and event_name != "PreToolUse":
                            findings.append(Finding(
                                severity="HIGH",
                                category="config",
                                title=f"Unsafe command in {event_name} hook",
                                description=f"Hook contains potentially dangerous pattern: {pattern}",
                                file_path=rel_path,
                                recommendation="Review hook commands for security. Move dangerous patterns to PreToolUse blockers.",
                            ))

        # Check for missing PreToolUse hooks
        if hooks and "PreToolUse" not in hooks:
            findings.append(Finding(
                severity="MEDIUM",
                category="config",
                title="No PreToolUse safety hooks configured",
                description="Settings have hooks but no PreToolUse guards. Dangerous commands can execute without pre-validation.",
                file_path=rel_path,
                recommendation="Add PreToolUse hooks to block rm -rf /, force push, and other dangerous commands.",
            ))

    return findings


# --- Scanning Engine ---

def collect_files(project_path: Path) -> list:
    """Collect files to scan, respecting skip dirs and size limits."""
    files = []
    for root, dirs, filenames in os.walk(project_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in filenames:
            if len(files) >= MAX_FILES:
                return files

            filepath = Path(root) / filename
            suffix = filepath.suffix.lower()

            if suffix not in CODE_EXTENSIONS and suffix not in CONFIG_EXTENSIONS:
                # Still check for dangerous filenames
                base = filepath.name.lower()
                is_dangerous = any(
                    base == df[0].lower() or base.endswith(df[0].lower())
                    for df in DANGEROUS_FILES
                )
                if not is_dangerous:
                    continue

            try:
                if filepath.stat().st_size > MAX_FILE_SIZE:
                    continue
            except OSError:
                continue

            files.append(filepath)

    return files


def scan_file_secrets(filepath: Path, content: str, rel_path: str) -> list:
    """Scan a file for hardcoded secrets."""
    findings = []
    for line_num, line in enumerate(content.splitlines(), 1):
        for pattern, name, severity in SECRET_PATTERNS:
            if re.search(pattern, line):
                # Skip comments and test files
                stripped = line.strip()
                if stripped.startswith(("#", "//", "*", "/*", "<!--")):
                    continue
                if "example" in line.lower() or "placeholder" in line.lower():
                    continue
                if "test" in rel_path.lower() and "fixture" in rel_path.lower():
                    continue

                findings.append(Finding(
                    severity=severity,
                    category="secrets",
                    title=f"Potential {name} detected",
                    description=f"Pattern matching suggests a {name} may be present in source code.",
                    file_path=rel_path,
                    line_number=line_num,
                    line_content=stripped[:120],
                    recommendation="Move secrets to environment variables or a secret manager. Never commit secrets to version control.",
                ))
                break  # One finding per line

    return findings


def scan_file_vulns(filepath: Path, content: str, rel_path: str) -> list:
    """Scan a file for vulnerability patterns."""
    findings = []
    suffix = filepath.suffix.lower()
    patterns = VULN_PATTERNS.get(suffix, [])

    for line_num, line in enumerate(content.splitlines(), 1):
        for pattern, title, severity, category, recommendation in patterns:
            if re.search(pattern, line):
                stripped = line.strip()
                # Skip comments
                if stripped.startswith(("#", "//", "*", "/*")):
                    continue

                findings.append(Finding(
                    severity=severity,
                    category=category,
                    title=title,
                    description=f"Potentially dangerous pattern found.",
                    file_path=rel_path,
                    line_number=line_num,
                    line_content=stripped[:120],
                    recommendation=recommendation,
                ))

    return findings


def scan_dangerous_files(project_path: Path, files: list) -> list:
    """Check for dangerous files that should not be in the repository."""
    findings = []

    for filepath in files:
        base = filepath.name.lower()
        for dangerous_name, severity, description in DANGEROUS_FILES:
            if base == dangerous_name.lower() or (dangerous_name.startswith(".") and base.endswith(dangerous_name.lower())):
                rel_path = str(filepath.relative_to(project_path))
                # Skip template files
                if "template" in rel_path.lower() or "example" in rel_path.lower():
                    continue
                findings.append(Finding(
                    severity=severity,
                    category="secrets",
                    title=f"Dangerous file in repository: {filepath.name}",
                    description=description,
                    file_path=rel_path,
                    recommendation="Remove from version control and add to .gitignore.",
                ))
                break

    return findings


def check_gitignore(project_path: Path) -> list:
    """Check if .gitignore covers sensitive patterns."""
    findings = []
    gitignore = project_path / ".gitignore"

    if not gitignore.is_file():
        findings.append(Finding(
            severity="MEDIUM",
            category="config",
            title="No .gitignore file",
            description="Project has no .gitignore. Sensitive files may be committed accidentally.",
            file_path=".gitignore",
            recommendation="Create a .gitignore with patterns for .env, *.key, *.pem, etc.",
        ))
        return findings

    content = gitignore.read_text(encoding="utf-8", errors="replace")
    essential_patterns = [
        (".env", "Environment files"),
        ("*.key", "Private key files"),
        ("*.pem", "Certificate/key files"),
    ]

    for pattern, description in essential_patterns:
        if pattern not in content:
            findings.append(Finding(
                severity="LOW",
                category="config",
                title=f".gitignore missing pattern: {pattern}",
                description=f"{description} are not excluded from version control.",
                file_path=".gitignore",
                recommendation=f"Add '{pattern}' to .gitignore.",
            ))

    return findings


def run_audit(project_path: Path) -> AuditReport:
    """Run the complete security audit."""
    report = AuditReport(
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        project_path=str(project_path),
    )

    # Collect files
    files = collect_files(project_path)
    report.files_scanned = len(files)

    # Scan each file
    for filepath in files:
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        rel_path = str(filepath.relative_to(project_path))

        # Skip self-referential scanning (the audit script contains patterns as strings)
        if filepath.name in SELF_EXCLUDE:
            continue

        # Secret scanning
        report.findings.extend(scan_file_secrets(filepath, content, rel_path))

        # Vulnerability pattern scanning
        report.findings.extend(scan_file_vulns(filepath, content, rel_path))

    # Dangerous file detection
    report.findings.extend(scan_dangerous_files(project_path, files))

    # Gitignore check
    report.findings.extend(check_gitignore(project_path))

    # StoryForge config audit
    report.findings.extend(audit_storyforge_config(project_path))

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    report.findings.sort(key=lambda f: (severity_order.get(f.severity, 5), f.category))

    return report


# --- Output Rendering ---

class Colors:
    ENABLED = True
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

    @classmethod
    def disable(cls):
        cls.ENABLED = False

    @classmethod
    def c(cls, color: str, text: str) -> str:
        if not cls.ENABLED:
            return text
        return f"{color}{text}{cls.RESET}"


SEVERITY_COLORS = {
    "CRITICAL": Colors.RED + Colors.BOLD,
    "HIGH": Colors.RED,
    "MEDIUM": Colors.YELLOW,
    "LOW": Colors.BLUE,
    "INFO": Colors.DIM,
}

SEVERITY_ICONS = {
    "CRITICAL": "!!!",
    "HIGH": " !! ",
    "MEDIUM": "  ! ",
    "LOW": "  - ",
    "INFO": "  i ",
}


def render_terminal(report: AuditReport) -> str:
    """Render audit report for terminal display."""
    lines = []
    width = min(os.get_terminal_size().columns if sys.stdout.isatty() else 100, 100)

    lines.append(Colors.c(Colors.CYAN, "=" * width))
    lines.append(Colors.c(Colors.BOLD + Colors.CYAN, "  STORYFORGE SECURITY AUDIT"))
    lines.append(Colors.c(Colors.CYAN, "=" * width))
    lines.append("")
    lines.append(f"  Project:  {report.project_path}")
    lines.append(f"  Scanned:  {report.files_scanned} files")
    lines.append(f"  Date:     {report.timestamp[:10]}")
    lines.append("")

    # Summary bar
    c = report.critical_count
    h = report.high_count
    m = report.medium_count
    l = report.low_count
    total = len(report.findings)

    if c > 0:
        status = Colors.c(Colors.RED + Colors.BOLD, "CRITICAL ISSUES FOUND")
    elif h > 0:
        status = Colors.c(Colors.RED, "HIGH SEVERITY ISSUES FOUND")
    elif m > 0:
        status = Colors.c(Colors.YELLOW, "MEDIUM SEVERITY ISSUES FOUND")
    elif l > 0:
        status = Colors.c(Colors.BLUE, "LOW SEVERITY ISSUES ONLY")
    else:
        status = Colors.c(Colors.GREEN + Colors.BOLD, "NO ISSUES FOUND")

    lines.append(f"  Status:   {status}")
    lines.append(f"  Findings: {Colors.c(Colors.RED, str(c))} critical, "
                 f"{Colors.c(Colors.RED, str(h))} high, "
                 f"{Colors.c(Colors.YELLOW, str(m))} medium, "
                 f"{Colors.c(Colors.BLUE, str(l))} low")
    lines.append("")

    if not report.findings:
        lines.append(Colors.c(Colors.GREEN, "  No security issues detected. Clean scan."))
        lines.append("")
        lines.append(Colors.c(Colors.DIM, "-" * width))
        return "\n".join(lines)

    # Group by category
    categories = {}
    for finding in report.findings:
        categories.setdefault(finding.category, []).append(finding)

    for category, findings in categories.items():
        lines.append(Colors.c(Colors.BOLD, f"  {category.upper()} ({len(findings)} finding{'s' if len(findings) != 1 else ''})"))
        lines.append("")

        for f in findings:
            color = SEVERITY_COLORS.get(f.severity, "")
            icon = SEVERITY_ICONS.get(f.severity, "")
            lines.append(f"  {Colors.c(color, icon)} {Colors.c(Colors.BOLD, f.title)}")
            lines.append(f"       {f.file_path}" + (f":{f.line_number}" if f.line_number else ""))
            if f.line_content:
                lines.append(f"       {Colors.c(Colors.DIM, f.line_content[:80])}")
            if f.recommendation:
                lines.append(f"       {Colors.c(Colors.CYAN, 'Fix: ' + f.recommendation[:90])}")
            lines.append("")

    lines.append(Colors.c(Colors.DIM, "-" * width))
    lines.append(Colors.c(Colors.DIM, "  StoryForge Security Audit • Run after each sprint"))
    return "\n".join(lines)


def render_markdown(report: AuditReport) -> str:
    """Render audit report as markdown."""
    lines = []
    lines.append("# Security Audit Report")
    lines.append("")
    lines.append(f"**Date**: {report.timestamp}")
    lines.append(f"**Project**: {report.project_path}")
    lines.append(f"**Files scanned**: {report.files_scanned}")
    lines.append("")

    c = report.critical_count
    h = report.high_count
    m = report.medium_count
    l = report.low_count

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Severity | Count |")
    lines.append(f"|:---------|------:|")
    lines.append(f"| Critical | {c} |")
    lines.append(f"| High | {h} |")
    lines.append(f"| Medium | {m} |")
    lines.append(f"| Low | {l} |")
    lines.append(f"| **Total** | **{len(report.findings)}** |")
    lines.append("")

    if not report.findings:
        lines.append("**No security issues detected.** Clean scan.")
        return "\n".join(lines)

    lines.append("## Findings")
    lines.append("")

    for f in report.findings:
        lines.append(f"### [{f.severity}] {f.title}")
        lines.append("")
        lines.append(f"- **Category**: {f.category}")
        lines.append(f"- **File**: `{f.file_path}`" + (f" (line {f.line_number})" if f.line_number else ""))
        if f.line_content:
            lines.append(f"- **Code**: `{f.line_content[:100]}`")
        lines.append(f"- **Description**: {f.description}")
        if f.recommendation:
            lines.append(f"- **Recommendation**: {f.recommendation}")
        lines.append("")

    return "\n".join(lines)


def render_json(report: AuditReport) -> str:
    """Render audit report as JSON."""
    data = {
        "timestamp": report.timestamp,
        "project_path": report.project_path,
        "files_scanned": report.files_scanned,
        "summary": {
            "total": len(report.findings),
            "critical": report.critical_count,
            "high": report.high_count,
            "medium": report.medium_count,
            "low": report.low_count,
        },
        "findings": [asdict(f) for f in report.findings],
    }
    return json.dumps(data, indent=2)


# --- Entry Point ---

def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, TypeError):
            pass

    args = sys.argv[1:]
    json_output = "--json" in args
    save_report = "--report" in args
    project_path = None

    for arg in args:
        if not arg.startswith("--"):
            project_path = Path(arg).resolve()
            break

    if project_path is None:
        project_path = Path.cwd()

    if not project_path.is_dir():
        print(f"Error: {project_path} is not a directory", file=sys.stderr)
        sys.exit(2)

    if not json_output:
        if not (os.environ.get("NO_COLOR") or not sys.stdout.isatty()):
            if sys.platform == "win32":
                try:
                    import ctypes
                    ctypes.windll.kernel32.SetConsoleMode(
                        ctypes.windll.kernel32.GetStdHandle(-11), 7
                    )
                except Exception:
                    if not os.environ.get("WT_SESSION"):
                        Colors.disable()
            # Unix: colors enabled by default if isatty
        else:
            Colors.disable()

    # Run audit
    report = run_audit(project_path)

    # Output
    if json_output:
        print(render_json(report))
    else:
        print(render_terminal(report))

    # Save markdown report
    if save_report:
        report_dir = project_path / ".kanban" / "security-reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        date_str = report.timestamp[:10]
        report_file = report_dir / f"security-audit-{date_str}.md"
        report_file.write_text(render_markdown(report), encoding="utf-8")
        if not json_output:
            print(f"\n  Report saved to {report_file}")

    # Exit code based on severity
    if report.critical_count > 0:
        sys.exit(1)
    elif report.high_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

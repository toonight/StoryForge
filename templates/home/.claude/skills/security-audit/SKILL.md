---
name: security-audit
description: Run a comprehensive security audit on the current project. Scans for secrets, vulnerabilities, dangerous configs, and risky patterns. Use at the end of each sprint or before releases.
disable-model-invocation: true
---

# Security Audit

Run a comprehensive security audit on the current project.

## Instructions

### Quick Scan (automated only)

Run the StoryForge security scanner:

```bash
python scripts/security_audit.py . --report
```

This will:
- Scan all code files for vulnerability patterns
- Check for hardcoded secrets and leaked credentials
- Detect dangerous files (.env, private keys)
- Audit StoryForge configuration for unsafe settings
- Save a markdown report to `.kanban/security-reports/`

### Full Audit (automated + manual)

For a complete audit, delegate to the `security-auditor` agent which will:
1. Run the automated scanner
2. Perform manual code review for auth, input validation, config issues
3. Run dependency audit if lock files exist
4. Generate a comprehensive report
5. Create Stories for critical and high findings

### Interpreting Results

| Exit Code | Meaning |
|---|---|
| 0 | No critical or high issues |
| 1 | Critical or high issues found (requires action) |
| 2 | Script error |

### After the Audit

1. Review the report in `.kanban/security-reports/`
2. For each CRITICAL/HIGH finding: create a Story with `/story-write`
3. For MEDIUM findings: add to backlog for future sprints
4. After fixing: re-run the audit to verify
5. Update `.kanban/changelog.md` with audit results

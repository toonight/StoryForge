#!/usr/bin/env python3
"""
StoryForge Release Validator

Validates the entire repo from a new user's perspective:
- All agent files match Claude Code spec
- All skill files match Claude Code spec
- Settings.json uses only valid fields and hook events
- Rules files have paths frontmatter
- CLAUDE.md files are under 200 lines
- Project templates are complete
- Scripts have shebangs and Bash/PS parity
- Docs exist and README links work
- Baseline hashes are complete

Usage:
    python scripts/validate_release.py
"""

import json
import re
import sys
from pathlib import Path

root = Path(__file__).parent.parent
errors = []
warnings = []


def ok(msg):
    print(f"  OK  {msg}")


def err(msg):
    errors.append(msg)
    print(f"  ERR {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"  !!! {msg}")


def parse_frontmatter(content):
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    return parts[1].strip(), parts[2].strip()


# ============================================================
print("=" * 60)
print("STORYFORGE RELEASE VALIDATION")
print("=" * 60)

# --- AGENTS ---
print("\n[AGENTS]")
agents_dir = root / "templates" / "home" / ".claude" / "agents"
for f in sorted(agents_dir.glob("*.md")):
    name = f.stem
    content = f.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    if fm is None:
        err(f"Agent {name}: missing or broken frontmatter")
        continue

    fm_name = re.search(r"^name:\s*(.+)$", fm, re.M)
    fm_desc = re.search(r"^description:\s*(.+)$", fm, re.M)

    if not fm_name:
        err(f"Agent {name}: missing name field")
    elif fm_name.group(1).strip() != name:
        err(f"Agent {name}: name '{fm_name.group(1).strip()}' != filename")

    if not fm_desc:
        err(f"Agent {name}: missing description")
    elif len(fm_desc.group(1).strip()) > 250:
        warn(f"Agent {name}: description > 250 chars")

    if not re.match(r"^[a-z][a-z0-9-]*$", name):
        err(f"Agent {name}: invalid name format")

    if len(body) < 50:
        warn(f"Agent {name}: very short prompt ({len(body)} chars)")

    ok(name)

# --- SKILLS ---
print("\n[SKILLS]")
skills_dir = root / "templates" / "home" / ".claude" / "skills"
valid_skill_fields = {
    "name", "description", "argument-hint", "disable-model-invocation",
    "user-invocable", "allowed-tools", "model", "effort", "context",
    "agent", "hooks", "paths", "shell",
}
for skill_dir in sorted(skills_dir.iterdir()):
    if not skill_dir.is_dir():
        continue
    sf = skill_dir / "SKILL.md"
    name = skill_dir.name

    if not sf.exists():
        err(f"Skill {name}: missing SKILL.md")
        continue

    content = sf.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    if fm is None:
        err(f"Skill {name}: missing or broken frontmatter")
        continue

    fm_name = re.search(r"^name:\s*(.+)$", fm, re.M)
    if not fm_name:
        err(f"Skill {name}: missing name field")
    elif fm_name.group(1).strip() != name:
        err(f"Skill {name}: name '{fm_name.group(1).strip()}' != dirname")

    if not re.match(r"^[a-z][a-z0-9-]*$", name):
        err(f"Skill {name}: invalid name format")

    for line in fm.splitlines():
        m = re.match(r"^([a-z][a-z-]*):", line)
        if m and m.group(1) not in valid_skill_fields:
            err(f"Skill {name}: unsupported field '{m.group(1)}'")

    ok(name)

# --- SETTINGS.JSON ---
print("\n[SETTINGS.JSON]")
valid_hook_events = {
    "SessionStart", "InstructionsLoaded", "UserPromptSubmit",
    "PreToolUse", "PermissionRequest", "PostToolUse",
    "PostToolUseFailure", "Notification", "SubagentStart",
    "SubagentStop", "TaskCreated", "TaskCompleted", "TeammateIdle",
    "Stop", "StopFailure", "SessionEnd", "ConfigChange",
    "CwdChanged", "FileChanged", "WorktreeCreate", "WorktreeRemove",
    "PreCompact", "PostCompact", "Elicitation", "ElicitationResult",
}
valid_hook_types = {"command", "http", "prompt", "agent"}

for sp in [
    root / "templates" / "home" / ".claude" / "settings.json",
    root / "templates" / "project" / ".claude" / "settings.json",
]:
    rel = str(sp.relative_to(root))
    try:
        data = json.loads(sp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"{rel}: invalid JSON: {e}")
        continue

    hooks = data.get("hooks", {})
    for event, groups in hooks.items():
        if event not in valid_hook_events:
            err(f"{rel}: unsupported hook event '{event}'")
        for group in groups:
            if "hooks" not in group:
                err(f"{rel}: hook group in {event} missing 'hooks' array")
            else:
                for hook in group["hooks"]:
                    htype = hook.get("type")
                    if htype not in valid_hook_types:
                        err(f"{rel}: hook type '{htype}' invalid in {event}")

    ok(rel)

# --- RULES ---
print("\n[RULES FILES]")
for rules_dir in [
    root / "templates" / "home" / ".claude" / "rules",
    root / "templates" / "project" / ".claude" / "rules",
    root / ".claude" / "rules",
]:
    if not rules_dir.exists():
        continue
    for f in sorted(rules_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        rel = str(f.relative_to(root))
        if fm is None or "paths:" not in fm:
            err(f"{rel}: missing paths frontmatter (required for rules)")
        else:
            ok(rel)

# --- CLAUDE.MD ---
print("\n[CLAUDE.MD FILES]")
for cp in [
    root / "templates" / "home" / ".claude" / "CLAUDE.md",
    root / "templates" / "project" / ".claude" / "CLAUDE.md",
    root / ".claude" / "CLAUDE.md",
]:
    if not cp.exists():
        continue
    content = cp.read_text(encoding="utf-8")
    lines = content.count("\n")
    rel = str(cp.relative_to(root))
    if lines > 200:
        warn(f"{rel}: {lines} lines (Anthropic recommends < 200)")
    if len(content) < 100:
        err(f"{rel}: suspiciously short ({len(content)} chars)")
    ok(f"{rel} ({lines} lines)")

# --- PROJECT TEMPLATE ---
print("\n[PROJECT TEMPLATE COMPLETENESS]")
required = [
    "templates/project/.claude/CLAUDE.md",
    "templates/project/.claude/settings.json",
    "templates/project/.claude/rules/kanban.md",
    "templates/project/.kanban/board.md",
    "templates/project/.kanban/backlog.md",
    "templates/project/.kanban/sprint.md",
    "templates/project/.kanban/decisions.md",
    "templates/project/.kanban/changelog.md",
    "templates/project/.kanban/stories/STORY-TEMPLATE.md",
]
for fpath in required:
    if (root / fpath).exists():
        ok(fpath)
    else:
        err(f"{fpath}: MISSING")

# Story template sections
st = (root / "templates" / "project" / ".kanban" / "stories" / "STORY-TEMPLATE.md").read_text(encoding="utf-8")
for section in ["Acceptance Criteria", "Non-Goals", "Depends-On", "GitHub",
                "Implementation Notes", "Risks", "Follow-ups"]:
    if section not in st:
        err(f"Story template: missing '{section}'")

# --- SCRIPTS ---
print("\n[SCRIPTS]")
bash_scripts = sorted((root / "scripts").glob("*.sh"))
ps_scripts = sorted((root / "scripts").glob("*.ps1"))
py_scripts = sorted((root / "scripts").glob("*.py"))

bash_names = {s.stem for s in bash_scripts}
ps_names = {s.stem for s in ps_scripts}
missing_ps = bash_names - ps_names
if missing_ps:
    err(f"Bash without PowerShell: {missing_ps}")

for s in bash_scripts:
    c = s.read_text(encoding="utf-8")
    if not c.startswith("#!"):
        err(f"{s.name}: missing shebang")
    if "set -e" not in c:
        err(f"{s.name}: missing set -e")
    ok(s.name)

for s in ps_scripts:
    c = s.read_text(encoding="utf-8")
    if "#Requires" not in c:
        warn(f"{s.name}: missing #Requires")
    ok(s.name)

for s in py_scripts:
    ok(s.name)

# --- DOCS ---
print("\n[DOCUMENTATION]")
required_docs = [
    "docs/architecture.md",
    "docs/operating-model.md",
    "docs/source-of-truth-policy.md",
    "docs/anthropic-source-map.md",
    "docs/upstream/doc-index.md",
    "docs/upstream/release-watch.md",
    "docs/upstream/changelog-adaptation-process.md",
    "docs/upstream/baseline-hashes.json",
]
for d in required_docs:
    if (root / d).exists():
        ok(d)
    else:
        err(f"{d}: MISSING")

bl = json.loads((root / "docs" / "upstream" / "baseline-hashes.json").read_text(encoding="utf-8"))
if len(bl) < 14:
    err(f"Baseline: only {len(bl)} pages (expected >= 14)")
else:
    ok(f"baseline-hashes.json: {len(bl)} pages")

# --- README LINKS ---
print("\n[README LINKS]")
readme = (root / "README.md").read_text(encoding="utf-8")
md_links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", readme)
for text, link in md_links:
    if link.startswith("http") or link.startswith("#"):
        continue
    if (root / link).exists():
        ok(f"[{text}]({link})")
    else:
        err(f"README broken link: [{text}]({link})")

# --- SUMMARY ---
print("\n" + "=" * 60)
print(f"ERRORS:   {len(errors)}")
print(f"WARNINGS: {len(warnings)}")
print("=" * 60)

if errors:
    print("\nERRORS:")
    for e in errors:
        print(f"  x {e}")

if warnings:
    print("\nWARNINGS:")
    for w in warnings:
        print(f"  ! {w}")

if not errors and not warnings:
    print("\nALL VALIDATIONS PASSED - READY FOR RELEASE")
elif not errors:
    print("\nNO ERRORS - warnings are non-blocking")
else:
    print(f"\nFIX {len(errors)} ERROR(S) BEFORE RELEASE")
    sys.exit(1)

---
paths:
  - "scripts/**/*"
---

# Script Rules

When editing files under scripts/:

- All scripts must start with #!/usr/bin/env bash
- All scripts must use set -euo pipefail
- Scripts must work in Git Bash on Windows and native bash on macOS/Linux
- Use $STORYFORGE_ROOT for absolute paths within the repo
- Avoid Windows-specific commands (use POSIX equivalents)
- Quote all variable expansions
- Test with: bash -n <script> for syntax, then python -m pytest tests/test_scripts.py

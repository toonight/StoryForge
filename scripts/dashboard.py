#!/usr/bin/env python3
"""
StoryForge Kanban Dashboard

A cross-platform CLI tool that parses .kanban/ artifacts and displays
a formatted dashboard in the terminal.

Usage:
    python scripts/dashboard.py [path-to-project]

If no path is given, uses the current directory.

Requires: Python 3.8+ (stdlib only, no pip dependencies)
"""

import os
import re
import sys
from pathlib import Path


# --- Terminal colors (graceful fallback) ---

class Colors:
    """ANSI color codes with graceful fallback for terminals that don't support them."""

    ENABLED = True

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"

    @classmethod
    def disable(cls):
        cls.ENABLED = False

    @classmethod
    def c(cls, color: str, text: str) -> str:
        if not cls.ENABLED:
            return text
        return f"{color}{text}{cls.RESET}"


def _detect_color_support() -> bool:
    """Detect if terminal supports ANSI colors."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if sys.platform == "win32":
        # Windows 10+ supports ANSI if running in modern terminal
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable ANSI on Windows
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return os.environ.get("WT_SESSION") is not None  # Windows Terminal
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


# --- Markdown Parsing ---

def parse_table_rows(text: str) -> list[dict[str, str]]:
    """Parse markdown table rows into list of dicts."""
    lines = text.strip().splitlines()
    if len(lines) < 2:
        return []

    # Find header line and separator
    header_line = None
    data_start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|") and "---" not in stripped:
            if header_line is None:
                header_line = stripped
                continue
            elif "|---" in lines[i - 1] if i > 0 else False:
                # Previous line was separator, this is data
                data_start = i
                break
        elif "---" in stripped and "|" in stripped:
            data_start = i + 1
            continue

    if header_line is None:
        return []

    headers = [h.strip() for h in header_line.split("|") if h.strip()]

    rows = []
    for line in lines[data_start:]:
        stripped = line.strip()
        if not stripped or not stripped.startswith("|"):
            continue
        if "---" in stripped:
            continue
        cells = [c.strip() for c in stripped.split("|") if c.strip()]
        if len(cells) >= len(headers):
            row = {}
            for j, header in enumerate(headers):
                row[header] = cells[j] if j < len(cells) else ""
            rows.append(row)

    return rows


def extract_section(text: str, heading: str) -> str:
    """Extract content under a markdown heading (### level)."""
    pattern = rf"^###?\s+{re.escape(heading)}\s*$"
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.IGNORECASE):
            start = i + 1
            break

    if start is None:
        return ""

    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].startswith("##"):
            end = i
            break

    return "\n".join(lines[start:end]).strip()


def count_checkboxes(text: str) -> tuple[int, int]:
    """Count checked and total checkboxes in text. Returns (checked, total)."""
    checked = len(re.findall(r"- \[x\]", text, re.IGNORECASE))
    unchecked = len(re.findall(r"- \[ \]", text))
    return checked, checked + unchecked


# --- Data Loading ---

class KanbanData:
    """Loads and holds all .kanban/ data."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.kanban_dir = project_dir / ".kanban"
        self.board_text = ""
        self.backlog_text = ""
        self.sprint_text = ""
        self.stories: dict[str, dict] = {}
        self.features: list[dict] = []
        self.board_sections: dict[str, list[dict]] = {}

    def load(self) -> bool:
        """Load all kanban files. Returns False if .kanban/ doesn't exist."""
        if not self.kanban_dir.is_dir():
            return False

        board_path = self.kanban_dir / "board.md"
        if board_path.is_file():
            self.board_text = board_path.read_text(encoding="utf-8")
            self._parse_board()

        backlog_path = self.kanban_dir / "backlog.md"
        if backlog_path.is_file():
            self.backlog_text = backlog_path.read_text(encoding="utf-8")

        sprint_path = self.kanban_dir / "sprint.md"
        if sprint_path.is_file():
            self.sprint_text = sprint_path.read_text(encoding="utf-8")

        self._load_stories()
        self._parse_velocity()
        return True

    def _parse_velocity(self):
        """Parse sprint history to compute velocity metrics."""
        self.completed_sprints = []
        if not self.sprint_text:
            return

        # Parse completed sprints section
        in_completed = False
        current_sprint = None

        for line in self.sprint_text.splitlines():
            if line.strip().startswith("## Completed Sprints") or line.strip().startswith("### Sprint") and "(" in line:
                in_completed = True

            if in_completed and (line.startswith("### ") or line.startswith("## ")) and "Sprint" in line:
                # Extract sprint name and date range from parentheses
                sprint_name = line.lstrip("#").strip()
                current_sprint = {"name": sprint_name, "done": 0, "total": 0}

            if in_completed and current_sprint and line.strip().startswith("Result:"):
                # Parse "Result: 8/8 stories completed"
                m = re.search(r"(\d+)/(\d+)", line)
                if m:
                    current_sprint["done"] = int(m.group(1))
                    current_sprint["total"] = int(m.group(2))
                    self.completed_sprints.append(current_sprint)
                    current_sprint = None

            # Also parse table rows in completed sprints for Done counts
            if in_completed and current_sprint and line.strip().startswith("|") and "Done" in line:
                current_sprint["done"] += 1
                current_sprint["total"] += 1

    def get_blocked_stories(self) -> list:
        """Find stories blocked by incomplete dependencies."""
        blocked = []
        for story_id, story in self.stories.items():
            if story["status"] in ("Done", "Backlog"):
                continue
            for dep_id in story.get("depends_on", []):
                dep = self.stories.get(dep_id)
                if dep and dep["status"] != "Done":
                    blocked.append((story_id, dep_id, dep["status"]))
        return blocked

    def _parse_board(self):
        """Parse board.md into sections and features."""
        # Parse features table
        features_section = extract_section(self.board_text, "Features")
        if features_section:
            self.features = parse_table_rows(features_section)

        # Parse board columns
        for column in ["Backlog", "Ready", "In Progress", "Review", "Done"]:
            section = extract_section(self.board_text, column)
            if section:
                rows = parse_table_rows(section)
                self.board_sections[column] = rows
            else:
                self.board_sections[column] = []

    def _load_stories(self):
        """Load all story files."""
        stories_dir = self.kanban_dir / "stories"
        if not stories_dir.is_dir():
            return

        for story_file in sorted(stories_dir.glob("STORY-*.md")):
            story_id = story_file.stem
            text = story_file.read_text(encoding="utf-8")
            status = ""
            title = story_id
            feature = ""

            depends_on = []
            github_ref = ""

            # Parse header
            for line in text.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                elif "**Status**" in line:
                    status = line.split(":")[-1].strip().rstrip("*").strip()
                elif "**Feature**" in line:
                    feature = line.split(":")[-1].strip().rstrip("*").strip()
                elif "**Depends-On**" in line:
                    dep_val = line.split(":")[-1].strip().rstrip("*").strip()
                    if dep_val and dep_val != "(none)":
                        depends_on = [d.strip() for d in re.split(r"[,;]", dep_val) if d.strip().startswith("STORY-")]
                elif "**GitHub**" in line:
                    gh_val = line.split(":", 1)[-1].strip().rstrip("*").strip()
                    if gh_val and gh_val != "(none)":
                        github_ref = gh_val

            checked, total = count_checkboxes(text)

            self.stories[story_id] = {
                "id": story_id,
                "title": title,
                "status": status,
                "feature": feature,
                "criteria_done": checked,
                "criteria_total": total,
                "depends_on": depends_on,
                "github_ref": github_ref,
                "text": text,
            }


# --- Dashboard Rendering ---

def get_terminal_width() -> int:
    """Get terminal width, defaulting to 80."""
    try:
        return os.get_terminal_size().columns
    except (ValueError, OSError):
        return 80


def render_header(project_name: str, width: int) -> str:
    """Render the dashboard header."""
    lines = []
    border = "═" * width
    lines.append(Colors.c(Colors.CYAN, border))
    title = f"  STORYFORGE DASHBOARD — {project_name}  "
    pad = max(0, (width - len(title)) // 2)
    lines.append(Colors.c(Colors.BOLD + Colors.CYAN, " " * pad + title))
    lines.append(Colors.c(Colors.CYAN, border))
    return "\n".join(lines)


def render_board_summary(data: KanbanData, width: int) -> str:
    """Render the Kanban board column summary."""
    lines = []
    lines.append("")
    lines.append(Colors.c(Colors.BOLD, "  KANBAN BOARD"))
    lines.append("")

    columns = ["Backlog", "Ready", "In Progress", "Review", "Done"]
    col_colors = {
        "Backlog": Colors.DIM,
        "Ready": Colors.YELLOW,
        "In Progress": Colors.BLUE,
        "Review": Colors.MAGENTA,
        "Done": Colors.GREEN,
    }
    col_icons = {
        "Backlog": "○",
        "Ready": "◉",
        "In Progress": "▶",
        "Review": "◈",
        "Done": "✓",
    }

    # Count stories per column
    counts = {}
    for col in columns:
        items = data.board_sections.get(col, [])
        counts[col] = len(items)

    total = sum(counts.values())

    # Render column bars
    col_width = max(12, (width - 10) // len(columns))
    header_line = "  "
    bar_line = "  "
    count_line = "  "

    for col in columns:
        color = col_colors[col]
        icon = col_icons[col]
        count = counts[col]
        label = f"{icon} {col}"
        header_line += Colors.c(color + Colors.BOLD, label.center(col_width))
        bar_line += Colors.c(color, ("█" * min(count, col_width - 2)).ljust(col_width))
        count_line += Colors.c(color, str(count).center(col_width))

    lines.append(header_line)
    lines.append(bar_line)
    lines.append(count_line)

    if total > 0:
        done_count = counts.get("Done", 0)
        pct = int((done_count / total) * 100)
        bar_len = width - 20
        filled = int(bar_len * done_count / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_len - filled)
        lines.append("")
        lines.append(f"  Progress: {Colors.c(Colors.GREEN, bar)} {pct}% ({done_count}/{total})")

    return "\n".join(lines)


def render_features(data: KanbanData, width: int) -> str:
    """Render features summary."""
    lines = []
    lines.append("")
    lines.append(Colors.c(Colors.BOLD, "  FEATURES"))
    lines.append("")

    if not data.features:
        lines.append("  (No features defined)")
        return "\n".join(lines)

    status_colors = {
        "Done": Colors.GREEN,
        "In Progress": Colors.BLUE,
        "Ready": Colors.YELLOW,
        "Backlog": Colors.DIM,
    }

    for feat in data.features:
        fid = feat.get("ID", "")
        title = feat.get("Title", "")
        status = feat.get("Status", "")
        color = status_colors.get(status, Colors.WHITE)
        status_badge = Colors.c(color, f"[{status}]")
        lines.append(f"  {Colors.c(Colors.DIM, fid)}  {title}  {status_badge}")

    return "\n".join(lines)


def render_active_stories(data: KanbanData, width: int) -> str:
    """Render details of In Progress stories."""
    lines = []
    lines.append("")
    lines.append(Colors.c(Colors.BOLD, "  ACTIVE STORIES"))
    lines.append("")

    active = [s for s in data.stories.values() if s["status"] == "In Progress"]
    if not active:
        lines.append(Colors.c(Colors.DIM, "  (No stories in progress)"))
        return "\n".join(lines)

    for story in active:
        sid = story["id"]
        title = story["title"]
        done = story["criteria_done"]
        total = story["criteria_total"]

        lines.append(f"  {Colors.c(Colors.BLUE + Colors.BOLD, '▶')} {Colors.c(Colors.BOLD, title)}")

        if total > 0:
            pct = int((done / total) * 100)
            bar_len = min(30, width - 30)
            filled = int(bar_len * done / total)
            bar = "█" * filled + "░" * (bar_len - filled)
            color = Colors.GREEN if pct == 100 else Colors.YELLOW if pct > 50 else Colors.RED
            lines.append(f"    Criteria: {Colors.c(color, bar)} {done}/{total} ({pct}%)")
        else:
            lines.append(f"    Criteria: {Colors.c(Colors.DIM, 'none defined')}")

        if story["feature"]:
            lines.append(f"    Feature:  {Colors.c(Colors.DIM, story['feature'])}")
        lines.append("")

    return "\n".join(lines)


def render_sprint(data: KanbanData, width: int) -> str:
    """Render sprint summary."""
    lines = []
    lines.append("")
    lines.append(Colors.c(Colors.BOLD, "  SPRINT"))
    lines.append("")

    if not data.sprint_text:
        lines.append(Colors.c(Colors.DIM, "  (No sprint defined)"))
        return "\n".join(lines)

    # Extract sprint name
    for line in data.sprint_text.splitlines():
        if line.startswith("## Current Sprint:"):
            sprint_name = line.replace("## Current Sprint:", "").strip()
            lines.append(f"  {Colors.c(Colors.CYAN, sprint_name)}")
            break

    # Parse sprint backlog table
    sprint_section = extract_section(data.sprint_text, "Sprint Backlog")
    if sprint_section:
        rows = parse_table_rows(sprint_section)
        if rows:
            done_count = sum(1 for r in rows if r.get("Status", "").strip() in ("Done", "Completed"))
            in_progress = sum(1 for r in rows if "Progress" in r.get("Status", ""))
            total = len(rows)

            lines.append(f"  Stories: {total} total, "
                         f"{Colors.c(Colors.GREEN, str(done_count))} done, "
                         f"{Colors.c(Colors.BLUE, str(in_progress))} in progress, "
                         f"{Colors.c(Colors.DIM, str(total - done_count - in_progress))} remaining")

            if total > 0:
                pct = int((done_count / total) * 100)
                bar_len = min(40, width - 20)
                filled = int(bar_len * done_count / total)
                bar = "█" * filled + "░" * (bar_len - filled)
                color = Colors.GREEN if pct == 100 else Colors.YELLOW
                lines.append(f"  Burndown: {Colors.c(color, bar)} {pct}%")

    # Extract goal
    for line in data.sprint_text.splitlines():
        if line.strip().startswith("- Goal:"):
            goal = line.split(":", 1)[1].strip()
            if goal and goal != "(TBD)":
                lines.append(f"  Goal:     {Colors.c(Colors.DIM, goal)}")
            break

    return "\n".join(lines)


def render_velocity(data: KanbanData, width: int) -> str:
    """Render sprint velocity metrics."""
    lines = []
    lines.append("")
    lines.append(Colors.c(Colors.BOLD, "  VELOCITY"))
    lines.append("")

    sprints = data.completed_sprints
    if not sprints:
        lines.append(Colors.c(Colors.DIM, "  (No completed sprints for velocity data)"))
        return "\n".join(lines)

    velocities = [s["done"] for s in sprints]
    avg = sum(velocities) / len(velocities) if velocities else 0
    trend = ""
    if len(velocities) >= 2:
        diff = velocities[-1] - velocities[-2]
        if diff > 0:
            trend = Colors.c(Colors.GREEN, f" ↑{diff}")
        elif diff < 0:
            trend = Colors.c(Colors.RED, f" ↓{abs(diff)}")
        else:
            trend = Colors.c(Colors.DIM, " →0")

    lines.append(f"  Average:  {Colors.c(Colors.CYAN, f'{avg:.1f}')} stories/sprint")
    if trend:
        lines.append(f"  Trend:    {velocities[-1]} (last){trend}")
    lines.append("")

    # Mini chart
    max_vel = max(velocities) if velocities else 1
    bar_max = min(30, width - 30)
    for i, sprint in enumerate(sprints[-5:]):  # Last 5 sprints
        v = sprint["done"]
        bar_len = int(bar_max * v / max_vel) if max_vel > 0 else 0
        bar = "█" * bar_len
        name = sprint["name"][:25]
        color = Colors.GREEN if v >= avg else Colors.YELLOW
        lines.append(f"  {Colors.c(Colors.DIM, name.ljust(26))} {Colors.c(color, bar)} {v}")

    return "\n".join(lines)


def render_dependencies(data: KanbanData, width: int) -> str:
    """Render blocked stories (dependency issues)."""
    blocked = data.get_blocked_stories()
    if not blocked:
        return ""

    lines = []
    lines.append("")
    lines.append(Colors.c(Colors.BOLD + Colors.RED, "  BLOCKED STORIES"))
    lines.append("")

    for story_id, dep_id, dep_status in blocked:
        story = data.stories[story_id]
        title = story["title"].split(":", 1)[-1].strip() if ":" in story["title"] else story["title"]
        lines.append(f"  {Colors.c(Colors.RED, '✗')} {Colors.c(Colors.BOLD, story_id)}: {title[:50]}")
        lines.append(f"    Blocked by: {Colors.c(Colors.YELLOW, dep_id)} ({dep_status})")
        lines.append("")

    return "\n".join(lines)


def render_recent_changelog(data: KanbanData, width: int) -> str:
    """Render last few changelog entries."""
    lines = []
    lines.append("")
    lines.append(Colors.c(Colors.BOLD, "  RECENT ACTIVITY"))
    lines.append("")

    changelog_path = data.kanban_dir / "changelog.md"
    if not changelog_path.is_file():
        lines.append(Colors.c(Colors.DIM, "  (No changelog)"))
        return "\n".join(lines)

    changelog_text = changelog_path.read_text(encoding="utf-8")
    entries = []
    current_date = ""
    for line in changelog_text.splitlines():
        if line.startswith("## "):
            current_date = line[3:].strip()
        elif line.strip().startswith("- ") and current_date:
            entry = line.strip()[2:].strip()
            entries.append((current_date, entry))

    # Show last 5 entries
    for date, entry in entries[:5]:
        lines.append(f"  {Colors.c(Colors.DIM, date)}  {entry}")

    if len(entries) > 5:
        lines.append(Colors.c(Colors.DIM, f"  ... and {len(entries) - 5} more"))

    return "\n".join(lines)


def render_footer(width: int) -> str:
    """Render footer."""
    lines = []
    lines.append("")
    lines.append(Colors.c(Colors.DIM, "─" * width))
    lines.append(Colors.c(Colors.DIM, "  StoryForge Dashboard • Run with: python scripts/dashboard.py"))
    return "\n".join(lines)


def render_dashboard(project_dir: Path):
    """Main dashboard rendering function."""
    width = min(get_terminal_width(), 100)
    project_name = project_dir.name

    data = KanbanData(project_dir)
    if not data.load():
        print(Colors.c(Colors.RED, f"No .kanban/ directory found in {project_dir}"))
        print("Run /kanban-bootstrap or bootstrap_project to set up StoryForge.")
        sys.exit(1)

    sections = [
        render_header(project_name, width),
        render_board_summary(data, width),
        render_features(data, width),
        render_active_stories(data, width),
        render_dependencies(data, width),
        render_sprint(data, width),
        render_velocity(data, width),
        render_recent_changelog(data, width),
        render_footer(width),
    ]
    # Filter empty sections
    sections = [s for s in sections if s]

    print("\n".join(sections))


# --- Entry Point ---

def main():
    # Ensure stdout can handle Unicode on Windows
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, TypeError):
            # Python < 3.7 or non-reconfigurable stream
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    if not _detect_color_support():
        Colors.disable()

    if len(sys.argv) > 1:
        project_dir = Path(sys.argv[1]).resolve()
    else:
        project_dir = Path.cwd()

    if not project_dir.is_dir():
        print(f"Error: {project_dir} is not a directory")
        sys.exit(1)

    render_dashboard(project_dir)


if __name__ == "__main__":
    main()

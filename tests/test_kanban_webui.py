"""
Tests for StoryForge Kanban Web UI parsing logic.

Covers board/stories sync detection, feature file parsing,
and missing file warnings (Issues #5 and #6).
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from kanban_webui import (
    find_board_story_refs,
    find_missing_story_files,
    parse_feature_file,
    find_board_feature_refs,
    find_missing_feature_files,
    parse_board,
    parse_story_file,
)


SAMPLE_PROJECT = REPO_ROOT / "examples" / "sample-project"


# --- Board/Stories Sync (Issue #5) ---

class TestFindBoardStoryRefs:
    """Test extracting STORY-NNN references from board.md."""

    def test_finds_refs_in_sample_project(self):
        refs = find_board_story_refs(SAMPLE_PROJECT / ".kanban")
        assert "STORY-001" in refs
        assert "STORY-002" in refs

    def test_returns_empty_for_missing_board(self, tmp_path):
        refs = find_board_story_refs(tmp_path)
        assert refs == set()

    def test_finds_refs_from_custom_board(self, tmp_path):
        kanban_dir = tmp_path / ".kanban"
        kanban_dir.mkdir()
        (kanban_dir / "board.md").write_text(
            "| STORY-010 | Some story |\n| STORY-020 | Another |\n"
        )
        refs = find_board_story_refs(kanban_dir)
        assert refs == {"STORY-010", "STORY-020"}


class TestFindMissingStoryFiles:
    """Test detection of stories referenced in board.md without files."""

    def test_sample_project_has_missing_story(self):
        # STORY-002 is referenced in board.md but has no file
        missing = find_missing_story_files(SAMPLE_PROJECT / ".kanban")
        assert "STORY-002" in missing

    def test_story_001_is_not_missing(self):
        missing = find_missing_story_files(SAMPLE_PROJECT / ".kanban")
        assert "STORY-001" not in missing

    def test_no_missing_when_all_files_exist(self, tmp_path):
        kanban_dir = tmp_path / ".kanban"
        kanban_dir.mkdir()
        stories_dir = kanban_dir / "stories"
        stories_dir.mkdir()
        (kanban_dir / "board.md").write_text("| STORY-001 | Test |\n")
        (stories_dir / "STORY-001.md").write_text("# STORY-001: Test\n")
        missing = find_missing_story_files(kanban_dir)
        assert missing == []

    def test_detects_missing_file(self, tmp_path):
        kanban_dir = tmp_path / ".kanban"
        kanban_dir.mkdir()
        stories_dir = kanban_dir / "stories"
        stories_dir.mkdir()
        (kanban_dir / "board.md").write_text(
            "| STORY-001 | Exists |\n| STORY-002 | Missing |\n"
        )
        (stories_dir / "STORY-001.md").write_text("# STORY-001: Exists\n")
        missing = find_missing_story_files(kanban_dir)
        assert missing == ["STORY-002"]


# --- Feature File Parsing (Issue #6) ---

class TestParseFeatureFile:
    """Test parsing FEAT-NNN.md files."""

    def test_parses_sample_feature(self):
        feat_file = SAMPLE_PROJECT / ".kanban" / "features" / "FEAT-001.md"
        feat = parse_feature_file(feat_file)
        assert feat["id"] == "FEAT-001"
        assert feat["title"] == "Core Application"
        assert "INIT-001" in feat["initiative"]
        assert feat["status"] == "In Progress"
        assert "STORY-001" in feat["story_refs"]
        assert "STORY-002" in feat["story_refs"]
        assert feat["goal"] != ""

    def test_parses_minimal_feature(self, tmp_path):
        feat_file = tmp_path / "FEAT-099.md"
        feat_file.write_text(
            "# FEAT-099: Minimal\n\n"
            "- **Status**: Backlog\n"
            "- **Initiative**: INIT-001\n"
        )
        feat = parse_feature_file(feat_file)
        assert feat["id"] == "FEAT-099"
        assert feat["title"] == "Minimal"
        assert feat["status"] == "Backlog"

    def test_parses_goal_section(self, tmp_path):
        feat_file = tmp_path / "FEAT-010.md"
        feat_file.write_text(
            "# FEAT-010: With Goal\n\n"
            "- **Status**: Ready\n\n"
            "## Goal\n\n"
            "Deliver feature X.\n\n"
            "## Stories\n\n"
            "- STORY-001: First\n"
        )
        feat = parse_feature_file(feat_file)
        assert feat["goal"] == "Deliver feature X."
        assert feat["story_refs"] == ["STORY-001"]


class TestFindBoardFeatureRefs:
    """Test extracting FEAT-NNN references from board.md."""

    def test_finds_refs_in_sample_project(self):
        refs = find_board_feature_refs(SAMPLE_PROJECT / ".kanban")
        assert "FEAT-001" in refs

    def test_returns_empty_for_missing_board(self, tmp_path):
        refs = find_board_feature_refs(tmp_path)
        assert refs == set()


class TestFindMissingFeatureFiles:
    """Test detection of features referenced in board.md without files."""

    def test_sample_project_no_missing_features(self):
        # FEAT-001 exists as a file now
        missing = find_missing_feature_files(SAMPLE_PROJECT / ".kanban")
        assert "FEAT-001" not in missing

    def test_detects_missing_feature_file(self, tmp_path):
        kanban_dir = tmp_path / ".kanban"
        kanban_dir.mkdir()
        features_dir = kanban_dir / "features"
        features_dir.mkdir()
        (kanban_dir / "board.md").write_text(
            "| FEAT-001 | Exists | INIT-001 | Done |\n"
            "| FEAT-002 | Missing | INIT-001 | Backlog |\n"
        )
        (features_dir / "FEAT-001.md").write_text("# FEAT-001: Exists\n")
        missing = find_missing_feature_files(kanban_dir)
        assert missing == ["FEAT-002"]


# --- Parse Board Integration ---

class TestParseBoardIntegration:
    """Test full board parsing with feature files and missing detection."""

    def test_sample_project_parses_fully(self):
        board = parse_board(SAMPLE_PROJECT / ".kanban")
        assert len(board["stories"]) >= 1
        assert len(board["features"]) >= 1
        assert len(board["feature_files"]) >= 1
        assert isinstance(board["missing_stories"], list)
        assert isinstance(board["missing_features"], list)

    def test_feature_files_merged_into_features(self):
        board = parse_board(SAMPLE_PROJECT / ".kanban")
        feat_ids = [f["id"] for f in board["features"]]
        assert "FEAT-001" in feat_ids

    def test_missing_stories_detected(self):
        board = parse_board(SAMPLE_PROJECT / ".kanban")
        # STORY-002 is in board.md but has no file
        assert "STORY-002" in board["missing_stories"]

    def test_board_with_no_kanban_dir(self, tmp_path):
        kanban_dir = tmp_path / ".kanban"
        kanban_dir.mkdir()
        board = parse_board(kanban_dir)
        assert board["stories"] == []
        assert board["features"] == []
        assert board["feature_files"] == []
        assert board["missing_stories"] == []

    def test_feature_file_adds_to_features_list(self, tmp_path):
        kanban_dir = tmp_path / ".kanban"
        kanban_dir.mkdir()
        features_dir = kanban_dir / "features"
        features_dir.mkdir()
        stories_dir = kanban_dir / "stories"
        stories_dir.mkdir()
        # Feature file exists but not in board.md features table
        (features_dir / "FEAT-010.md").write_text(
            "# FEAT-010: From File\n\n"
            "- **Status**: Backlog\n"
            "- **Initiative**: INIT-001\n"
        )
        (kanban_dir / "board.md").write_text("# Board\n")
        board = parse_board(kanban_dir)
        feat_ids = [f["id"] for f in board["features"]]
        assert "FEAT-010" in feat_ids


# --- Story File Parsing ---

class TestParseStoryFile:
    """Test story file parsing (existing functionality, regression tests)."""

    def test_parses_sample_story(self):
        story = parse_story_file(SAMPLE_PROJECT / ".kanban" / "stories" / "STORY-001.md")
        assert story["id"] == "STORY-001"
        assert story["title"] == "Create Initial Application Structure"
        assert story["status"] == "In Progress"
        assert "FEAT-001" in story["feature"]
        assert story["criteria_total"] == 4
        assert story["criteria_done"] == 0

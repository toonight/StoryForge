#!/usr/bin/env python3
"""
StoryForge Kanban Web UI

Serves an interactive Kanban board as a local web application.
Parses .kanban/ markdown files and renders a modern board view.

Usage:
    python scripts/kanban_webui.py [project_path] [--port PORT]

Requires: Python 3.8+ (stdlib only, no pip dependencies)
"""

import http.server
import json
import os
import re
import signal
import socket
import sys
import webbrowser
from pathlib import Path
from typing import Optional


# --- Configuration ---

DEFAULT_PORT = 8742
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent


# --- Markdown Parsing ---

def parse_story_file(path: Path) -> dict:
    """Parse a STORY-NNN.md file into a structured dict."""
    content = path.read_text(encoding="utf-8")
    story = {
        "id": path.stem,
        "file": path.name,
        "title": "",
        "feature": "",
        "initiative": "",
        "status": "Backlog",
        "created": "",
        "criteria": [],
        "criteria_done": 0,
        "criteria_total": 0,
        "context": "",
        "risks": [],
    }

    # Parse title from H1
    m = re.search(r"^#\s+(?:STORY-\d+:\s*)?(.+)", content, re.MULTILINE)
    if m:
        story["title"] = m.group(1).strip()

    # Parse metadata fields
    for key, field in [
        ("Feature", "feature"),
        ("Initiative", "initiative"),
        ("Status", "status"),
        ("Created", "created"),
    ]:
        m = re.search(rf"\*\*{key}\*\*:\s*(.+)", content)
        if m:
            story[field] = m.group(1).strip()

    # Parse acceptance criteria
    criteria = re.findall(r"- \[([ xX])\] (.+)", content)
    story["criteria_total"] = len(criteria)
    story["criteria_done"] = sum(1 for c in criteria if c[0].lower() == "x")
    story["criteria"] = [
        {"text": c[1], "done": c[0].lower() == "x"} for c in criteria
    ]

    return story


def find_board_story_refs(kanban_dir: Path) -> set:
    """Find all STORY-NNN references in board.md."""
    board_file = kanban_dir / "board.md"
    if not board_file.is_file():
        return set()
    content = board_file.read_text(encoding="utf-8")
    return set(re.findall(r"STORY-\d+", content))


def find_missing_story_files(kanban_dir: Path) -> list:
    """Return STORY-NNN IDs referenced in board.md but missing files."""
    refs = find_board_story_refs(kanban_dir)
    stories_dir = kanban_dir / "stories"
    missing = []
    for ref in sorted(refs):
        story_file = stories_dir / f"{ref}.md"
        if not story_file.is_file():
            missing.append(ref)
    return missing


def parse_feature_file(path: Path) -> dict:
    """Parse a FEAT-NNN.md file into a structured dict."""
    content = path.read_text(encoding="utf-8")
    feature = {
        "id": path.stem,
        "file": path.name,
        "title": "",
        "initiative": "",
        "status": "Backlog",
        "created": "",
        "goal": "",
        "story_refs": [],
    }

    # Parse title from H1
    m = re.search(r"^#\s+(?:FEAT-\d+:\s*)?(.+)", content, re.MULTILINE)
    if m:
        feature["title"] = m.group(1).strip()

    # Parse metadata fields
    for key, field in [
        ("Initiative", "initiative"),
        ("Status", "status"),
        ("Created", "created"),
    ]:
        m = re.search(rf"\*\*{key}\*\*:\s*(.+)", content)
        if m:
            feature[field] = m.group(1).strip()

    # Parse goal section
    goal_match = re.search(
        r"## Goal\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if goal_match:
        feature["goal"] = goal_match.group(1).strip()

    # Parse story references from Stories section
    stories_match = re.search(
        r"## Stories\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
    )
    if stories_match:
        feature["story_refs"] = re.findall(
            r"(STORY-\d+)", stories_match.group(1)
        )

    return feature


def find_board_feature_refs(kanban_dir: Path) -> set:
    """Find all FEAT-NNN references in board.md."""
    board_file = kanban_dir / "board.md"
    if not board_file.is_file():
        return set()
    content = board_file.read_text(encoding="utf-8")
    return set(re.findall(r"FEAT-\d+", content))


def find_missing_feature_files(kanban_dir: Path) -> list:
    """Return FEAT-NNN IDs referenced in board.md but missing files."""
    refs = find_board_feature_refs(kanban_dir)
    features_dir = kanban_dir / "features"
    missing = []
    for ref in sorted(refs):
        feat_file = features_dir / f"{ref}.md"
        if not feat_file.is_file():
            missing.append(ref)
    return missing


def parse_board(kanban_dir: Path) -> dict:
    """Parse the full Kanban board from .kanban/ directory."""
    board = {
        "stories": [],
        "features": [],
        "feature_files": [],
        "initiatives": [],
        "sprint": None,
        "backlog_items": [],
        "missing_stories": [],
        "missing_features": [],
    }

    # Parse stories
    stories_dir = kanban_dir / "stories"
    if stories_dir.is_dir():
        for f in sorted(stories_dir.glob("STORY-[0-9]*.md")):
            board["stories"].append(parse_story_file(f))

    # Parse board.md for features and initiatives
    board_file = kanban_dir / "board.md"
    if board_file.is_file():
        content = board_file.read_text(encoding="utf-8")

        # Split content by sections to avoid cross-matching
        feat_section = re.search(
            r"## Features\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
        )
        init_section = re.search(
            r"## Initiatives\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
        )

        if feat_section:
            for m in re.finditer(
                r"\|\s*(FEAT-\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
                feat_section.group(1),
            ):
                board["features"].append({
                    "id": m.group(1),
                    "title": m.group(2).strip(),
                    "initiative": m.group(3).strip(),
                    "status": m.group(4).strip(),
                })

        if init_section:
            for m in re.finditer(
                r"\|\s*(INIT-\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|",
                init_section.group(1),
            ):
                board["initiatives"].append({
                    "id": m.group(1),
                    "title": m.group(2).strip(),
                    "status": m.group(3).strip(),
                })

    # Parse sprint.md
    sprint_file = kanban_dir / "sprint.md"
    if sprint_file.is_file():
        content = sprint_file.read_text(encoding="utf-8")
        if "No active sprint" not in content:
            m = re.search(r"### (Sprint \d+.*?)$", content, re.MULTILINE)
            if m:
                board["sprint"] = m.group(1)

    # Parse feature files
    features_dir = kanban_dir / "features"
    if features_dir.is_dir():
        for f in sorted(features_dir.glob("FEAT-[0-9]*.md")):
            board["feature_files"].append(parse_feature_file(f))

    # Merge feature files with board.md features
    file_ids = {f["id"] for f in board["feature_files"]}
    for ff in board["feature_files"]:
        # If feature from file not already in board features, add it
        if not any(bf["id"] == ff["id"] for bf in board["features"]):
            board["features"].append({
                "id": ff["id"],
                "title": ff["title"],
                "initiative": ff["initiative"],
                "status": ff["status"],
            })

    # Detect missing story and feature files
    board["missing_stories"] = find_missing_story_files(kanban_dir)
    board["missing_features"] = find_missing_feature_files(kanban_dir)

    # Parse backlog.md future items
    backlog_file = kanban_dir / "backlog.md"
    if backlog_file.is_file():
        content = backlog_file.read_text(encoding="utf-8")
        in_future = False
        current_item = None
        for line in content.splitlines():
            if "Future Work" in line:
                in_future = True
                continue
            if in_future:
                if line.startswith("### "):
                    current_item = line[4:].strip()
                    board["backlog_items"].append({
                        "title": current_item,
                        "details": [],
                    })
                elif line.startswith("- ") and board["backlog_items"]:
                    board["backlog_items"][-1]["details"].append(
                        line[2:].strip()
                    )
                elif line.startswith("---"):
                    break

    return board


# --- HTML Template ---

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StoryForge Kanban Board</title>
<style>
  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --surface2: #1c2129;
    --border: #30363d;
    --text: #e6edf3;
    --text-dim: #8b949e;
    --accent: #58a6ff;
    --green: #3fb950;
    --yellow: #d29922;
    --orange: #db6d28;
    --purple: #bc8cff;
    --red: #f85149;
    --pink: #f778ba;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
  }

  header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  header h1 {
    font-size: 20px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  header h1 .logo {
    width: 28px;
    height: 28px;
    background: linear-gradient(135deg, var(--accent), var(--purple));
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
  }

  .stats {
    display: flex;
    gap: 20px;
    font-size: 13px;
    color: var(--text-dim);
  }

  .stats .stat-value {
    color: var(--text);
    font-weight: 600;
  }

  .tabs {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0 24px;
    display: flex;
    gap: 0;
  }

  .tab {
    padding: 10px 16px;
    font-size: 13px;
    color: var(--text-dim);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
  }

  .tab:hover { color: var(--text); }
  .tab.active {
    color: var(--text);
    border-bottom-color: var(--accent);
  }

  .board {
    display: none;
    gap: 16px;
    padding: 20px 24px;
    overflow-x: auto;
    min-height: calc(100vh - 110px);
    align-items: flex-start;
  }

  .column {
    min-width: 280px;
    max-width: 320px;
    flex: 1;
    background: var(--surface);
    border-radius: 10px;
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
  }

  .column-header {
    padding: 14px 16px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .column-title {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .column-title .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }

  .col-backlog .dot { background: var(--text-dim); }
  .col-ready .dot { background: var(--yellow); }
  .col-inprogress .dot { background: var(--accent); }
  .col-review .dot { background: var(--orange); }
  .col-done .dot { background: var(--green); }

  .column-count {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1px 8px;
    font-size: 12px;
    color: var(--text-dim);
  }

  .column-cards {
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    overflow-y: auto;
    max-height: calc(100vh - 200px);
  }

  .card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    cursor: pointer;
    transition: all 0.15s;
  }

  .card:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
  }

  .card-id {
    font-size: 11px;
    color: var(--accent);
    font-weight: 600;
    margin-bottom: 6px;
  }

  .card-title {
    font-size: 13px;
    font-weight: 500;
    line-height: 1.4;
    margin-bottom: 10px;
  }

  .card-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-dim);
  }

  .card-feature {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 10px;
  }

  .progress-bar {
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    margin-top: 10px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: var(--green);
    border-radius: 2px;
    transition: width 0.3s;
  }

  /* Features view */
  .features-view, .backlog-view {
    padding: 24px;
    display: none;
  }

  .features-view.active, .backlog-view.active, .board.active {
    display: flex;
  }

  .features-view.active, .backlog-view.active {
    display: block;
  }

  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 12px;
    margin-top: 16px;
  }

  .feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px;
  }

  .feature-card h3 {
    font-size: 14px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .feature-card .feat-id {
    color: var(--purple);
    font-size: 11px;
    font-weight: 600;
  }

  .feature-card .feat-status {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 500;
  }

  .feat-status.done { background: rgba(63,185,80,0.15); color: var(--green); }
  .feat-status.inprogress { background: rgba(88,166,255,0.15); color: var(--accent); }

  .feature-stories {
    margin-top: 10px;
    font-size: 12px;
    color: var(--text-dim);
  }

  /* Backlog */
  .backlog-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 12px;
  }

  .backlog-section h3 {
    font-size: 14px;
    margin-bottom: 10px;
    color: var(--yellow);
  }

  .backlog-section li {
    font-size: 13px;
    color: var(--text-dim);
    margin-left: 16px;
    margin-bottom: 4px;
  }

  /* Modal */
  .modal-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.6);
    z-index: 100;
    justify-content: center;
    align-items: center;
  }

  .modal-overlay.open {
    display: flex;
  }

  .modal {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    width: 560px;
    max-height: 80vh;
    overflow-y: auto;
    padding: 24px;
  }

  .modal h2 {
    font-size: 16px;
    margin-bottom: 4px;
  }

  .modal .modal-id {
    color: var(--accent);
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 16px;
  }

  .modal .modal-field {
    margin-bottom: 12px;
  }

  .modal .modal-label {
    font-size: 11px;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
  }

  .modal .modal-value {
    font-size: 13px;
  }

  .modal .criteria-list {
    list-style: none;
    font-size: 13px;
  }

  .modal .criteria-list li {
    padding: 4px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .modal .criteria-list .check {
    color: var(--green);
  }

  .modal .criteria-list .uncheck {
    color: var(--text-dim);
  }

  .close-btn {
    float: right;
    background: none;
    border: none;
    color: var(--text-dim);
    font-size: 20px;
    cursor: pointer;
  }

  .close-btn:hover { color: var(--text); }

  .empty-col {
    text-align: center;
    color: var(--text-dim);
    font-size: 12px;
    padding: 20px 10px;
    font-style: italic;
  }

  /* Warning banner */
  .warning-banner {
    background: rgba(210,153,34,0.12);
    border: 1px solid var(--yellow);
    border-radius: 8px;
    margin: 12px 24px 0;
    padding: 12px 16px;
    font-size: 13px;
    color: var(--yellow);
    display: none;
  }

  .warning-banner.visible { display: block; }

  .warning-banner strong { color: var(--text); }

  .warning-banner .missing-ids {
    margin-top: 4px;
    font-family: monospace;
    font-size: 12px;
    color: var(--text-dim);
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: var(--text-dim); }
</style>
</head>
<body>

<header>
  <h1>
    <span class="logo">S</span>
    StoryForge Kanban
  </h1>
  <div class="stats">
    <span>Stories <span class="stat-value" id="total-stories">0</span></span>
    <span>Done <span class="stat-value" id="total-done">0</span></span>
    <span>Features <span class="stat-value" id="total-features">0</span></span>
    <span>Sprint <span class="stat-value" id="current-sprint">None</span></span>
  </div>
</header>

<div class="tabs">
  <div class="tab active" data-view="board">Board</div>
  <div class="tab" data-view="features">Features</div>
  <div class="tab" data-view="backlog">Backlog</div>
</div>

<div class="warning-banner" id="warning-banner"></div>

<div class="board active" id="board-view">
  <div class="column col-backlog">
    <div class="column-header">
      <span class="column-title"><span class="dot"></span> Backlog</span>
      <span class="column-count" id="count-backlog">0</span>
    </div>
    <div class="column-cards" id="cards-backlog"></div>
  </div>
  <div class="column col-ready">
    <div class="column-header">
      <span class="column-title"><span class="dot"></span> Ready</span>
      <span class="column-count" id="count-ready">0</span>
    </div>
    <div class="column-cards" id="cards-ready"></div>
  </div>
  <div class="column col-inprogress">
    <div class="column-header">
      <span class="column-title"><span class="dot"></span> In Progress</span>
      <span class="column-count" id="count-inprogress">0</span>
    </div>
    <div class="column-cards" id="cards-inprogress"></div>
  </div>
  <div class="column col-review">
    <div class="column-header">
      <span class="column-title"><span class="dot"></span> Review</span>
      <span class="column-count" id="count-review">0</span>
    </div>
    <div class="column-cards" id="cards-review"></div>
  </div>
  <div class="column col-done">
    <div class="column-header">
      <span class="column-title"><span class="dot"></span> Done</span>
      <span class="column-count" id="count-done">0</span>
    </div>
    <div class="column-cards" id="cards-done"></div>
  </div>
</div>

<div class="features-view" id="features-view"></div>
<div class="backlog-view" id="backlog-view"></div>

<div class="modal-overlay" id="modal-overlay">
  <div class="modal" id="modal"></div>
</div>

<script>
const DATA = __BOARD_DATA__;

// Escape HTML special characters to prevent XSS from markdown content
function esc(s) {
  const el = document.createElement('span');
  el.textContent = s;
  return el.innerHTML;
}

// --- Render Board ---
function statusToColumn(status) {
  const s = status.toLowerCase().replace(/\s+/g, '');
  const map = {
    'backlog': 'backlog',
    'ready': 'ready',
    'inprogress': 'inprogress',
    'review': 'review',
    'done': 'done',
  };
  return map[s] || 'backlog';
}

function renderCards() {
  const cols = { backlog: [], ready: [], inprogress: [], review: [], done: [] };

  DATA.stories.forEach(story => {
    const col = statusToColumn(story.status);
    cols[col].push(story);
  });

  Object.keys(cols).forEach(col => {
    const container = document.getElementById('cards-' + col);
    const count = document.getElementById('count-' + col);
    count.textContent = cols[col].length;

    if (cols[col].length === 0) {
      container.innerHTML = '<div class="empty-col">No stories</div>';
      return;
    }

    container.innerHTML = cols[col].map(story => {
      const pct = story.criteria_total > 0
        ? Math.round((story.criteria_done / story.criteria_total) * 100)
        : 0;
      const feat = story.feature.replace(/^(FEAT-\d+)\s*-?\s*/, '$1 ');
      return `
        <div class="card" onclick="openModal('${esc(story.id)}')">
          <div class="card-id">${esc(story.id)}</div>
          <div class="card-title">${esc(story.title)}</div>
          <div class="card-meta">
            <span class="card-feature">${esc(feat.split(' ')[0])}</span>
            <span>${story.criteria_done}/${story.criteria_total}</span>
          </div>
          ${story.criteria_total > 0 ? `
          <div class="progress-bar">
            <div class="progress-fill" style="width:${pct}%"></div>
          </div>` : ''}
        </div>`;
    }).join('');
  });

  // Stats
  document.getElementById('total-stories').textContent = DATA.stories.length;
  document.getElementById('total-done').textContent =
    DATA.stories.filter(s => s.status.toLowerCase() === 'done').length;
  document.getElementById('total-features').textContent = DATA.features.length;
  document.getElementById('current-sprint').textContent =
    DATA.sprint || 'None';
}

// --- Render Features ---
function renderFeatures() {
  const view = document.getElementById('features-view');

  // Build a lookup of feature files by ID
  const fileById = {};
  if (DATA.feature_files) {
    DATA.feature_files.forEach(ff => { fileById[ff.id] = ff; });
  }

  // Group features by initiative
  const byInit = {};
  DATA.initiatives.forEach(i => { byInit[i.id] = { ...i, features: [] }; });
  // Add an "unassigned" group for features not matching any initiative
  const unassigned = { id: '', title: 'Unassigned', status: '', features: [] };

  DATA.features.forEach(f => {
    const iid = f.initiative;
    if (byInit[iid]) {
      byInit[iid].features.push(f);
    } else {
      unassigned.features.push(f);
    }
  });

  let html = '';
  const groups = [...Object.values(byInit)];
  if (unassigned.features.length > 0) groups.push(unassigned);

  groups.forEach(init => {
    if (init.features.length === 0 && init.id) return;
    if (init.id) {
      html += `<h2 style="margin-bottom:4px;font-size:15px;">${esc(init.id)}: ${esc(init.title)}
        <span style="font-size:12px;color:var(--text-dim);font-weight:400;"> &mdash; ${esc(init.status)}</span></h2>`;
    }
    html += '<div class="feature-grid">';
    init.features.forEach(f => {
      const statusCls = f.status.toLowerCase().replace(/\s+/g, '');
      const stories = DATA.stories.filter(s => s.feature.includes(f.id));
      const doneStories = stories.filter(s => s.status.toLowerCase() === 'done').length;
      const ff = fileById[f.id];
      const goal = ff && ff.goal ? ff.goal : '';
      html += `
        <div class="feature-card">
          <h3>
            <span class="feat-id">${esc(f.id)}</span>
            ${esc(f.title)}
            <span class="feat-status ${statusCls}">${esc(f.status)}</span>
          </h3>
          ${goal ? `<div style="font-size:12px;color:var(--text-dim);margin:6px 0;">${esc(goal)}</div>` : ''}
          <div class="feature-stories">
            <div style="font-size:11px;color:var(--text-dim);margin-bottom:4px;">
              Stories: ${doneStories}/${stories.length} done
            </div>
            ${stories.length > 0
              ? stories.map(s => {
                  const sIcon = s.status.toLowerCase() === 'done' ? '&#10003;' : '&#9675;';
                  const sColor = s.status.toLowerCase() === 'done' ? 'var(--green)' : 'var(--text-dim)';
                  return `<div><span style="color:${sColor}">${sIcon}</span> ${esc(s.id)}: ${esc(s.title)}</div>`;
                }).join('')
              : '<div style="font-style:italic">No tracked stories</div>'}
          </div>
          ${stories.length > 0 ? `
          <div class="progress-bar" style="margin-top:8px">
            <div class="progress-fill" style="width:${stories.length > 0 ? Math.round((doneStories / stories.length) * 100) : 0}%"></div>
          </div>` : ''}
        </div>`;
    });
    html += '</div>';
  });
  view.innerHTML = html;
}

// --- Render Backlog ---
function renderBacklog() {
  const view = document.getElementById('backlog-view');
  if (DATA.backlog_items.length === 0) {
    view.innerHTML = '<div class="empty-col" style="padding:40px">No backlog items</div>';
    return;
  }
  view.innerHTML = DATA.backlog_items.map(item => `
    <div class="backlog-section">
      <h3>${esc(item.title)}</h3>
      <ul>${item.details.map(d => `<li>${esc(d)}</li>`).join('')}</ul>
    </div>
  `).join('');
}

// --- Warning Banner ---
function renderWarnings() {
  const banner = document.getElementById('warning-banner');
  const msgs = [];

  if (DATA.missing_stories && DATA.missing_stories.length > 0) {
    msgs.push(
      '<strong>Missing story files:</strong> ' +
      DATA.missing_stories.map(id => esc(id) + '.md').join(', ') +
      ' referenced in board.md but no file in stories/'
    );
  }

  if (DATA.missing_features && DATA.missing_features.length > 0) {
    msgs.push(
      '<strong>Missing feature files:</strong> ' +
      DATA.missing_features.map(id => esc(id) + '.md').join(', ') +
      ' referenced in board.md but no file in features/'
    );
  }

  if (msgs.length > 0) {
    banner.innerHTML = msgs.join('<br>');
    banner.classList.add('visible');
  } else {
    banner.classList.remove('visible');
  }
}

// --- Modal ---
function openModal(storyId) {
  const story = DATA.stories.find(s => s.id === storyId);
  if (!story) return;

  const modal = document.getElementById('modal');
  modal.innerHTML = `
    <button class="close-btn" onclick="closeModal()">&times;</button>
    <div class="modal-id">${esc(story.id)}</div>
    <h2>${esc(story.title)}</h2>
    <br>
    <div class="modal-field">
      <div class="modal-label">Status</div>
      <div class="modal-value">${esc(story.status)}</div>
    </div>
    <div class="modal-field">
      <div class="modal-label">Feature</div>
      <div class="modal-value">${esc(story.feature)}</div>
    </div>
    <div class="modal-field">
      <div class="modal-label">Initiative</div>
      <div class="modal-value">${esc(story.initiative)}</div>
    </div>
    <div class="modal-field">
      <div class="modal-label">Created</div>
      <div class="modal-value">${esc(story.created)}</div>
    </div>
    ${story.criteria.length > 0 ? `
    <div class="modal-field">
      <div class="modal-label">Acceptance Criteria (${story.criteria_done}/${story.criteria_total})</div>
      <ul class="criteria-list">
        ${story.criteria.map(c => `
          <li>
            <span class="${c.done ? 'check' : 'uncheck'}">${c.done ? '&#10003;' : '&#9675;'}</span>
            ${esc(c.text)}
          </li>
        `).join('')}
      </ul>
    </div>` : ''}
  `;
  document.getElementById('modal-overlay').classList.add('open');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('open');
}

document.getElementById('modal-overlay').addEventListener('click', e => {
  if (e.target.id === 'modal-overlay') closeModal();
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// --- Tabs ---
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const view = tab.dataset.view;
    document.getElementById('board-view').classList.toggle('active', view === 'board');
    document.getElementById('features-view').classList.toggle('active', view === 'features');
    document.getElementById('backlog-view').classList.toggle('active', view === 'backlog');
  });
});

// --- Live Reload ---
let _liveData = DATA;

async function pollForUpdates() {
  try {
    const resp = await fetch('/api/board');
    if (!resp.ok) return;
    const newData = await resp.json();
    const newJson = JSON.stringify(newData);
    const oldJson = JSON.stringify(_liveData);
    if (newJson !== oldJson) {
      _liveData = newData;
      // Update global DATA reference used by renderers
      Object.keys(newData).forEach(k => { DATA[k] = newData[k]; });
      renderCards();
      renderFeatures();
      renderBacklog();
      renderWarnings();
    }
  } catch (e) { /* ignore network errors */ }
}

setInterval(pollForUpdates, 3000);

// --- Init ---
renderCards();
renderFeatures();
renderBacklog();
renderWarnings();
</script>
</body>
</html>"""


# --- Server ---

class KanbanHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler that serves the Kanban board with live reload."""

    kanban_dir: Optional[Path] = None

    def _get_board_data(self) -> dict:
        """Re-parse .kanban/ on every request for live updates."""
        if self.kanban_dir and self.kanban_dir.is_dir():
            return parse_board(self.kanban_dir)
        return {}

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            board_data = self._get_board_data()
            html = HTML_TEMPLATE.replace(
                "__BOARD_DATA__", json.dumps(board_data)
            )
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/api/board":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            board_data = self._get_board_data()
            self.wfile.write(
                json.dumps(board_data, indent=2).encode("utf-8")
            )
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def _is_port_in_use(port: int) -> bool:
    """Check if a TCP port is already in use on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return False
        except OSError:
            return True


def _kill_process_on_port(port: int) -> None:
    """Kill the process occupying a given port. Works on Windows and Unix."""
    import subprocess

    try:
        if sys.platform == "win32":
            # netstat to find PID, then taskkill
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.splitlines():
                if f"127.0.0.1:{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    pid = parts[-1]
                    if pid.isdigit() and int(pid) != os.getpid():
                        subprocess.run(
                            ["taskkill", "/F", "/PID", pid],
                            capture_output=True, timeout=5,
                        )
                        print(f"  Killed previous process (PID {pid}).")
                        return
        else:
            # lsof to find PID, then kill
            result = subprocess.run(
                ["lsof", "-ti", f"tcp:{port}", "-s", "tcp:listen"],
                capture_output=True, text=True, timeout=5,
            )
            for pid_str in result.stdout.strip().splitlines():
                pid = int(pid_str)
                if pid != os.getpid():
                    os.kill(pid, signal.SIGTERM)
                    print(f"  Killed previous process (PID {pid}).")
                    return
    except (subprocess.SubprocessError, ValueError, OSError):
        pass  # Fall through to the bind attempt which will give a clear error


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except (AttributeError, TypeError):
            pass

    args = sys.argv[1:]
    port = DEFAULT_PORT
    project_path = None

    i = 0
    while i < len(args):
        if args[i] == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 2
        elif not args[i].startswith("--"):
            project_path = Path(args[i])
            i += 1
        else:
            i += 1

    if project_path is None:
        project_path = Path.cwd()

    kanban_dir = project_path / ".kanban"
    if not kanban_dir.is_dir():
        print(f"Error: No .kanban/ directory found in {project_path}")
        print("Run this from a StoryForge-managed project root.")
        sys.exit(1)

    print(f"Parsing .kanban/ in {project_path}...")
    board_data = parse_board(kanban_dir)

    stories_count = len(board_data["stories"])
    features_count = len(board_data["features"])
    done_count = sum(
        1 for s in board_data["stories"] if s["status"].lower() == "done"
    )
    print(f"  {stories_count} stories, {features_count} features, {done_count} done")

    KanbanHandler.kanban_dir = kanban_dir

    url = f"http://127.0.0.1:{port}"

    # Check if port is already in use and kill the previous instance
    if _is_port_in_use(port):
        print(f"  Port {port} is already in use. Stopping previous instance...")
        _kill_process_on_port(port)

    try:
        server = http.server.HTTPServer(("127.0.0.1", port), KanbanHandler)
    except OSError as e:
        print(f"Error: Could not bind to port {port}: {e}")
        print("Try --port <other_port> or stop the existing process manually.")
        sys.exit(1)

    print(f"\nKanban board available at: {url}")
    print("Press Ctrl+C to stop.\n")

    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()

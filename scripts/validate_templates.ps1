#Requires -Version 5.1
<#
.SYNOPSIS
    Validate that StoryForge templates are complete and well-formed.

.EXAMPLE
    .\scripts\validate_templates.ps1
#>

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StoryForgeRoot = Split-Path -Parent $ScriptDir
$Errors = 0
$Warnings = 0

Write-Host "=== StoryForge Template Validation ===" -ForegroundColor Cyan
Write-Host ""

function Test-FileExists {
    param([string]$Path, [string]$Description)
    $FullPath = Join-Path $StoryForgeRoot $Path
    if (Test-Path $FullPath) {
        Write-Host "  OK: $Path" -ForegroundColor Green
    } else {
        Write-Host "  MISSING: $Path ($Description)" -ForegroundColor Red
        $script:Errors++
    }
}

function Test-DirExists {
    param([string]$Path, [string]$Description)
    $FullPath = Join-Path $StoryForgeRoot $Path
    if (Test-Path $FullPath -PathType Container) {
        Write-Host "  OK: $Path/" -ForegroundColor Green
    } else {
        Write-Host "  MISSING: $Path/ ($Description)" -ForegroundColor Red
        $script:Errors++
    }
}

# Repo root
Write-Host "Checking repository root..."
Test-FileExists "README.md" "Repository readme"
Test-FileExists "LICENSE" "License file"
Test-FileExists ".gitignore" "Git ignore rules"
Test-FileExists "CHANGELOG.md" "Change log"
Test-FileExists "ROADMAP.md" "Roadmap"

# Docs
Write-Host ""
Write-Host "Checking documentation..."
Test-FileExists "docs\architecture.md" "Architecture"
Test-FileExists "docs\operating-model.md" "Operating model"
Test-FileExists "docs\source-of-truth-policy.md" "Source of truth"
Test-FileExists "docs\anthropic-source-map.md" "Source map"
Test-FileExists "docs\upstream\doc-index.md" "Doc index"

# Home templates
Write-Host ""
Write-Host "Checking user-level templates..."
Test-FileExists "templates\home\.claude\CLAUDE.md" "Global CLAUDE.md"
Test-FileExists "templates\home\.claude\settings.json" "Global settings"
Test-DirExists "templates\home\.claude\agents" "Agent definitions"

$Agents = @("portfolio-orchestrator", "planner", "implementer", "reviewer", "doc-maintainer", "upstream-watch")
foreach ($Agent in $Agents) {
    Test-FileExists "templates\home\.claude\agents\$Agent.md" "$Agent agent"
}

$Skills = @("kanban-bootstrap", "story-write", "sprint-groom", "release-adapt", "doc-update")
foreach ($Skill in $Skills) {
    Test-FileExists "templates\home\.claude\skills\$Skill\SKILL.md" "$Skill skill"
}

# Agent frontmatter
Write-Host ""
Write-Host "Checking agent frontmatter..."
foreach ($Agent in $Agents) {
    $AgentPath = Join-Path $StoryForgeRoot "templates\home\.claude\agents\$Agent.md"
    if (Test-Path $AgentPath) {
        $Content = Get-Content $AgentPath -Raw
        if ($Content.StartsWith("---")) {
            Write-Host "  OK: $Agent has frontmatter" -ForegroundColor Green
        } else {
            Write-Host "  ERROR: $Agent missing frontmatter" -ForegroundColor Red
            $Errors++
        }
        if ($Content -match "name:\s*$Agent") {
            Write-Host "  OK: $Agent has name field" -ForegroundColor Green
        } else {
            Write-Host "  ERROR: $Agent missing name field" -ForegroundColor Red
            $Errors++
        }
    }
}

# Project templates
Write-Host ""
Write-Host "Checking project-level templates..."
Test-FileExists "templates\project\.claude\CLAUDE.md" "Project CLAUDE.md"
Test-FileExists "templates\project\.claude\settings.json" "Project settings"
Test-FileExists "templates\project\.kanban\board.md" "Board"
Test-FileExists "templates\project\.kanban\backlog.md" "Backlog"
Test-FileExists "templates\project\.kanban\sprint.md" "Sprint"
Test-FileExists "templates\project\.kanban\decisions.md" "Decisions"
Test-FileExists "templates\project\.kanban\changelog.md" "Changelog"
Test-FileExists "templates\project\.kanban\stories\STORY-TEMPLATE.md" "Story template"

# JSON validation
Write-Host ""
Write-Host "Checking JSON validity..."
$JsonFiles = @("templates\home\.claude\settings.json", "templates\project\.claude\settings.json")
foreach ($JsonFile in $JsonFiles) {
    $FullPath = Join-Path $StoryForgeRoot $JsonFile
    if (Test-Path $FullPath) {
        try {
            Get-Content $FullPath -Raw | ConvertFrom-Json | Out-Null
            Write-Host "  OK: $JsonFile is valid JSON" -ForegroundColor Green
        } catch {
            Write-Host "  ERROR: $JsonFile is invalid JSON" -ForegroundColor Red
            $Errors++
        }
    }
}

# Scripts
Write-Host ""
Write-Host "Checking scripts..."
Test-FileExists "scripts\install_storyforge.sh" "Install (bash)"
Test-FileExists "scripts\bootstrap_project.sh" "Bootstrap (bash)"
Test-FileExists "scripts\validate_templates.sh" "Validate (bash)"
Test-FileExists "scripts\sync_upstream_docs.sh" "Sync upstream (bash)"
Test-FileExists "scripts\install_storyforge.ps1" "Install (PowerShell)"
Test-FileExists "scripts\bootstrap_project.ps1" "Bootstrap (PowerShell)"
Test-FileExists "scripts\validate_templates.ps1" "Validate (PowerShell)"
Test-FileExists "scripts\sync_upstream_docs.ps1" "Sync upstream (PowerShell)"
Test-FileExists "scripts\dashboard.py" "Dashboard"

# Summary
Write-Host ""
Write-Host "=== Validation Summary ===" -ForegroundColor Cyan
Write-Host "  Errors:   $Errors"
Write-Host "  Warnings: $Warnings"
Write-Host ""

if ($Errors -gt 0) {
    Write-Host "FAILED: $Errors error(s) found." -ForegroundColor Red
    exit 1
} else {
    Write-Host "PASSED: All checks passed." -ForegroundColor Green
    exit 0
}

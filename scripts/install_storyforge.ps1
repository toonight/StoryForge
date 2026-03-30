#Requires -Version 5.1
<#
.SYNOPSIS
    Install StoryForge user-level configuration to ~/.claude/

.DESCRIPTION
    Copies StoryForge templates to the user's home Claude config directory.
    Backs up existing files before overwriting.

.PARAMETER Force
    Replace existing files instead of appending/skipping.

.EXAMPLE
    .\scripts\install_storyforge.ps1
    .\scripts\install_storyforge.ps1 -Force
#>

[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StoryForgeRoot = Split-Path -Parent $ScriptDir
$TemplateDir = Join-Path $StoryForgeRoot "templates\home\.claude"
$TargetDir = Join-Path $env:USERPROFILE ".claude"
$BackupDir = Join-Path $TargetDir ("backups\storyforge-" + (Get-Date -Format "yyyyMMdd-HHmmss"))

Write-Host "=== StoryForge Installer ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Source:  $TemplateDir"
Write-Host "Target:  $TargetDir"
Write-Host ""

if (-not (Test-Path $TemplateDir)) {
    Write-Error "Template directory not found: $TemplateDir"
    exit 1
}

if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

function Install-FileWithBackup {
    param(
        [string]$Source,
        [string]$RelativePath
    )
    $Dest = Join-Path $TargetDir $RelativePath
    $DestDir = Split-Path -Parent $Dest

    if (-not (Test-Path $DestDir)) {
        New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
    }

    if (Test-Path $Dest) {
        if (-not $Force) {
            Write-Host "  EXISTS: $RelativePath" -ForegroundColor Yellow
            $BackupPath = Join-Path $BackupDir $RelativePath
            $BackupPathDir = Split-Path -Parent $BackupPath
            if (-not (Test-Path $BackupPathDir)) {
                New-Item -ItemType Directory -Path $BackupPathDir -Force | Out-Null
            }
            Copy-Item $Dest $BackupPath
            Write-Host "    Backed up to: $BackupPath"
        }
    }

    Copy-Item $Source $Dest -Force
    Write-Host "  INSTALLED: $RelativePath" -ForegroundColor Green
}

# Install CLAUDE.md
Write-Host "Installing CLAUDE.md..."
$ClaudeMdSource = Join-Path $TemplateDir "CLAUDE.md"
$ClaudeMdDest = Join-Path $TargetDir "CLAUDE.md"

if ((Test-Path $ClaudeMdDest) -and (Get-Item $ClaudeMdDest).Length -gt 0 -and (-not $Force)) {
    Write-Host "  WARNING: Existing CLAUDE.md has content." -ForegroundColor Yellow
    Write-Host "  Appending StoryForge content. Use -Force to replace."
    if (-not (Test-Path $BackupDir)) {
        New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    }
    Copy-Item $ClaudeMdDest (Join-Path $BackupDir "CLAUDE.md")
    Add-Content -Path $ClaudeMdDest -Value "`n`n"
    Get-Content $ClaudeMdSource | Add-Content -Path $ClaudeMdDest
    Write-Host "  APPENDED: CLAUDE.md" -ForegroundColor Green
} else {
    Install-FileWithBackup -Source $ClaudeMdSource -RelativePath "CLAUDE.md"
}

# Install settings.json
Write-Host ""
Write-Host "Installing settings.json..."
$SettingsSource = Join-Path $TemplateDir "settings.json"
$SettingsDest = Join-Path $TargetDir "settings.json"

if (Test-Path $SettingsDest) {
    Write-Host "  WARNING: Existing settings.json found." -ForegroundColor Yellow
    Write-Host "  Saved as settings.storyforge.json (merge manually)."
    Copy-Item $SettingsSource (Join-Path $TargetDir "settings.storyforge.json")
} else {
    Install-FileWithBackup -Source $SettingsSource -RelativePath "settings.json"
}

# Install agents
Write-Host ""
Write-Host "Installing agents..."
$AgentFiles = Get-ChildItem (Join-Path $TemplateDir "agents") -Filter "*.md" -ErrorAction SilentlyContinue
foreach ($AgentFile in $AgentFiles) {
    $RelPath = "agents\$($AgentFile.Name)"
    Install-FileWithBackup -Source $AgentFile.FullName -RelativePath $RelPath
}

# Install skills
Write-Host ""
Write-Host "Installing skills..."
$SkillDirs = Get-ChildItem (Join-Path $TemplateDir "skills") -Directory -ErrorAction SilentlyContinue
foreach ($SkillDir in $SkillDirs) {
    $SkillFiles = Get-ChildItem $SkillDir.FullName -File
    foreach ($SkillFile in $SkillFiles) {
        $RelPath = "skills\$($SkillDir.Name)\$($SkillFile.Name)"
        Install-FileWithBackup -Source $SkillFile.FullName -RelativePath $RelPath
    }
}

# Install rules
Write-Host ""
Write-Host "Installing rules..."
$RulesDir = Join-Path $TemplateDir "rules"
if (Test-Path $RulesDir) {
    $RuleFiles = Get-ChildItem $RulesDir -Filter "*.md" -ErrorAction SilentlyContinue
    foreach ($RuleFile in $RuleFiles) {
        $RelPath = "rules\$($RuleFile.Name)"
        Install-FileWithBackup -Source $RuleFile.FullName -RelativePath $RelPath
    }
}

Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installed components:"
Write-Host "  - CLAUDE.md (global operating system)"
Write-Host "  - settings.json (or settings.storyforge.json for manual merge)"
Write-Host "  - agents/ (portfolio-orchestrator + specialists)"
Write-Host "  - skills/ (kanban-bootstrap, story-write, sprint-groom, release-adapt, doc-update)"
Write-Host "  - rules/ (storyforge-delivery)"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. If settings.storyforge.json was created, merge it into your settings.json"
Write-Host "  2. Start a new Claude Code session to load the StoryForge operating system"
Write-Host "  3. Use /kanban-bootstrap in a project to set up delivery tracking"
Write-Host ""

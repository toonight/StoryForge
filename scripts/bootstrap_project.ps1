#Requires -Version 5.1
<#
.SYNOPSIS
    Bootstrap a project with StoryForge project-level structure.

.DESCRIPTION
    Creates .claude/ and .kanban/ directories with templates.
    Run this from the root of the project you want to bootstrap.

.PARAMETER ProjectName
    Name of the project. Defaults to the current directory name.

.EXAMPLE
    .\scripts\bootstrap_project.ps1
    .\scripts\bootstrap_project.ps1 -ProjectName "MyProject"
#>

[CmdletBinding()]
param(
    [string]$ProjectName
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StoryForgeRoot = Split-Path -Parent $ScriptDir
$TemplateDir = Join-Path $StoryForgeRoot "templates\project"
$ProjectDir = Get-Location
if (-not $ProjectName) {
    $ProjectName = Split-Path -Leaf $ProjectDir
}

Write-Host "=== StoryForge Project Bootstrap ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project:   $ProjectName"
Write-Host "Directory: $ProjectDir"
Write-Host "Templates: $TemplateDir"
Write-Host ""

# Safety check
if ($ProjectDir.Path -eq $StoryForgeRoot) {
    Write-Error "Do not bootstrap the StoryForge repository itself."
    exit 1
}

if (-not (Test-Path $TemplateDir)) {
    Write-Error "Template directory not found: $TemplateDir"
    exit 1
}

$SkipKanban = $false
if (Test-Path (Join-Path $ProjectDir ".kanban")) {
    Write-Host "WARNING: .kanban/ already exists. Skipping Kanban setup." -ForegroundColor Yellow
    $SkipKanban = $true
}

# Create .claude/ structure
Write-Host "Setting up .claude/ ..."
$ClaudeDir = Join-Path $ProjectDir ".claude"
if (-not (Test-Path $ClaudeDir)) {
    New-Item -ItemType Directory -Path $ClaudeDir -Force | Out-Null
}

$ClaudeMdDest = Join-Path $ClaudeDir "CLAUDE.md"
if (-not (Test-Path $ClaudeMdDest)) {
    $Content = (Get-Content (Join-Path $TemplateDir ".claude\CLAUDE.md") -Raw) -replace '\{\{PROJECT_NAME\}\}', $ProjectName
    Set-Content -Path $ClaudeMdDest -Value $Content -NoNewline
    Write-Host "  CREATED: .claude\CLAUDE.md" -ForegroundColor Green
} else {
    Write-Host "  EXISTS:  .claude\CLAUDE.md (skipped)" -ForegroundColor Yellow
}

$SettingsDest = Join-Path $ClaudeDir "settings.json"
if (-not (Test-Path $SettingsDest)) {
    Copy-Item (Join-Path $TemplateDir ".claude\settings.json") $SettingsDest
    Write-Host "  CREATED: .claude\settings.json" -ForegroundColor Green
} else {
    Write-Host "  EXISTS:  .claude\settings.json (skipped)" -ForegroundColor Yellow
}

# Create .claude/rules/
$RulesSourceDir = Join-Path $TemplateDir ".claude\rules"
if (Test-Path $RulesSourceDir) {
    $RulesDestDir = Join-Path $ClaudeDir "rules"
    if (-not (Test-Path $RulesDestDir)) {
        New-Item -ItemType Directory -Path $RulesDestDir -Force | Out-Null
    }
    $RuleFiles = Get-ChildItem $RulesSourceDir -Filter "*.md"
    foreach ($RuleFile in $RuleFiles) {
        $RuleDest = Join-Path $RulesDestDir $RuleFile.Name
        if (-not (Test-Path $RuleDest)) {
            Copy-Item $RuleFile.FullName $RuleDest
            Write-Host "  CREATED: .claude\rules\$($RuleFile.Name)" -ForegroundColor Green
        }
    }
}

# Install project-level skills
$SkillsSourceDir = Join-Path $TemplateDir ".claude\skills"
if (Test-Path $SkillsSourceDir) {
    Write-Host ""
    Write-Host "Installing project skills..."
    $SkillsDestDir = Join-Path $ClaudeDir "skills"
    if (-not (Test-Path $SkillsDestDir)) {
        New-Item -ItemType Directory -Path $SkillsDestDir -Force | Out-Null
    }
    $SkillDirs = Get-ChildItem $SkillsSourceDir -Directory
    foreach ($SkillDir in $SkillDirs) {
        $SkillDest = Join-Path $SkillsDestDir $SkillDir.Name
        if (-not (Test-Path $SkillDest)) {
            New-Item -ItemType Directory -Path $SkillDest -Force | Out-Null
            $SkillFiles = Get-ChildItem $SkillDir.FullName -File
            foreach ($SkillFile in $SkillFiles) {
                Copy-Item $SkillFile.FullName (Join-Path $SkillDest $SkillFile.Name)
            }
            Write-Host "  CREATED: .claude\skills\$($SkillDir.Name)\" -ForegroundColor Green
        } else {
            Write-Host "  EXISTS:  .claude\skills\$($SkillDir.Name)\ (skipped)" -ForegroundColor Yellow
        }
    }
}

# Create .kanban/ structure
if (-not $SkipKanban) {
    Write-Host ""
    Write-Host "Setting up .kanban/ ..."
    $KanbanDir = Join-Path $ProjectDir ".kanban"
    $StoriesDir = Join-Path $KanbanDir "stories"
    $FeaturesDir = Join-Path $KanbanDir "features"
    New-Item -ItemType Directory -Path $StoriesDir -Force | Out-Null
    New-Item -ItemType Directory -Path $FeaturesDir -Force | Out-Null

    $TemplateFiles = @("board.md", "backlog.md", "sprint.md", "decisions.md", "changelog.md")
    foreach ($FileName in $TemplateFiles) {
        $Source = Join-Path $TemplateDir ".kanban\$FileName"
        $Dest = Join-Path $KanbanDir $FileName
        $Content = (Get-Content $Source -Raw) -replace '\{\{PROJECT_NAME\}\}', $ProjectName
        Set-Content -Path $Dest -Value $Content -NoNewline
        Write-Host "  CREATED: .kanban\$FileName" -ForegroundColor Green
    }

    # Copy story template
    Copy-Item (Join-Path $TemplateDir ".kanban\stories\STORY-TEMPLATE.md") (Join-Path $StoriesDir "STORY-TEMPLATE.md")
    Write-Host "  CREATED: .kanban\stories\STORY-TEMPLATE.md" -ForegroundColor Green

    # Copy feature template
    Copy-Item (Join-Path $TemplateDir ".kanban\features\FEAT-TEMPLATE.md") (Join-Path $FeaturesDir "FEAT-TEMPLATE.md")
    Write-Host "  CREATED: .kanban\features\FEAT-TEMPLATE.md" -ForegroundColor Green
}

# Update .gitignore
$GitignorePath = Join-Path $ProjectDir ".gitignore"
if (Test-Path $GitignorePath) {
    $Content = Get-Content $GitignorePath -Raw
    if ($Content -notmatch "settings\.local\.json") {
        Add-Content -Path $GitignorePath -Value "`n# Claude Code local settings`n.claude/settings.local.json`n.claude/agent-memory-local/`n.claude/worktrees/"
        Write-Host "  UPDATED: .gitignore" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "=== Bootstrap Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Edit .claude\CLAUDE.md with project-specific architecture and conventions"
Write-Host "  2. Define your first Initiative in .kanban\backlog.md"
Write-Host "  3. Create your first Story with /story-write"
Write-Host ""

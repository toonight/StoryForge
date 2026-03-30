#Requires -Version 5.1
<#
.SYNOPSIS
    Check Anthropic Claude Code documentation pages for availability.

.DESCRIPTION
    Verifies that all documented URLs in doc-index.md are reachable
    and optionally updates verification dates.

.PARAMETER Update
    Update doc-index.md verification dates for reachable pages.

.EXAMPLE
    .\scripts\sync_upstream_docs.ps1
    .\scripts\sync_upstream_docs.ps1 -Update
#>

[CmdletBinding()]
param(
    [switch]$Update
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StoryForgeRoot = Split-Path -Parent $ScriptDir
$DocIndex = Join-Path $StoryForgeRoot "docs\upstream\doc-index.md"
$Today = Get-Date -Format "yyyy-MM-dd"

Write-Host "=== StoryForge Upstream Documentation Sync ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Date: $Today"
Write-Host ""

if (-not (Test-Path $DocIndex)) {
    Write-Error "doc-index.md not found at $DocIndex"
    exit 1
}

$Docs = @(
    @{Name="CLAUDE.md"; Url="https://code.claude.com/docs/en/claude-md"},
    @{Name="Subagents"; Url="https://code.claude.com/docs/en/sub-agents"},
    @{Name="Hooks"; Url="https://code.claude.com/docs/en/hooks"},
    @{Name="Skills"; Url="https://code.claude.com/docs/en/skills"},
    @{Name="Settings"; Url="https://code.claude.com/docs/en/settings"},
    @{Name="CLI Reference"; Url="https://code.claude.com/docs/en/cli-reference"},
    @{Name="Permission Modes"; Url="https://code.claude.com/docs/en/permission-modes"},
    @{Name="Permissions"; Url="https://code.claude.com/docs/en/permissions"},
    @{Name="Common Workflows"; Url="https://code.claude.com/docs/en/common-workflows"},
    @{Name="Best Practices"; Url="https://code.claude.com/docs/en/best-practices"},
    @{Name="Headless Mode"; Url="https://code.claude.com/docs/en/headless"},
    @{Name="GitHub Actions"; Url="https://code.claude.com/docs/en/github-actions"},
    @{Name="Agent Teams"; Url="https://code.claude.com/docs/en/agent-teams"},
    @{Name="MCP"; Url="https://code.claude.com/docs/en/mcp"}
)

$Reachable = 0
$Unreachable = 0
$UnreachableList = @()

Write-Host "Checking documentation pages..."
Write-Host ""

foreach ($Doc in $Docs) {
    try {
        $Response = Invoke-WebRequest -Uri $Doc.Url -Method Head -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        if ($Response.StatusCode -ge 200 -and $Response.StatusCode -lt 400) {
            Write-Host "  OK: $($Doc.Name)" -ForegroundColor Green
            $Reachable++
        } else {
            Write-Host "  UNREACHABLE: $($Doc.Name) (HTTP $($Response.StatusCode))" -ForegroundColor Red
            $Unreachable++
            $UnreachableList += $Doc
        }
    } catch {
        Write-Host "  UNREACHABLE: $($Doc.Name) ($($_.Exception.Message))" -ForegroundColor Red
        $Unreachable++
        $UnreachableList += $Doc
    }
}

Write-Host ""
Write-Host "=== Results ===" -ForegroundColor Cyan
Write-Host "  Reachable:   $Reachable"
Write-Host "  Unreachable: $Unreachable"

if ($Unreachable -gt 0) {
    Write-Host ""
    Write-Host "Unreachable pages:" -ForegroundColor Yellow
    foreach ($Doc in $UnreachableList) {
        Write-Host "  - $($Doc.Name): $($Doc.Url)"
    }
}

if ($Update -and $Reachable -gt 0) {
    Write-Host ""
    Write-Host "Updating doc-index.md verification dates..."
    $Content = Get-Content $DocIndex -Raw
    $Content = $Content -replace "Last updated: \d{4}-\d{2}-\d{2}", "Last updated: $Today"
    Set-Content -Path $DocIndex -Value $Content -NoNewline
    Write-Host "  Done." -ForegroundColor Green
}

Write-Host ""
if ($Unreachable -gt 0) {
    Write-Host "COMPLETED WITH WARNINGS" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "ALL CHECKS PASSED" -ForegroundColor Green
    exit 0
}

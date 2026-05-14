param(
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[ai-teacher-stack] $Message"
}

function Assert-PortFree {
    param([int]$Port)
    $listener = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
    if ($listener) {
        throw "Port $Port is already in use. Stop the other service before starting the pre-release."
    }
}

function Invoke-Json {
    param([string]$Url)
    return Invoke-RestMethod -Uri $Url -Method Get -TimeoutSec 3
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot

Write-Step "Checking Docker prerequisites"
Get-Command docker | Out-Null
docker compose version | Out-Null

Write-Step "Checking local ports 8010 and 8051"
Assert-PortFree -Port 8010
Assert-PortFree -Port 8051

if (-not (Test-Path ".env")) {
    Write-Step "Creating .env from .env.example"
    Copy-Item ".env.example" ".env"
}

Write-Step "Starting Docker Compose stack"
docker compose up --build -d | Out-Host

Write-Step "Waiting for teacher-tools, Claude-OS, and Redis readiness"
$deadline = (Get-Date).AddMinutes(2)
do {
    Start-Sleep -Seconds 3
    try {
        $status = Invoke-Json -Url "http://localhost:8010/status"
        $claudeHealth = Invoke-Json -Url "http://localhost:8051/health"
        $runningServices = docker compose ps --status running --services
        $redisReady = $runningServices -contains "claude-os-redis"
        if ($status.ready -and $claudeHealth.status -eq "ok" -and $redisReady) {
            break
        }
    } catch {
        # Continue polling until the deadline.
    }
} while ((Get-Date) -lt $deadline)

$finalStatus = Invoke-Json -Url "http://localhost:8010/status"
$finalClaude = Invoke-Json -Url "http://localhost:8051/health"
$finalServices = docker compose ps --status running --services

if (-not ($finalStatus.ready -and $finalClaude.status -eq "ok" -and ($finalServices -contains "claude-os-redis"))) {
    throw "Stack did not become ready in time. Run .\scripts\check-pre-release.ps1 for diagnostics."
}

Write-Host ""
Write-Step "Pre-release is ready"
Write-Host "Claude-OS admin and review UI: http://localhost:8051"
Write-Host "teacher-tools API:           http://localhost:8010"
Write-Host "Stack status:                http://localhost:8010/status"
Write-Host ""
Write-Host "Open Claude Code or Codex App in this workspace folder:"
Write-Host "  $repoRoot"

if ($OpenBrowser) {
    Start-Process "http://localhost:8051"
}

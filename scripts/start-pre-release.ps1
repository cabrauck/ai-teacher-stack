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

function Sync-EnvExample {
    $existingKeys = @{}
    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)=') {
                $existingKeys[$Matches[1]] = $true
            }
        }
    }

    $missingLines = @()
    Get-Content ".env.example" | ForEach-Object {
        if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)=') {
            if (-not $existingKeys.ContainsKey($Matches[1])) {
                $missingLines += $_
            }
        }
    }

    if ($missingLines.Count -gt 0) {
        Add-Content ".env" ""
        Add-Content ".env" "# Added by ai-teacher-stack start script from .env.example"
        $missingLines | ForEach-Object { Add-Content ".env" $_ }
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot

Write-Step "Checking Docker prerequisites"
Get-Command docker | Out-Null
docker compose version | Out-Null

Write-Step "Checking local ports 3080, 8010, and 8051"
Assert-PortFree -Port 3080
Assert-PortFree -Port 8010
Assert-PortFree -Port 8051

if (-not (Test-Path ".env")) {
    Write-Step "Creating .env from .env.example"
    Copy-Item ".env.example" ".env"
} else {
    Write-Step "Checking .env for new runtime keys"
    Sync-EnvExample
}

Write-Step "Starting Docker Compose stack"
docker compose up --build -d | Out-Host

Write-Step "Waiting for LibreChat, teacher-tools, Claude-OS, and Redis readiness"
$deadline = (Get-Date).AddMinutes(2)
do {
    Start-Sleep -Seconds 3
    try {
        $status = Invoke-Json -Url "http://localhost:8010/status"
        $claudeHealth = Invoke-Json -Url "http://localhost:8051/health"
        $runningServices = docker compose ps --status running --services
        $redisReady = $runningServices -contains "claude-os-redis"
        $libreChatReady = $runningServices -contains "librechat"
        if ($status.ready -and $claudeHealth.status -eq "ok" -and $redisReady -and $libreChatReady) {
            break
        }
    } catch {
        # Continue polling until the deadline.
    }
} while ((Get-Date) -lt $deadline)

$finalStatus = Invoke-Json -Url "http://localhost:8010/status"
$finalClaude = Invoke-Json -Url "http://localhost:8051/health"
$finalServices = docker compose ps --status running --services

if (-not ($finalStatus.ready -and $finalClaude.status -eq "ok" -and ($finalServices -contains "claude-os-redis") -and ($finalServices -contains "librechat"))) {
    throw "Stack did not become ready in time. Run .\scripts\check-pre-release.ps1 for diagnostics."
}

Write-Host ""
Write-Step "Pre-release is ready"
Write-Host "LibreChat teacher frontend: http://localhost:3080"
Write-Host "Claude-OS memory runtime:    http://localhost:8051"
Write-Host "teacher-tools API:           http://localhost:8010"
Write-Host "Stack status:                http://localhost:8010/status"
Write-Host ""
Write-Host "Open LibreChat and configure OpenRouter or BYOK provider keys in your local .env."

if ($OpenBrowser) {
    Start-Process "http://localhost:3080"
}

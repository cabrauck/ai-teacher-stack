$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[ai-teacher-stack] $Message"
}

function Try-Json {
    param([string]$Url)
    try {
        return Invoke-RestMethod -Uri $Url -Method Get -TimeoutSec 3
    } catch {
        return $null
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot

Write-Step "Docker services"
docker compose ps | Out-Host
Write-Host ""

$status = Try-Json -Url "http://localhost:8010/status"
if ($null -eq $status) {
    Write-Step "teacher-tools status endpoint is not reachable"
} else {
    Write-Step "teacher-tools aggregated status"
    $status | ConvertTo-Json -Depth 6 | Out-Host
}

Write-Host ""
$librechat = Try-Json -Url "http://localhost:3080"
if ($null -eq $librechat) {
    Write-Step "LibreChat teacher frontend is not reachable"
} else {
    Write-Step "LibreChat teacher frontend is reachable at http://localhost:3080"
}

Write-Host ""
$claudeHealth = Try-Json -Url "http://localhost:8051/health"
if ($null -eq $claudeHealth) {
    Write-Step "Claude-OS health endpoint is not reachable"
} else {
    Write-Step "Claude-OS health"
    $claudeHealth | ConvertTo-Json -Depth 4 | Out-Host
}

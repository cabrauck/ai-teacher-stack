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

function Get-EnvValue {
    param(
        [string]$Key,
        [string]$Default = ""
    )

    if (-not (Test-Path ".env")) {
        return $Default
    }

    $pattern = "^\s*(?:" + [regex]::Escape($Key) + ")=(.*)$"
    foreach ($line in Get-Content ".env") {
        if ($line -match $pattern) {
            return $Matches[1]
        }
    }

    return $Default
}

function Get-EnvPort {
    param(
        [string]$Key,
        [int]$Default
    )

    $rawValue = Get-EnvValue -Key $Key -Default "$Default"
    $parsedValue = 0
    if (-not [int]::TryParse($rawValue, [ref]$parsedValue)) {
        throw "Configured value for $Key must be an integer port. Current value: $rawValue"
    }
    return $parsedValue
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot

$publicHost = Get-EnvValue -Key "STACK_PUBLIC_HOST" -Default "localhost"
$libreChatUrl = "http://${publicHost}:$(Get-EnvPort -Key "HOST_LIBRECHAT_PORT" -Default 3080)"
$teacherToolsStatusUrl = "http://${publicHost}:$(Get-EnvPort -Key "HOST_TEACHER_TOOLS_PORT" -Default 8010)/status"
$claudeHealthUrl = "http://${publicHost}:$(Get-EnvPort -Key "HOST_CLAUDE_OS_PORT" -Default 8051)/health"
$claudeUiUrl = "http://${publicHost}:$(Get-EnvPort -Key "HOST_CLAUDE_OS_FRONTEND_PORT" -Default 5173)"

Write-Step "Docker services"
docker compose ps | Out-Host
Write-Host ""

$status = Try-Json -Url $teacherToolsStatusUrl
if ($null -eq $status) {
    Write-Step "teacher-tools status endpoint is not reachable"
} else {
    Write-Step "teacher-tools aggregated status"
    $status | ConvertTo-Json -Depth 6 | Out-Host
}

Write-Host ""
$librechat = Try-Json -Url $libreChatUrl
if ($null -eq $librechat) {
    Write-Step "LibreChat teacher frontend is not reachable"
} else {
    Write-Step "LibreChat teacher frontend is reachable at $libreChatUrl"
}

Write-Host ""
$claudeUi = $null
try {
    $claudeUi = Invoke-WebRequest -Uri $claudeUiUrl -Method Get -TimeoutSec 3 -UseBasicParsing
} catch {
    $claudeUi = $null
}
if ($null -eq $claudeUi) {
    Write-Step "Claude-OS UI is not reachable"
} else {
    Write-Step "Claude-OS UI is reachable at $claudeUiUrl"
}

Write-Host ""
$claudeHealth = Try-Json -Url $claudeHealthUrl
if ($null -eq $claudeHealth) {
    Write-Step "Claude-OS health endpoint is not reachable"
} else {
    Write-Step "Claude-OS health"
    $claudeHealth | ConvertTo-Json -Depth 4 | Out-Host
}

param(
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "[ai-teacher-stack] $Message"
}

function Test-PortBusy {
    param([int]$Port)
    $listener = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -ne $listener
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

function Set-EnvValue {
    param(
        [string]$Key,
        [string]$Value
    )

    $pattern = "^\s*(?:" + [regex]::Escape($Key) + ")=.*$"
    $lines = if (Test-Path ".env") { Get-Content ".env" } else { @() }
    $updated = $false
    $newLines = [System.Collections.Generic.List[string]]::new()

    foreach ($line in $lines) {
        if (-not $updated -and $line -match $pattern) {
            $newLines.Add("${Key}=${Value}")
            $updated = $true
        } else {
            $newLines.Add($line)
        }
    }

    if (-not $updated) {
        $newLines.Add("${Key}=${Value}")
    }

    Set-Content ".env" -Value $newLines
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

function Select-FreePort {
    param(
        [int]$PreferredPort,
        [int[]]$ReservedPorts = @()
    )

    $port = $PreferredPort
    $attempts = 0
    while ((Test-PortBusy -Port $port) -or ($ReservedPorts -contains $port)) {
        $port += 1
        $attempts += 1
        if ($attempts -ge 200) {
            throw "Could not find a free local port near $PreferredPort."
        }
    }
    return $port
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

function Sync-PublicUrls {
    param(
        [string]$PublicHost,
        [int]$LibreChatPort,
        [int]$TeacherToolsPort,
        [int]$ClaudeOsPort
    )

    $libreChatUrl = "http://${PublicHost}:${LibreChatPort}"
    Set-EnvValue -Key "DOMAIN_CLIENT" -Value $libreChatUrl
    Set-EnvValue -Key "DOMAIN_SERVER" -Value $libreChatUrl

    $managedOrigins = @(
        "http://${PublicHost}:${LibreChatPort}",
        "http://${PublicHost}:${ClaudeOsPort}",
        "http://${PublicHost}:${TeacherToolsPort}",
        "http://127.0.0.1:${LibreChatPort}",
        "http://127.0.0.1:${ClaudeOsPort}",
        "http://127.0.0.1:${TeacherToolsPort}"
    )
    $existingOrigins = (Get-EnvValue -Key "ALLOWED_ORIGINS").Split(",") |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ }
    $preservedOrigins = $existingOrigins | Where-Object {
        $_ -notmatch '^http://(localhost|127\.0\.0\.1):\d+$'
    }
    $allOrigins = @($managedOrigins + $preservedOrigins) | Select-Object -Unique
    Set-EnvValue -Key "ALLOWED_ORIGINS" -Value ($allOrigins -join ",")
}

function Resolve-HostPorts {
    $publicHost = Get-EnvValue -Key "STACK_PUBLIC_HOST" -Default "localhost"
    $configuredPorts = @(
        @{ Key = "HOST_LIBRECHAT_PORT"; Label = "LibreChat"; Default = 3080 },
        @{ Key = "HOST_TEACHER_TOOLS_PORT"; Label = "teacher-tools"; Default = 8010 },
        @{ Key = "HOST_CLAUDE_OS_PORT"; Label = "Claude-OS"; Default = 8051 }
    )
    $selectedPorts = @{}
    $reservedPorts = @()

    foreach ($config in $configuredPorts) {
        $requestedPort = Get-EnvPort -Key $config.Key -Default $config.Default
        $selectedPort = Select-FreePort -PreferredPort $requestedPort -ReservedPorts $reservedPorts
        if ($selectedPort -ne $requestedPort) {
            Write-Step "$($config.Label) host port $requestedPort is already in use; using $selectedPort instead."
        }
        Set-EnvValue -Key $config.Key -Value "$selectedPort"
        $selectedPorts[$config.Key] = $selectedPort
        $reservedPorts += $selectedPort
    }

    Sync-PublicUrls `
        -PublicHost $publicHost `
        -LibreChatPort $selectedPorts["HOST_LIBRECHAT_PORT"] `
        -TeacherToolsPort $selectedPorts["HOST_TEACHER_TOOLS_PORT"] `
        -ClaudeOsPort $selectedPorts["HOST_CLAUDE_OS_PORT"]

    return @{
        PublicHost = $publicHost
        LibreChatPort = $selectedPorts["HOST_LIBRECHAT_PORT"]
        TeacherToolsPort = $selectedPorts["HOST_TEACHER_TOOLS_PORT"]
        ClaudeOsPort = $selectedPorts["HOST_CLAUDE_OS_PORT"]
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Set-Location $repoRoot

Write-Step "Checking Docker prerequisites"
Get-Command docker | Out-Null
docker compose version | Out-Null

if (-not (Test-Path ".env")) {
    Write-Step "Creating .env from .env.example"
    Copy-Item ".env.example" ".env"
} else {
    Write-Step "Checking .env for new runtime keys"
    Sync-EnvExample
}

$runningServices = @(docker compose ps --status running --services 2>$null)
if ($runningServices.Count -gt 0) {
    Write-Step "Reusing configured host ports because this Docker Compose project already has running services"
    $runtimeConfig = @{
        PublicHost = Get-EnvValue -Key "STACK_PUBLIC_HOST" -Default "localhost"
        LibreChatPort = Get-EnvPort -Key "HOST_LIBRECHAT_PORT" -Default 3080
        TeacherToolsPort = Get-EnvPort -Key "HOST_TEACHER_TOOLS_PORT" -Default 8010
        ClaudeOsPort = Get-EnvPort -Key "HOST_CLAUDE_OS_PORT" -Default 8051
    }
    Sync-PublicUrls `
        -PublicHost $runtimeConfig.PublicHost `
        -LibreChatPort $runtimeConfig.LibreChatPort `
        -TeacherToolsPort $runtimeConfig.TeacherToolsPort `
        -ClaudeOsPort $runtimeConfig.ClaudeOsPort
} else {
    Write-Step "Checking host ports and selecting fallbacks when defaults are already in use"
    $runtimeConfig = Resolve-HostPorts
}

$libreChatUrl = "http://$($runtimeConfig.PublicHost):$($runtimeConfig.LibreChatPort)"
$teacherToolsApiUrl = "http://$($runtimeConfig.PublicHost):$($runtimeConfig.TeacherToolsPort)"
$statusUrl = "${teacherToolsApiUrl}/status"
$claudeOsUrl = "http://$($runtimeConfig.PublicHost):$($runtimeConfig.ClaudeOsPort)"
$claudeHealthUrl = "${claudeOsUrl}/health"

Write-Step "Starting Docker Compose stack"
docker compose up --build -d | Out-Host

Write-Step "Waiting for LibreChat, teacher-tools, Claude-OS, and Redis readiness"
$deadline = (Get-Date).AddMinutes(2)
do {
    Start-Sleep -Seconds 3
    try {
        $status = Invoke-Json -Url $statusUrl
        $claudeHealth = Invoke-Json -Url $claudeHealthUrl
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

$finalStatus = Invoke-Json -Url $statusUrl
$finalClaude = Invoke-Json -Url $claudeHealthUrl
$finalServices = docker compose ps --status running --services

if (-not ($finalStatus.ready -and $finalClaude.status -eq "ok" -and ($finalServices -contains "claude-os-redis") -and ($finalServices -contains "librechat"))) {
    throw "Stack did not become ready in time. Run .\scripts\check-pre-release.ps1 for diagnostics."
}

Write-Host ""
Write-Step "Pre-release is ready"
Write-Host "LibreChat teacher frontend: $libreChatUrl"
Write-Host "Claude-OS memory runtime:    $claudeOsUrl"
Write-Host "teacher-tools API:           $teacherToolsApiUrl"
Write-Host "Stack status:                $statusUrl"
Write-Host ""
Write-Host "Open LibreChat and configure OpenRouter or BYOK provider keys in your local .env."

if ($OpenBrowser) {
    Start-Process $libreChatUrl
}

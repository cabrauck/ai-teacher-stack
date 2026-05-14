#!/usr/bin/env bash
set -euo pipefail

OPEN_BROWSER=false
if [[ "${1:-}" == "--open-browser" ]]; then
  OPEN_BROWSER=true
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

log() {
  printf '[ai-teacher-stack] %s\n' "$1"
}

assert_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$1" >&2
    exit 1
  fi
}

is_port_busy() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    lsof -iTCP:"${port}" -sTCP:LISTEN -t >/dev/null 2>&1
    return $?
  fi
  if command -v ss >/dev/null 2>&1; then
    ss -ltn "( sport = :${port} )" | grep -q "${port}"
    return $?
  fi
  if command -v netstat >/dev/null 2>&1; then
    netstat -an 2>/dev/null | grep -E "[\.:]${port}[[:space:]].*LISTEN" >/dev/null 2>&1
    return $?
  fi
  return 1
}

cd "${REPO_ROOT}"

log "Checking Docker prerequisites"
assert_command docker
assert_command curl
docker compose version >/dev/null

log "Checking local ports 8010 and 8051"
for port in 8010 8051; do
  if is_port_busy "${port}"; then
    printf 'Port %s is already in use. Stop the other service before starting the pre-release.\n' "${port}" >&2
    exit 1
  fi
done

if [[ ! -f .env ]]; then
  log "Creating .env from .env.example"
  cp .env.example .env
fi

log "Starting Docker Compose stack"
docker compose up --build -d

log "Waiting for teacher-tools, Claude-OS, and Redis readiness"
deadline=$((SECONDS + 120))
while (( SECONDS < deadline )); do
  if status_json="$(curl -fsS http://localhost:8010/status 2>/dev/null)" \
    && curl -fsS http://localhost:8051/health >/dev/null 2>&1 \
    && echo "${status_json}" | grep -Eq '"ready"[[:space:]]*:[[:space:]]*true' \
    && docker compose ps --status running --services | grep -qx 'claude-os-redis'; then
    break
  fi
  sleep 3
done

status_json="$(curl -fsS http://localhost:8010/status)"
curl -fsS http://localhost:8051/health >/dev/null
docker compose ps --status running --services | grep -qx 'claude-os-redis'
echo "${status_json}" | grep -Eq '"ready"[[:space:]]*:[[:space:]]*true'

printf '\n'
log "Pre-release is ready"
printf 'Claude-OS admin and review UI: http://localhost:8051\n'
printf 'teacher-tools API:           http://localhost:8010\n'
printf 'Stack status:                http://localhost:8010/status\n\n'
printf 'Open Claude Code or Codex App in this workspace folder:\n  %s\n' "${REPO_ROOT}"

if [[ "${OPEN_BROWSER}" == "true" ]]; then
  if command -v open >/dev/null 2>&1; then
    open "http://localhost:8051"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:8051" >/dev/null 2>&1 &
  fi
fi

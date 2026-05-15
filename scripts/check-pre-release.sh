#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

log() {
  printf '[ai-teacher-stack] %s\n' "$1"
}

cd "${REPO_ROOT}"

log "Docker services"
docker compose ps
printf '\n'

if status_json="$(curl -fsS http://localhost:8010/status 2>/dev/null)"; then
  log "teacher-tools aggregated status"
  printf '%s\n' "${status_json}"
else
  log "teacher-tools status endpoint is not reachable"
fi

printf '\n'
if curl -fsS http://localhost:3080 >/dev/null 2>&1; then
  log "LibreChat teacher frontend is reachable at http://localhost:3080"
else
  log "LibreChat teacher frontend is not reachable"
fi

printf '\n'
if claude_json="$(curl -fsS http://localhost:8051/health 2>/dev/null)"; then
  log "Claude-OS health"
  printf '%s\n' "${claude_json}"
else
  log "Claude-OS health endpoint is not reachable"
fi

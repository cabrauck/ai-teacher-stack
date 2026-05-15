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

sync_env_example() {
  local tmp_file
  tmp_file="$(mktemp)"
  awk -F= '/^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*=/ {gsub(/^[[:space:]]+|[[:space:]]+$/, "", $1); print $1}' .env \
    | sort -u > "${tmp_file}"

  local missing_lines=()
  while IFS= read -r line; do
    if [[ "${line}" =~ ^[[:space:]]*([A-Za-z_][A-Za-z0-9_]*)= ]]; then
      if ! grep -qx "${BASH_REMATCH[1]}" "${tmp_file}"; then
        missing_lines+=("${line}")
      fi
    fi
  done < .env.example

  rm -f "${tmp_file}"
  if (( ${#missing_lines[@]} > 0 )); then
    {
      printf '\n# Added by ai-teacher-stack start script from .env.example\n'
      printf '%s\n' "${missing_lines[@]}"
    } >> .env
  fi
}

cd "${REPO_ROOT}"

log "Checking Docker prerequisites"
assert_command docker
assert_command curl
docker compose version >/dev/null

log "Checking local ports 3080, 8010, and 8051"
for port in 3080 8010 8051; do
  if is_port_busy "${port}"; then
    printf 'Port %s is already in use. Stop the other service before starting the pre-release.\n' "${port}" >&2
    exit 1
  fi
done

if [[ ! -f .env ]]; then
  log "Creating .env from .env.example"
  cp .env.example .env
else
  log "Checking .env for new runtime keys"
  sync_env_example
fi

log "Starting Docker Compose stack"
docker compose up --build -d

log "Waiting for LibreChat, teacher-tools, Claude-OS, and Redis readiness"
deadline=$((SECONDS + 120))
while (( SECONDS < deadline )); do
  if status_json="$(curl -fsS http://localhost:8010/status 2>/dev/null)" \
    && curl -fsS http://localhost:8051/health >/dev/null 2>&1 \
    && echo "${status_json}" | grep -Eq '"ready"[[:space:]]*:[[:space:]]*true' \
    && docker compose ps --status running --services | grep -qx 'claude-os-redis' \
    && docker compose ps --status running --services | grep -qx 'librechat'; then
    break
  fi
  sleep 3
done

status_json="$(curl -fsS http://localhost:8010/status)"
curl -fsS http://localhost:8051/health >/dev/null
docker compose ps --status running --services | grep -qx 'claude-os-redis'
docker compose ps --status running --services | grep -qx 'librechat'
echo "${status_json}" | grep -Eq '"ready"[[:space:]]*:[[:space:]]*true'

printf '\n'
log "Pre-release is ready"
printf 'LibreChat teacher frontend: http://localhost:3080\n'
printf 'Claude-OS memory runtime:    http://localhost:8051\n'
printf 'teacher-tools API:           http://localhost:8010\n'
printf 'Stack status:                http://localhost:8010/status\n\n'
printf 'Open LibreChat and configure OpenRouter or BYOK provider keys in your local .env.\n'

if [[ "${OPEN_BROWSER}" == "true" ]]; then
  if command -v open >/dev/null 2>&1; then
    open "http://localhost:3080"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:3080" >/dev/null 2>&1 &
  fi
fi

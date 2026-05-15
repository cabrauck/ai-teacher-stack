#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

log() {
  printf '[ai-teacher-stack] %s\n' "$1"
}

get_env_value() {
  local key="$1"
  local default_value="${2:-}"
  if [[ ! -f .env ]]; then
    printf '%s\n' "${default_value}"
    return
  fi

  local value
  value="$(awk -F= -v key="${key}" '$1 == key { sub(/^[^=]*=/, "", $0); print $0; exit }' .env)"
  if [[ -n "${value}" ]]; then
    printf '%s\n' "${value}"
  else
    printf '%s\n' "${default_value}"
  fi
}

get_env_port() {
  local key="$1"
  local default_port="$2"
  local value
  value="$(get_env_value "${key}" "${default_port}")"
  if [[ ! "${value}" =~ ^[0-9]+$ ]]; then
    printf 'Configured value for %s must be an integer port. Current value: %s\n' "${key}" "${value}" >&2
    exit 1
  fi
  printf '%s\n' "${value}"
}

cd "${REPO_ROOT}"

public_host="$(get_env_value "STACK_PUBLIC_HOST" "localhost")"
librechat_url="http://${public_host}:$(get_env_port "HOST_LIBRECHAT_PORT" "3080")"
teacher_tools_status_url="http://${public_host}:$(get_env_port "HOST_TEACHER_TOOLS_PORT" "8010")/status"
claude_os_health_url="http://${public_host}:$(get_env_port "HOST_CLAUDE_OS_PORT" "8051")/health"

log "Docker services"
docker compose ps
printf '\n'

if status_json="$(curl -fsS "${teacher_tools_status_url}" 2>/dev/null)"; then
  log "teacher-tools aggregated status"
  printf '%s\n' "${status_json}"
else
  log "teacher-tools status endpoint is not reachable"
fi

printf '\n'
if curl -fsS "${librechat_url}" >/dev/null 2>&1; then
  log "LibreChat teacher frontend is reachable at ${librechat_url}"
else
  log "LibreChat teacher frontend is not reachable"
fi

printf '\n'
if claude_json="$(curl -fsS "${claude_os_health_url}" 2>/dev/null)"; then
  log "Claude-OS health"
  printf '%s\n' "${claude_json}"
else
  log "Claude-OS health endpoint is not reachable"
fi

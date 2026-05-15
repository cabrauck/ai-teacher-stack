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

set_env_value() {
  local key="$1"
  local value="$2"
  local tmp_file
  tmp_file="$(mktemp)"
  awk -v key="${key}" -v value="${value}" '
    BEGIN { updated = 0 }
    $0 ~ ("^" key "=") && updated == 0 {
      print key "=" value
      updated = 1
      next
    }
    { print }
    END {
      if (updated == 0) {
        print key "=" value
      }
    }
  ' .env > "${tmp_file}"
  mv "${tmp_file}" .env
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

select_free_port() {
  local preferred_port="$1"
  shift || true
  local reserved_ports=("$@")
  local port="${preferred_port}"
  local attempts=0

  while :; do
    if ! is_port_busy "${port}" && ! printf '%s\n' "${reserved_ports[@]:-}" | grep -qx "${port}"; then
      printf '%s\n' "${port}"
      return
    fi
    port=$((port + 1))
    attempts=$((attempts + 1))
    if (( attempts >= 200 )); then
      printf 'Could not find a free local port near %s\n' "${preferred_port}" >&2
      exit 1
    fi
  done
}

sync_public_urls() {
  local public_host="$1"
  local librechat_port="$2"
  local teacher_tools_port="$3"
  local claude_os_port="$4"

  local librechat_url="http://${public_host}:${librechat_port}"
  set_env_value "DOMAIN_CLIENT" "${librechat_url}"
  set_env_value "DOMAIN_SERVER" "${librechat_url}"

  local existing_origins preserved_origins managed_origins allowed_origins
  existing_origins="$(get_env_value "ALLOWED_ORIGINS" "")"
  preserved_origins="$(
    printf '%s' "${existing_origins}" \
      | tr ',' '\n' \
      | sed 's/^[[:space:]]*//; s/[[:space:]]*$//' \
      | grep -Ev '^$|^http://(localhost|127\.0\.0\.1):[0-9]+$' || true
  )"
  managed_origins="$(
    printf '%s\n' \
      "http://${public_host}:${librechat_port}" \
      "http://${public_host}:${claude_os_port}" \
      "http://${public_host}:${teacher_tools_port}" \
      "http://127.0.0.1:${librechat_port}" \
      "http://127.0.0.1:${claude_os_port}" \
      "http://127.0.0.1:${teacher_tools_port}"
  )"
  allowed_origins="$(
    {
      printf '%s\n' "${managed_origins}"
      printf '%s\n' "${preserved_origins}"
    } | awk 'NF && !seen[$0]++ { print }' | paste -sd ',' -
  )"
  set_env_value "ALLOWED_ORIGINS" "${allowed_origins}"
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

if [[ ! -f .env ]]; then
  log "Creating .env from .env.example"
  cp .env.example .env
else
  log "Checking .env for new runtime keys"
  sync_env_example
fi

running_services="$(docker compose ps --status running --services 2>/dev/null || true)"
public_host="$(get_env_value "STACK_PUBLIC_HOST" "localhost")"

if [[ -n "${running_services}" ]]; then
  log "Reusing configured host ports because this Docker Compose project already has running services"
  librechat_port="$(get_env_port "HOST_LIBRECHAT_PORT" "3080")"
  teacher_tools_port="$(get_env_port "HOST_TEACHER_TOOLS_PORT" "8010")"
  claude_os_port="$(get_env_port "HOST_CLAUDE_OS_PORT" "8051")"
  sync_public_urls "${public_host}" "${librechat_port}" "${teacher_tools_port}" "${claude_os_port}"
else
  log "Checking host ports and selecting fallbacks when defaults are already in use"

  librechat_requested_port="$(get_env_port "HOST_LIBRECHAT_PORT" "3080")"
  librechat_port="$(select_free_port "${librechat_requested_port}")"
  if [[ "${librechat_port}" != "${librechat_requested_port}" ]]; then
    log "LibreChat host port ${librechat_requested_port} is already in use; using ${librechat_port} instead."
  fi
  set_env_value "HOST_LIBRECHAT_PORT" "${librechat_port}"

  teacher_tools_requested_port="$(get_env_port "HOST_TEACHER_TOOLS_PORT" "8010")"
  teacher_tools_port="$(select_free_port "${teacher_tools_requested_port}" "${librechat_port}")"
  if [[ "${teacher_tools_port}" != "${teacher_tools_requested_port}" ]]; then
    log "teacher-tools host port ${teacher_tools_requested_port} is already in use; using ${teacher_tools_port} instead."
  fi
  set_env_value "HOST_TEACHER_TOOLS_PORT" "${teacher_tools_port}"

  claude_os_requested_port="$(get_env_port "HOST_CLAUDE_OS_PORT" "8051")"
  claude_os_port="$(select_free_port "${claude_os_requested_port}" "${librechat_port}" "${teacher_tools_port}")"
  if [[ "${claude_os_port}" != "${claude_os_requested_port}" ]]; then
    log "Claude-OS host port ${claude_os_requested_port} is already in use; using ${claude_os_port} instead."
  fi
  set_env_value "HOST_CLAUDE_OS_PORT" "${claude_os_port}"

  sync_public_urls "${public_host}" "${librechat_port}" "${teacher_tools_port}" "${claude_os_port}"
fi

librechat_url="http://${public_host}:${librechat_port}"
teacher_tools_api_url="http://${public_host}:${teacher_tools_port}"
teacher_tools_status_url="${teacher_tools_api_url}/status"
claude_os_url="http://${public_host}:${claude_os_port}"
claude_os_health_url="${claude_os_url}/health"

log "Starting Docker Compose stack"
docker compose up --build -d

log "Waiting for LibreChat, teacher-tools, Claude-OS, and Redis readiness"
deadline=$((SECONDS + 120))
while (( SECONDS < deadline )); do
  if status_json="$(curl -fsS "${teacher_tools_status_url}" 2>/dev/null)" \
    && curl -fsS "${claude_os_health_url}" >/dev/null 2>&1 \
    && echo "${status_json}" | grep -Eq '"ready"[[:space:]]*:[[:space:]]*true' \
    && docker compose ps --status running --services | grep -qx 'claude-os-redis' \
    && docker compose ps --status running --services | grep -qx 'librechat'; then
    break
  fi
  sleep 3
done

status_json="$(curl -fsS "${teacher_tools_status_url}")"
curl -fsS "${claude_os_health_url}" >/dev/null
docker compose ps --status running --services | grep -qx 'claude-os-redis'
docker compose ps --status running --services | grep -qx 'librechat'
echo "${status_json}" | grep -Eq '"ready"[[:space:]]*:[[:space:]]*true'

printf '\n'
log "Pre-release is ready"
printf 'LibreChat teacher frontend: %s\n' "${librechat_url}"
printf 'Claude-OS memory runtime:    %s\n' "${claude_os_url}"
printf 'teacher-tools API:           %s\n' "${teacher_tools_api_url}"
printf 'Stack status:                %s\n\n' "${teacher_tools_status_url}"
printf 'Open LibreChat and configure OpenRouter or BYOK provider keys in your local .env.\n'

if [[ "${OPEN_BROWSER}" == "true" ]]; then
  if command -v open >/dev/null 2>&1; then
    open "${librechat_url}"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "${librechat_url}" >/dev/null 2>&1 &
  fi
fi

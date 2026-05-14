#!/usr/bin/env bash
set -euo pipefail

mkdir -p \
  /workspace/.claude-os/data \
  /workspace/.claude-os/logs \
  /workspace/.claude-os/uploads \
  /workspace/vault/Sources \
  /workspace/vault/Wiki

cd /opt/claude-os

export SQLITE_DB_PATH="${SQLITE_DB_PATH:-/workspace/.claude-os/data/claude-os.db}"
export UPLOAD_DIR="${UPLOAD_DIR:-/workspace/.claude-os/uploads}"
export REDIS_HOST="${REDIS_HOST:-claude-os-redis}"
export REDIS_PORT="${REDIS_PORT:-6379}"
export MCP_SERVER_HOST="${MCP_SERVER_HOST:-0.0.0.0}"
export MCP_SERVER_PORT="${MCP_SERVER_PORT:-8051}"
export OLLAMA_HOST="${OLLAMA_HOST:-http://host.docker.internal:11434}"
export ALLOWED_ORIGINS="${ALLOWED_ORIGINS:-http://localhost:5173,http://localhost:8051,http://localhost:8010,http://127.0.0.1:5173,http://127.0.0.1:8051,http://127.0.0.1:8010}"

if [ "${CLAUDE_OS_BOOTSTRAP_WIKI_KB:-true}" = "true" ]; then
  if python /usr/local/bin/claude-os-bootstrap-vault.py \
      >> /workspace/.claude-os/logs/bootstrap.log 2>&1; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) Claude-OS vault bootstrap finished" \
      >> /workspace/.claude-os/logs/bootstrap.log
  else
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) Claude-OS vault bootstrap failed; continuing startup" \
      >> /workspace/.claude-os/logs/bootstrap.log
  fi
fi

worker_pid=""
if [ "${CLAUDE_OS_RUN_WORKERS:-true}" = "true" ]; then
  python -c "from app.core.redis_config import start_redis_workers; start_redis_workers()" \
    > /workspace/.claude-os/logs/rq_workers.log 2>&1 &
  worker_pid="$!"
fi

cleanup() {
  if [ -n "$worker_pid" ] && kill -0 "$worker_pid" 2>/dev/null; then
    kill "$worker_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

exec python mcp_server/server.py

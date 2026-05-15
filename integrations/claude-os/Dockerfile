FROM python:3.12-slim

ARG CLAUDE_OS_REPO=https://github.com/brobertsaz/claude-os.git
ARG CLAUDE_OS_COMMIT=ee7b62bc5bf36541018a1c14592bcac2b59022f9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONPATH=/opt/claude-os

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        git \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone "${CLAUDE_OS_REPO}" claude-os \
    && cd claude-os \
    && git checkout "${CLAUDE_OS_COMMIT}"

WORKDIR /opt/claude-os
RUN python - <<'PY'
from pathlib import Path

patches = {
    "mcp_server/server.py": {
        'base_url="http://localhost:11434"': "base_url=Config.OLLAMA_HOST",
    },
    "app/core/rag_engine.py": {
        'base_url="http://localhost:11434"  # Native Ollama (not Docker)': "base_url=Config.OLLAMA_HOST",
    },
}

for filename, replacements in patches.items():
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
PY
RUN python -m venv /opt/claude-os/venv \
    && /opt/claude-os/venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/claude-os/venv/bin/pip install -r requirements.txt

COPY entrypoint.sh /usr/local/bin/claude-os-entrypoint
COPY bootstrap_vault.py /usr/local/bin/claude-os-bootstrap-vault.py
RUN chmod +x /usr/local/bin/claude-os-entrypoint

ENV PATH=/opt/claude-os/venv/bin:$PATH
ENV CLAUDE_OS_PROVIDER=local
ENV MCP_SERVER_HOST=0.0.0.0
ENV MCP_SERVER_PORT=8051
ENV SQLITE_DB_PATH=/workspace/.claude-os/data/claude-os.db
ENV UPLOAD_DIR=/workspace/.claude-os/uploads
ENV REDIS_HOST=claude-os-redis
ENV REDIS_PORT=6379
ENV OLLAMA_HOST=http://host.docker.internal:11434
ENV CLAUDE_OS_BOOTSTRAP_WIKI_KB=true
ENV CLAUDE_OS_BOOTSTRAP_SYNC=true
ENV CLAUDE_OS_PROJECT_NAME=ai-teacher-stack
ENV CLAUDE_OS_WORKSPACE_PATH=/workspace
ENV CLAUDE_OS_WIKI_PATH=/workspace/vault/Wiki
ENV CLAUDE_OS_WIKI_KB_NAME=ai-teacher-stack-wiki
ENV CLAUDE_OS_WIKI_MCP_TYPE=project_memories

EXPOSE 8051

ENTRYPOINT ["claude-os-entrypoint"]

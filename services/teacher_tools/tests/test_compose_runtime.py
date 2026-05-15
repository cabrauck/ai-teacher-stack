from __future__ import annotations

from pathlib import Path


def test_default_compose_includes_core_claude_os_services():
    repo_root = Path(__file__).resolve().parents[3]
    compose = (repo_root / "docker-compose.yml").read_text(encoding="utf-8")
    env_example = (repo_root / ".env.example").read_text(encoding="utf-8")

    assert "  claude-os:" in compose
    assert "  claude-os-frontend:" in compose
    assert "  claude-os-redis:" in compose
    assert '${HOST_CLAUDE_OS_PORT:-8051}:8051' in compose
    assert '${HOST_CLAUDE_OS_FRONTEND_PORT:-5173}:5173' in compose
    assert "dockerfile: frontend.Dockerfile" in compose
    assert "HOST_CLAUDE_OS_FRONTEND_PORT: ${HOST_CLAUDE_OS_FRONTEND_PORT:-5173}" in compose
    assert (
        "VITE_API_URL: http://${STACK_PUBLIC_HOST:-localhost}:"
        "${HOST_CLAUDE_OS_PORT:-8051}"
    ) in compose
    assert "host.docker.internal:host-gateway" in compose
    assert "./vault:/workspace/vault" in compose
    assert "./.claude-os:/workspace/.claude-os" in compose
    assert "ee7b62bc5bf36541018a1c14592bcac2b59022f9" in compose
    assert "CLAUDE_OS_BOOTSTRAP_WIKI_KB" in compose
    assert "CLAUDE_OS_WIKI_PATH: /workspace/vault/Wiki" in compose
    assert "HOST_CLAUDE_OS_PORT=8051" in env_example
    assert "HOST_CLAUDE_OS_FRONTEND_PORT=5173" in env_example
    assert "ALLOWED_ORIGINS=http://localhost:3080" in env_example


def test_claude_os_wrapper_bootstraps_wiki_knowledge_base():
    repo_root = Path(__file__).resolve().parents[3]
    entrypoint = (repo_root / "integrations/claude-os/entrypoint.sh").read_text(
        encoding="utf-8"
    )
    dockerfile = (repo_root / "integrations/claude-os/Dockerfile").read_text(
        encoding="utf-8"
    )
    frontend_dockerfile = (
        repo_root / "integrations/claude-os/frontend.Dockerfile"
    ).read_text(encoding="utf-8")
    frontend_entrypoint = (
        repo_root / "integrations/claude-os/frontend-entrypoint.sh"
    ).read_text(encoding="utf-8")
    bootstrap = (repo_root / "integrations/claude-os/bootstrap_vault.py").read_text(
        encoding="utf-8"
    )

    assert "claude-os-bootstrap-vault.py" in entrypoint
    assert "COPY bootstrap_vault.py" in dockerfile
    assert "Config.OLLAMA_HOST" in dockerfile
    assert "npm run dev -- --host 0.0.0.0 --port 5173" in frontend_entrypoint
    assert "CLAUDE_OS_API_INTERNAL_URL" in frontend_dockerfile
    assert "CLAUDE_OS_WIKI_PATH" in bootstrap
    assert "project_memories" in bootstrap
    assert "hook.enable_kb_autosync" in bootstrap
    assert "sync_kb_folder" in bootstrap


def test_default_compose_includes_librechat_teacher_frontend_without_duplicate_rag():
    repo_root = Path(__file__).resolve().parents[3]
    compose = (repo_root / "docker-compose.yml").read_text(encoding="utf-8")
    env_example = (repo_root / ".env.example").read_text(encoding="utf-8")
    librechat_config = (repo_root / "integrations/librechat/librechat.yaml").read_text(
        encoding="utf-8"
    )

    assert "  librechat:" in compose
    assert "  librechat-mongodb:" in compose
    assert "  teacher-tools-mcp:" in compose
    assert '${HOST_LIBRECHAT_PORT:-3080}:3080' in compose
    assert '${HOST_TEACHER_TOOLS_PORT:-8010}:8010' in compose
    assert "teacher-tools-mcp:8020" in librechat_config
    assert "claude-os:8051" in librechat_config
    assert "OpenRouter" in librechat_config
    assert "artifacts: true" in librechat_config
    assert "librechat-rag-api" not in compose
    assert "librechat-vectordb" not in compose
    assert "librechat-meilisearch" not in compose
    assert 'SEARCH: "false"' in compose
    assert "HOST_LIBRECHAT_PORT=3080" in env_example
    assert "HOST_TEACHER_TOOLS_PORT=8010" in env_example

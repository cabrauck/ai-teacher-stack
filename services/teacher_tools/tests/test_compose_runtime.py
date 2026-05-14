from __future__ import annotations

from pathlib import Path


def test_default_compose_includes_core_claude_os_services():
    repo_root = Path(__file__).resolve().parents[3]
    compose = (repo_root / "docker-compose.yml").read_text(encoding="utf-8")

    assert "  claude-os:" in compose
    assert "  claude-os-redis:" in compose
    assert "8051:8051" in compose
    assert "./vault:/workspace/vault" in compose
    assert "./.claude-os:/workspace/.claude-os" in compose
    assert "ee7b62bc5bf36541018a1c14592bcac2b59022f9" in compose
    assert "CLAUDE_OS_BOOTSTRAP_WIKI_KB" in compose
    assert "CLAUDE_OS_WIKI_PATH: /workspace/vault/Wiki" in compose


def test_claude_os_wrapper_bootstraps_wiki_knowledge_base():
    repo_root = Path(__file__).resolve().parents[3]
    entrypoint = (repo_root / "integrations/claude-os/entrypoint.sh").read_text(
        encoding="utf-8"
    )
    dockerfile = (repo_root / "integrations/claude-os/Dockerfile").read_text(
        encoding="utf-8"
    )
    bootstrap = (repo_root / "integrations/claude-os/bootstrap_vault.py").read_text(
        encoding="utf-8"
    )

    assert "claude-os-bootstrap-vault.py" in entrypoint
    assert "COPY bootstrap_vault.py" in dockerfile
    assert "CLAUDE_OS_WIKI_PATH" in bootstrap
    assert "project_memories" in bootstrap
    assert "hook.enable_kb_autosync" in bootstrap
    assert "sync_kb_folder" in bootstrap

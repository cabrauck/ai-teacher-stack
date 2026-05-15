from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from teacher_tools import api, stack_status


def _bootstrap_vault(vault_root: Path) -> None:
    (vault_root / "Sources").mkdir(parents=True)
    (vault_root / "Wiki").mkdir(parents=True)
    (vault_root / "Wiki" / "index.md").write_text("# Index\n", encoding="utf-8")
    (vault_root / "Wiki" / "log.md").write_text("# Log\n", encoding="utf-8")


def _stub_non_core_status(monkeypatch) -> None:
    monkeypatch.setattr(
        stack_status,
        "inspect_claude_os_frontend_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://claude-os-frontend:5173",
            "health_url": "http://claude-os-frontend:5173/",
            "reachable": True,
            "http_status": 200,
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_ollama_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://host.docker.internal:11434",
            "reachable": True,
            "available_models": ["llama3.2:3b", "nomic-embed-text"],
            "missing_models": [],
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_tcp_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "host": "claude-os-redis",
            "port": 6379,
            "reachable": True,
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_claude_os_runtime",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "project": {"id": 1, "name": "ai-teacher-stack"},
            "wiki_kb_name": "ai-teacher-stack-wiki",
            "document_count": 1,
            "chunk_count": 1,
            "embedding_coverage": {"status": "ok"},
        },
    )


def test_status_api_reports_ready_stack(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    export_root = tmp_path / "exports"
    _bootstrap_vault(vault_root)
    export_root.mkdir()
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
    monkeypatch.setattr(api.settings, "claude_os_url", "http://claude-os:8051")
    monkeypatch.setattr(api.settings, "claude_os_frontend_url", "http://claude-os-frontend:5173")
    monkeypatch.setattr(api.settings, "librechat_url", "http://librechat:3080")
    _stub_non_core_status(monkeypatch)
    monkeypatch.setattr(
        stack_status,
        "inspect_claude_os_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://claude-os:8051",
            "health_url": "http://claude-os:8051/health",
            "reachable": True,
            "http_status": 200,
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_librechat_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://librechat:3080",
            "health_url": "http://librechat:3080/",
            "reachable": True,
            "http_status": 200,
        },
    )
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["services"]["claude_os"]["status"] == "ok"
    assert payload["services"]["claude_os_frontend"]["status"] == "ok"
    assert payload["services"]["claude_os_redis"]["status"] == "ok"
    assert payload["services"]["librechat"]["status"] == "ok"
    assert payload["capabilities"]["claude_os_runtime"]["document_count"] == 1
    assert payload["storage"]["exports"]["is_empty"] is True
    assert payload["urls"]["librechat"] == "http://localhost:3080"
    assert payload["urls"]["teacher_tools_status"] == "http://localhost:8010/status"
    assert payload["urls"]["claude_os_ui"] == "http://localhost:5173"


def test_status_api_reports_unreachable_claude_os(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    export_root = tmp_path / "exports"
    _bootstrap_vault(vault_root)
    export_root.mkdir()
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
    monkeypatch.setattr(api.settings, "librechat_url", "http://librechat:3080")
    _stub_non_core_status(monkeypatch)
    monkeypatch.setattr(
        stack_status,
        "inspect_claude_os_service",
        lambda *_args, **_kwargs: {
            "status": "error",
            "url": "http://claude-os:8051",
            "health_url": "http://claude-os:8051/health",
            "reachable": False,
            "detail": "connection refused",
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_librechat_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://librechat:3080",
            "health_url": "http://librechat:3080/",
            "reachable": True,
            "http_status": 200,
        },
    )
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["ready"] is False
    assert payload["services"]["claude_os"]["detail"] == "connection refused"


def test_status_api_reports_unreachable_librechat(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    export_root = tmp_path / "exports"
    _bootstrap_vault(vault_root)
    export_root.mkdir()
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
    _stub_non_core_status(monkeypatch)
    monkeypatch.setattr(
        stack_status,
        "inspect_claude_os_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://claude-os:8051",
            "health_url": "http://claude-os:8051/health",
            "reachable": True,
            "http_status": 200,
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_librechat_service",
        lambda *_args, **_kwargs: {
            "status": "error",
            "url": "http://librechat:3080",
            "health_url": "http://librechat:3080/",
            "reachable": False,
            "detail": "connection refused",
        },
    )
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["ready"] is False
    assert payload["services"]["librechat"]["detail"] == "connection refused"


def test_status_api_reports_incomplete_vault_bootstrap(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    export_root = tmp_path / "exports"
    export_root.mkdir()
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
    monkeypatch.setattr(api.settings, "librechat_url", "http://librechat:3080")
    _stub_non_core_status(monkeypatch)
    monkeypatch.setattr(
        stack_status,
        "inspect_claude_os_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://claude-os:8051",
            "health_url": "http://claude-os:8051/health",
            "reachable": True,
            "http_status": 200,
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_librechat_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://librechat:3080",
            "health_url": "http://librechat:3080/",
            "reachable": True,
            "http_status": 200,
        },
    )
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert "Sources" in payload["storage"]["vault"]["missing"]
    assert "Wiki/index.md" in payload["storage"]["memory"]["missing"]


def test_status_api_reports_missing_export_root(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    _bootstrap_vault(vault_root)
    export_root = tmp_path / "exports"
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
    monkeypatch.setattr(api.settings, "librechat_url", "http://librechat:3080")
    _stub_non_core_status(monkeypatch)
    monkeypatch.setattr(
        stack_status,
        "inspect_claude_os_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://claude-os:8051",
            "health_url": "http://claude-os:8051/health",
            "reachable": True,
            "http_status": 200,
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_librechat_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://librechat:3080",
            "health_url": "http://librechat:3080/",
            "reachable": True,
            "http_status": 200,
        },
    )
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["storage"]["exports"]["status"] == "error"
    assert payload["storage"]["exports"]["exists"] is False


def test_status_api_reports_configured_public_urls(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    export_root = tmp_path / "exports"
    _bootstrap_vault(vault_root)
    export_root.mkdir()
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
    monkeypatch.setattr(api.settings, "stack_public_host", "127.0.0.1")
    monkeypatch.setattr(api.settings, "host_librechat_port", 3180)
    monkeypatch.setattr(api.settings, "host_teacher_tools_port", 8110)
    monkeypatch.setattr(api.settings, "host_claude_os_port", 8151)
    monkeypatch.setattr(api.settings, "host_claude_os_frontend_port", 5174)
    _stub_non_core_status(monkeypatch)
    monkeypatch.setattr(
        stack_status,
        "inspect_claude_os_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://claude-os:8051",
            "health_url": "http://claude-os:8051/health",
            "reachable": True,
            "http_status": 200,
        },
    )
    monkeypatch.setattr(
        stack_status,
        "inspect_librechat_service",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "url": "http://librechat:3080",
            "health_url": "http://librechat:3080/",
            "reachable": True,
            "http_status": 200,
        },
    )
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["urls"]["librechat"] == "http://127.0.0.1:3180"
    assert payload["urls"]["teacher_tools_api"] == "http://127.0.0.1:8110"
    assert payload["urls"]["teacher_tools_status"] == "http://127.0.0.1:8110/status"
    assert payload["urls"]["claude_os"] == "http://127.0.0.1:8151"
    assert payload["urls"]["claude_os_ui"] == "http://127.0.0.1:5174"

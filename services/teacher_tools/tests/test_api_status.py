from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from teacher_tools import api, stack_status


def _bootstrap_vault(vault_root: Path) -> None:
    (vault_root / "Sources").mkdir(parents=True)
    (vault_root / "Wiki").mkdir(parents=True)
    (vault_root / "Wiki" / "index.md").write_text("# Index\n", encoding="utf-8")
    (vault_root / "Wiki" / "log.md").write_text("# Log\n", encoding="utf-8")


def test_status_api_reports_ready_stack(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    export_root = tmp_path / "exports"
    _bootstrap_vault(vault_root)
    export_root.mkdir()
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
    monkeypatch.setattr(api.settings, "claude_os_url", "http://claude-os:8051")
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
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["services"]["claude_os"]["status"] == "ok"
    assert payload["storage"]["exports"]["is_empty"] is True


def test_status_api_reports_unreachable_claude_os(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    export_root = tmp_path / "exports"
    _bootstrap_vault(vault_root)
    export_root.mkdir()
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
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
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert payload["ready"] is False
    assert payload["services"]["claude_os"]["detail"] == "connection refused"


def test_status_api_reports_incomplete_vault_bootstrap(tmp_path: Path, monkeypatch):
    vault_root = tmp_path / "vault"
    export_root = tmp_path / "exports"
    export_root.mkdir()
    monkeypatch.setattr(api.settings, "vault_root", vault_root)
    monkeypatch.setattr(api.settings, "export_root", export_root)
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
    client = TestClient(api.app)

    response = client.get("/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["storage"]["exports"]["status"] == "error"
    assert payload["storage"]["exports"]["exists"] is False

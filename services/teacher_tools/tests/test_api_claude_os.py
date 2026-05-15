from __future__ import annotations

from fastapi.testclient import TestClient

from teacher_tools import api


def test_claude_os_memory_status_endpoint_uses_local_runtime(monkeypatch):
    monkeypatch.setattr(
        api,
        "inspect_claude_os_runtime",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "wiki_kb_name": "ai-teacher-stack-wiki",
            "document_count": 3,
        },
    )
    client = TestClient(api.app)

    response = client.get("/claude-os/memory/status")

    assert response.status_code == 200
    assert response.json()["document_count"] == 3


def test_claude_os_memory_sync_endpoint_returns_sync_result(monkeypatch):
    monkeypatch.setattr(
        api,
        "sync_claude_os_memory",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "sync": {"sync_result": {"successful": 1}},
        },
    )
    client = TestClient(api.app)

    response = client.post("/claude-os/memory/sync")

    assert response.status_code == 200
    assert response.json()["sync"]["sync_result"]["successful"] == 1


def test_claude_os_memory_search_endpoint_returns_cited_sources(monkeypatch):
    monkeypatch.setattr(
        api,
        "search_claude_os_memory",
        lambda *_args, **_kwargs: {
            "status": "ok",
            "answer": "Kartenarbeit mit Legende.",
            "sources": [{"path": "Wiki/kartenarbeit.md"}],
        },
    )
    client = TestClient(api.app)

    response = client.post(
        "/claude-os/memory/search",
        json={"query": "Kartenarbeit", "use_hybrid": True},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["sources"][0]["path"] == "Wiki/kartenarbeit.md"

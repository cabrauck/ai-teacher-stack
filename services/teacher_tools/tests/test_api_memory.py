from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from teacher_tools import api


def test_memory_api_creates_source_wiki_and_index(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(api.settings, "vault_root", tmp_path)
    client = TestClient(api.app)

    source_response = client.post(
        "/memory/sources",
        json={
            "title": "Kartenarbeit",
            "body": "Kartenlegenden und Wegbeschreibungen fuer Klasse 3/4.",
            "tags": ["hsu"],
        },
    )
    assert source_response.status_code == 200
    assert source_response.json()["path"].startswith("Sources/")

    wiki_response = client.post(
        "/memory/wiki",
        json={
            "title": "Kartenarbeit",
            "body": "Bewaehrte Struktur fuer Kartenstunden.",
            "tags": ["hsu"],
        },
    )
    assert wiki_response.status_code == 200
    assert wiki_response.json()["path"] == "Wiki/kartenarbeit.md"

    index_response = client.get("/memory/wiki/index")
    assert index_response.status_code == 200
    assert "[[kartenarbeit|Kartenarbeit]]" in index_response.json()["markdown"]


def test_memory_api_blocks_sensitive_promotion(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(api.settings, "vault_root", tmp_path)
    source_dir = tmp_path / "Sources"
    source_dir.mkdir(parents=True)
    (source_dir / "bad.md").write_text(
        "---\ncontains_personal_data: true\n---\n# Bad\n",
        encoding="utf-8",
    )
    client = TestClient(api.app)

    response = client.post("/memory/wiki/promote", json={"source_path": "Sources/bad.md"})

    assert response.status_code == 400
    assert "blocked by privacy policy" in response.json()["detail"]

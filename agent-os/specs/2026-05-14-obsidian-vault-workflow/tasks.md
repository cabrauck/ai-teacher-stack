# Tasks: Obsidian LTM and Claude-OS Core Runtime

Status: Done

## Implementation

- [x] Add deterministic memory path and slug helpers.
- [x] Add `vault/Sources/` and `vault/Wiki/` skeletons.
- [x] Add source note, wiki page, index, log, and promotion functions.
- [x] Add privacy validation before wiki writes and promotion.
- [x] Add FastAPI `/memory/...` endpoints.
- [x] Add Claude-OS Docker wrapper pinned to upstream commit.
- [x] Add Claude-OS and Redis to default Docker Compose.
- [x] Add automatic Claude-OS KB bootstrap for `vault/Wiki/`.
- [x] Add `.claude-os/` local state skeleton and ignore rules.
- [x] Update release package allowlist and boundary checks.
- [x] Update roadmap, architecture, privacy, quickstart, and agent docs.

## Verification

- [x] Add unit tests for memory path, index, log, and privacy behavior.
- [x] Add API tests for memory endpoints.
- [x] Add release-boundary test coverage for Claude-OS and vault skeletons.
- [x] Add Compose service presence test.
- [x] Run `uv run ruff check .`.
- [x] Run `uv run pytest`.
- [x] Run `python scripts/build_release.py --version dev --check`.
- [x] Run `docker compose config` when Docker is available.

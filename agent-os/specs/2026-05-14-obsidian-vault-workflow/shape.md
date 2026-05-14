# Obsidian LTM and Claude-OS Core Runtime - Shaping Notes

## Decisions

- Claude-OS is core, not optional.
- Obsidian is the visible source of truth for teacher memory.
- `vault/Wiki/` is the only default Claude-OS indexing target.
- `vault/Sources/` is curated input and must be promoted before indexing.
- Windows support is via Docker Desktop with WSL2.
- macOS support is via Docker Desktop.
- Agent-OS is separate from runtime memory and teacher frontend concerns.

## Risks

- Upstream Claude-OS has no release tags in current inspection, so the Docker
  wrapper uses a commit pin.
- Claude-OS local provider may need Ollama for full search quality, but tests
  and deterministic teacher-tools flows must not require Ollama.
- Real memory data must remain local and release-excluded.

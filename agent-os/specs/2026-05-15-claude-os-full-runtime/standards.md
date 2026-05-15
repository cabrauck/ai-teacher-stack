# Standards: Claude-OS Full Runtime Integration

- `contributor-workflow`: this is Agent-OS-scoped work because it changes
  runtime services, release docs, vault behavior, and privacy-sensitive memory
  indexing.
- `privacy-boundary`: Claude-OS may index only privacy-checked `vault/Wiki`
  content by default.
- `security-compliance`: local-first storage, no secrets in docs/tests, no
  compliance certification claims, and explicit degraded status when optional
  local model capabilities are missing.
- `document-output`: Obsidian-compatible Markdown remains readable without a
  custom app; generated material still needs teacher review.
- `python`: shared behavior belongs in pure functions under `teacher_tools`,
  with FastAPI/MCP wrappers kept thin.

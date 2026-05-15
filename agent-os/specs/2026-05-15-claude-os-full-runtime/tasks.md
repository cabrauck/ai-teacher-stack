# Tasks: Claude-OS Full Runtime Integration

Status: Ready

## Phase 1: Audit and Runtime Truth

- [x] Verify current Docker Compose services and exposed ports.
- [x] Verify upstream Claude-OS frontend exists in the built image.
- [x] Verify current backend routes for projects, KBs, jobs, services,
  semantic indexing, and RAG modes.
- [x] Verify current database bootstrap state and document counts.
- [x] Record the implementation gap in roadmap and architecture docs.

## Phase 2: Claude-OS UI Exposure

- [ ] Add a `claude-os-frontend` runtime service or production-served frontend
  path for the upstream React/Vite UI.
- [ ] Add `HOST_CLAUDE_OS_FRONTEND_PORT` and update Windows and shell start
  scripts to select fallback ports.
- [ ] Configure frontend API base URL to reach `claude-os:8051` inside Docker
  and the published API URL from the browser.
- [ ] Update check scripts and status output to print the Claude-OS UI URL
  separately from the API/MCP URL.
- [ ] Add Compose and release-boundary tests for the frontend runtime files and
  port configuration.

## Phase 3: Memory Sync and Indexing Proof

- [ ] Extend teacher-tools status with Claude-OS project, KB, folder hook,
  document count, embedding count, and last sync information.
- [ ] Add a local-only test helper or API check that proves a
  privacy-checked `vault/Wiki` page can sync into the Claude-OS wiki KB.
- [ ] Add an explicit sync action for `vault/Wiki` from teacher-tools or startup
  diagnostics, while keeping writes privacy-gated.
- [ ] Add semantic indexing status and a clear degraded state when
  `nomic-embed-text` or the configured embedding model is unavailable.
- [ ] Add tests that use local HTTP stubs or SQLite fixtures; do not call
  external APIs in tests.

## Phase 4: RAG and Local LLM Controls

- [ ] Expose documented teacher-safe toggles for vector search, hybrid search,
  reranking, and agentic RAG.
- [ ] Decide whether those toggles live in Claude-OS UI only, LibreChat agent
  instructions, teacher-tools APIs, or all three.
- [ ] Add prompt guidance so LibreChat uses Claude-OS memory intentionally and
  cites local wiki pages when memory is used.
- [ ] Report local Ollama model availability and missing model names in the
  teacher-tools status endpoint.
- [ ] Keep cloud-model prompts explicit about what local memory context is being
  sent to OpenRouter or any other provider.

## Phase 5: LibreChat Visible Memory and Documents

- [ ] Add teacher-tools MCP tools that list `vault/Wiki` memory pages in a
  teacher-readable format.
- [ ] Add teacher-tools MCP tools that read or summarize a selected wiki memory
  page with local path citation.
- [ ] Add teacher-tools MCP tools that list generated/exported documents under
  `exports/` with type, filename, and path.
- [ ] Add Claude-OS-backed tools that list KBs, documents, document counts,
  embedding coverage, jobs, and last sync state after Phase 3 proves the sync
  path.
- [ ] Add a Claude-OS memory search tool for LibreChat that returns cited local
  results and makes clear when vector/hybrid/rerank/agentic modes were used.
- [ ] Add LibreChat preset instructions for Teacher Material Assistant: show
  memory/documents on request, cite local paths, and never imply sensitive
  student data should be stored.
- [ ] Decide whether a richer visible surface is best delivered as a
  teacher-tools dashboard linked from LibreChat or an artifact view. Do not
  fork or patch LibreChat core for this milestone.
- [ ] Add tests for each visible tool response shape.

## Phase 6: Karpathy Obsidian Workflow

- [ ] Add a teacher-memory schema document for the wiki conventions,
  frontmatter, source references, cross-links, index, and log format.
- [ ] Add ingest workflow documentation for one-source-at-a-time teacher review.
- [ ] Add lint workflow for contradictions, stale claims, orphan pages, missing
  cross-links, and privacy boundary violations.
- [ ] Add helper functions or MCP tools for wiki lint, query-to-wiki filing, and
  index/log maintenance.
- [ ] Add tests for schema output, index/log updates, privacy blocking, and
  Obsidian-compatible links.

## Verification

- [ ] `uv run ruff check .`
- [ ] `uv run pytest`
- [ ] `python scripts/build_release.py --version dev --check`
- [ ] `docker compose config`
- [ ] Windows PowerShell pre-release start/check flow
- [ ] Browser verification for LibreChat and Claude-OS UI

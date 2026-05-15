# Spec: Claude-OS Full Runtime Integration

Status: Ready

## Purpose

Close the gap between the intended Claude-OS role in `ai-teacher-stack` and the
current pre-release implementation. The stack should expose the useful
Claude-OS project, memory, indexing, RAG, local LLM, and UI features while
preserving the teacher-first LibreChat workflow, Obsidian wiki source of truth,
and strict privacy boundary.

## Current Verified State

- The Docker image contains upstream Claude-OS backend and frontend source.
- The current Compose runtime starts only the Claude-OS MCP/API server on
  `8051`; the upstream Vite frontend on `5173` is not started or exposed.
- The Claude-OS backend exposes API routes for projects, knowledge bases,
  jobs, services, project folders, hooks, lifecycle checks, semantic indexing,
  hybrid search, reranking, and agentic RAG.
- Startup bootstraps one `ai-teacher-stack` project and four MCP knowledge
  bases: `knowledge_docs`, `project_profile`, `project_index`, and
  `project_memories`.
- Only `project_memories` is wired to `/workspace/vault/Wiki` with autosync.
- The current verified test instance has zero documents in Claude-OS, so vector
  embeddings and RAG over teacher memory are not yet proven active.
- LibreChat is configured to reach `claude-os-memory` through MCP, but
  teacher-facing prompts and docs do not yet make memory retrieval behavior
  explicit or testable.
- LibreChat does not currently show Claude-OS memories, wiki pages, Claude-OS
  documents, jobs, or RAG status as first-class visible panels. At best they
  are reachable through configured MCP tools.
- Qdrant exists only behind the optional `rag` Compose profile and is not part
  of the default Claude-OS memory path.

## Product Boundary

- LibreChat remains the v1 teacher frontend for normal planning, material
  generation, and export workflows.
- Claude-OS UI is an advanced local memory, project, service, and RAG
  management surface, not the primary teacher planning UI.
- Obsidian-compatible Markdown remains the durable source of truth.
- `vault/Sources/` stores curated raw inputs; `vault/Wiki/` stores
  privacy-checked synthesized wiki pages.
- Claude-OS may index only privacy-checked `vault/Wiki/` content by default.
- OpenRouter and other cloud models may answer teacher prompts, but the local
  memory layer must remain explicit and teacher-reviewed.

## Required Runtime Shape

- Add a `claude-os-frontend` service or equivalent production-served frontend
  path that exposes the upstream Claude-OS UI on a documented host port.
- Keep `claude-os` API/MCP on `8051` and route the frontend to that API.
- Add host-port selection, status reporting, and docs for the Claude-OS
  frontend port.
- Make Claude-OS project, KB, folder, sync, jobs, and services status visible
  in `teacher-tools` aggregated status.
- Add a deterministic bootstrap or health action that can prove whether
  `vault/Wiki` pages are present in Claude-OS documents and whether embeddings
  exist.
- Keep local Ollama optional for basic startup, but clearly report when
  embeddings, semantic indexing, local chat, reranking, or agentic RAG are
  unavailable because required models are missing.

## LibreChat Surface Shape

The integration must make useful Claude-OS and Obsidian memory state visible in
LibreChat, not only technically connected in configuration.

Minimum acceptable v1 surface:

- A teacher can ask LibreChat to show current long-term memories and receive a
  structured list from `vault/Wiki`.
- A teacher can ask LibreChat to open or summarize a named wiki memory page.
- A teacher can ask LibreChat to show generated/exported documents and receive
  local paths plus document type information.
- A teacher can ask LibreChat what Claude-OS knows about the memory index and
  receive KB/document/indexing status.
- When Claude-OS search is used, LibreChat responses identify that local
  Claude-OS memory was used and cite local wiki page paths or KB document names.

Preferred later surface:

- A LibreChat-accessible artifact or custom view shows memory pages, documents,
  Claude-OS KB status, and RAG controls without requiring the teacher to know
  tool names.
- Do not fork or patch LibreChat core for this milestone. If upstream LibreChat
  cannot expose that as a sidebar through configuration or MCP/artifact
  responses, implement a small teacher-tools memory/dashboard surface linked
  from LibreChat instead.

## Karpathy Obsidian Wiki Fit

The Karpathy LLM wiki pattern is adopted as the teacher-memory operating model:

- Raw sources are immutable curated inputs.
- The wiki is the compounding synthesized layer.
- The schema/instructions define how agents maintain the wiki.
- Ingest updates summaries, cross-links, index, and log.
- Query reads the wiki first and can file useful answers back into the wiki.
- Lint checks contradictions, stale claims, orphan pages, missing links, and
  gaps.

For this project, that pattern must be adapted to German school privacy rules:
only privacy-checked, non-personal, teacher-reviewable synthesis may enter
`vault/Wiki` or Claude-OS indexes.

## Acceptance Criteria

- Opening the documented Claude-OS UI URL displays the project dashboard from
  upstream Claude-OS, not a `405 Method Not Allowed` API response.
- The default release docs distinguish LibreChat, Claude-OS UI, Claude-OS
  API/MCP, teacher-tools API, and Obsidian vault roles accurately.
- Stack status reports Claude-OS API, Claude-OS frontend, Redis, Ollama
  reachability, embedding model availability, project bootstrap, wiki folder
  hook, document count, and embedding coverage.
- A privacy-checked wiki page created through teacher-tools appears in
  `vault/Wiki`, syncs or can be synced into the Claude-OS wiki KB, and is
  searchable through Claude-OS MCP/API.
- Semantic indexing is triggered explicitly or automatically when the configured
  embedding model is available, and skipped with a clear degraded status when
  it is not.
- LibreChat can call teacher-tools and Claude-OS MCP tools from the Teacher
  Material Assistant preset.
- LibreChat can display memory and document lists through teacher-facing
  MCP tools or artifacts, with tests proving the tools return useful structured
  output.
- Tests cover Compose services, release package contents, status reporting,
  bootstrap state inspection, and at least one API-level memory sync/search
  path without calling external APIs.

## Non-goals

- Do not make Ollama mandatory for basic lesson generation, exports, or stack
  startup.
- Do not index `vault/Sources/`, exports, credentials, or school-confidential
  folders by default.
- Do not add student records, grades, diagnoses, parent communication, health
  data, or sensitive individual cases.
- Do not claim certified DSGVO, BSI IT-Grundschutz, or NIS2 compliance.
- Do not replace LibreChat with Claude-OS UI as the v1 teacher frontend.

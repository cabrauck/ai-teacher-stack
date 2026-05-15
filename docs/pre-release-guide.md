# Pre-Release Guide

## Goal of This Pre-Release

This pre-release is meant to be **usable by a teacher on a local workstation**
without turning the project into a large custom web app.

The intended shape is:

- **LibreChat** for normal teacher work
- **Claude-OS API/MCP** for local memory runtime integration
- **Obsidian-compatible vault files** as the durable local workspace
- **teacher-tools API/MCP** as the local service boundary

## What Is Ready Today

- Start, stop, and readiness scripts for Windows and shell-based platforms
- Local Docker Compose runtime
- LibreChat teacher frontend at `http://localhost:3080`
- Claude-OS UI at `http://localhost:5173`
- Claude-OS API/MCP runtime with local state under `.claude-os/`
- teacher-tools MCP integration for LibreChat
- Curriculum search
- Lesson planning API
- Schriftwesen and handover generation
- DOCX export
- Privacy-checked wiki memory workflow

## What Claude-OS Exposes Today

Use the Claude-OS UI at `http://localhost:5173` for:

- project dashboard
- MCP and KB review
- service and job status
- RAG mode controls and manual checks

Use the Claude-OS API/MCP service at `http://localhost:8051` for:

- `http://localhost:8051/health` for runtime health
- `http://localhost:8051/docs` for technical API documentation
- MCP access from LibreChat and other configured local clients

The root URL `http://localhost:8051/` is not the web app; it may return
`405 Method Not Allowed`. Use `http://localhost:5173` for the UI.

## What LibreChat Is For

Use LibreChat for:

- drafting lesson structures
- generating artifact-friendly Markdown or HTML previews
- using teacher-tools and Claude-OS through MCP
- listing and reading local `vault/Wiki/` memories through teacher-tools MCP
- listing generated local documents under `exports/`
- showing Claude-OS memory status, KB document counts, sync results, and local
  search results through teacher-tools MCP
- exporting reviewed material to local files
- working with OpenRouter or locally configured BYOK providers

## Teacher Workflow Model

### Unterricht

1. Draft or update a note in `vault/Unterricht/`
2. Search curriculum references with the local API if needed
3. Work with the result in LibreChat
4. Export classroom-ready output to `exports/`

### Schriftwesen

1. Work from `vault/Schriftwesen/` and the templates under
   `vault/Templates/Schriftwesen/`
2. Keep inputs organizational, didactic, curriculum-based, and material-based
3. Export reviewed output locally

### Long-Term Memory

1. Capture raw material in `vault/Sources/`
2. Promote only privacy-checked synthesis into `vault/Wiki/`
3. Let Claude-OS index `vault/Wiki/`, not raw source notes

## Troubleshooting

If the start script fails:

- run the matching `check-pre-release` script
- verify Docker Desktop is running
- if Windows blocks PowerShell scripts from the downloaded ZIP, unblock the
  `.ps1` files in file properties or run them once with
  `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-pre-release.ps1`
- note that the start script can move default host ports `3080`, `8010`, and
  `8051`, and `5173` to the next free local ports and stores the chosen values
  in `.env`
- open `http://localhost:3080`
- open `http://localhost:5173`
- open `http://localhost:8010/status`
- open `http://localhost:8051/health`
- open `http://localhost:8051/docs` for the technical Claude-OS API surface

If Claude-OS is not reachable:

- inspect `docker compose ps`
- inspect the `claude-os` and `claude-os-redis` services
- confirm that `.claude-os/` is writable

If memory bootstrap looks incomplete:

- confirm `vault/Sources/`, `vault/Wiki/`, `vault/Wiki/index.md`, and
  `vault/Wiki/log.md` exist
- run `scripts/init-vault.sh` if you need to re-create starter notes

## Hard Boundaries

- no student names
- no grades
- no diagnoses
- no parent communication
- no credentials in notes
- no confidential school documents in the indexed memory space

Claude-OS may index only privacy-checked content under `vault/Wiki/`.

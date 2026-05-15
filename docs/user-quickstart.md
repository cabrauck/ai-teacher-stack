# ai-teacher-stack

This is the user runtime package for `ai-teacher-stack`. It contains the local
Docker Compose stack, a Claude-OS admin and review UI, sample curriculum data,
prompts, templates, and empty local workspace folders for an Obsidian-compatible
vault and exports.

Claude-OS is part of the default local runtime and remains the core local
memory service over privacy-checked wiki notes in `vault/Wiki/`.

## What You Use For What

- **LibreChat**: primary teacher frontend for planning, writing, previews, and
  tool-assisted workflows at `http://localhost:3080`
- **Claude-OS**: local memory runtime plus admin, review, and status surface at
  `http://localhost:8051`
- **teacher-tools API**: local runtime API at `http://localhost:8010`
- **Obsidian-compatible vault**: your durable local workspace under `vault/`

The current pre-release is intentionally **LibreChat-first**. Claude-OS is
tightly connected behind the interface, but it is not the main teacher
workspace for lesson planning.

## Requirements

- Docker Desktop or Docker Engine with Docker Compose
- Windows: Docker Desktop with the WSL2 backend
- macOS: Docker Desktop
- A terminal in this extracted folder

Optional but recommended:

- OpenRouter API key
- BYOK keys for selected frontier providers if you want to use them directly

## Start

### Windows PowerShell

```powershell
.\scripts\start-pre-release.ps1
```

Open the Claude-OS web UI automatically:

```powershell
.\scripts\start-pre-release.ps1 -OpenBrowser
```

### macOS / Linux shell

```bash
./scripts/start-pre-release.sh
```

Open the Claude-OS web UI automatically:

```bash
./scripts/start-pre-release.sh --open-browser
```

If `.env` does not exist yet, the start script creates it from `.env.example`.

## Check and Stop

Windows PowerShell:

```powershell
.\scripts\check-pre-release.ps1
.\scripts\stop-pre-release.ps1
```

macOS / Linux shell:

```bash
./scripts/check-pre-release.sh
./scripts/stop-pre-release.sh
```

## Local URLs

- LibreChat teacher frontend: `http://localhost:3080`
- Claude-OS admin and review UI: `http://localhost:8051`
- Claude-OS health: `http://localhost:8051/health`
- teacher-tools API: `http://localhost:8010`
- Aggregated stack status: `http://localhost:8010/status`

The aggregated stack status endpoint reports local readiness for:

- teacher-tools
- LibreChat
- Claude-OS reachability
- vault structure
- export structure
- memory bootstrap basics

## Typical First Steps

1. Start the stack with the script for your platform.
2. Open `http://localhost:3080`.
3. Add your OpenRouter key, or configure a BYOK provider in your local `.env`.
4. Use `vault/Unterricht/`, `vault/Schriftwesen/`, and `exports/` as your local
   working folders.
5. Save only privacy-checked long-term memory in `vault/Wiki/`.

## Example Checks

```bash
curl http://localhost:8010/health
curl http://localhost:8051/health
curl http://localhost:8010/status
curl "http://localhost:8010/curriculum/search?q=lesen"
```

Generate an example lesson:

```bash
curl -X POST http://localhost:8010/lessons \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "HSU",
    "grade_band": "3/4",
    "topic": "Orientierung mit Karten",
    "duration_minutes": 45
  }'
```

Generate an example weekly Schriftwesen plan:

```bash
curl -X POST http://localhost:8010/schriftwesen/weekly-plan \
  -H "Content-Type: application/json" \
  -d '{
    "woche": "2026-KW21",
    "klasse": "Klasse 3a",
    "themen": ["Kartenarbeit", "Lesestrategien"],
    "personenbezogene_daten": false
  }'
```

Create a privacy-checked long-term memory wiki note:

```bash
curl -X POST http://localhost:8010/memory/wiki \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Kartenarbeit Routinen",
    "body": "Bewaehrte HSU-Struktur: Einstieg mit Kartensymbolen, Partnerarbeit, Sicherung.",
    "tags": ["hsu", "planung"]
  }'
```

## Local Folders

- `data/curriculum/`: structured curriculum sample data
- `.librechat/`: local LibreChat app state, uploads, and logs
- `vault/`: Obsidian-compatible local notes skeleton
- `vault/Sources/`: curated raw memory notes
- `vault/Wiki/`: privacy-checked long-term memory indexed by Claude-OS
- `.claude-os/`: local Claude-OS databases, logs, uploads, and cache state
- `exports/`: generated documents
- `prompts/`: reusable planning and review prompts
- `templates/`: document templates, including privacy-safe Schriftwesen templates

Run `scripts/init-vault.sh` if you want to create starter vault notes.

## Further Reading

- `docs/pre-release-guide.md`
- `docs/architecture.md`
- `docs/privacy-boundary.md`

## Privacy Boundary

Keep student names, grades, diagnoses, parent communication, credentials,
private school documents, and copyrighted textbook content out of this package
and out of any public repository.

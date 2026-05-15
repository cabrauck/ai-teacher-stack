# Teacher Memory Wiki

The project uses a Karpathy-style LLM wiki pattern adapted for local teacher
work: raw material is collected first, durable synthesis is written into a wiki,
and future agents read the wiki before generating new material.

## Folders

- `vault/Sources/` stores curated raw inputs. It is not indexed by default.
- `vault/Wiki/` stores privacy-checked synthesis and is the Claude-OS memory KB
  folder.
- `vault/Wiki/index.md` is generated from wiki pages.
- `vault/Wiki/log.md` records writes and promotions.

## Wiki Page Schema

```yaml
---
type: memory_wiki
title: Kartenarbeit Routinen
slug: kartenarbeit-routinen
updated_at: 2026-05-15T12:00:00+00:00
privacy_status: no_personal_data_detected
source: Sources/2026-05-15_kartenarbeit.md
tags:
  - hsu
  - planung
---
```

Every page should include a level-1 heading, teacher-review note, concise
synthesis, local source reference, tags, and Obsidian cross-links where helpful.

## Ingest Workflow

1. Add one curated raw input to `vault/Sources/`.
2. Promote only a privacy-checked synthesis into `vault/Wiki/`.
3. Keep generated `Wiki/index.md` and append-only `Wiki/log.md` as audit aids.
4. Sync `vault/Wiki/` into Claude-OS only after privacy validation.
5. When a useful answer creates reusable knowledge, file the reviewed synthesis
   back into `vault/Wiki/`, not into raw sources.

## Lint Workflow

Use the teacher-tools API or LibreChat MCP tools to check the wiki:

```bash
curl http://localhost:8010/memory/wiki/lint
```

The linter checks frontmatter type, privacy status, title presence, index links,
basic cross-linking, local source references, and privacy-boundary violations.
Warnings do not block local startup, but errors must be fixed before treating a
page as approved long-term memory.

## Privacy Rule

Do not store student names, grades, diagnoses, parent communication, health data,
credentials, confidential school documents, or copyrighted textbook content in
`vault/Wiki/` or Claude-OS indexes.

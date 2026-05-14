# Agent Client Setup

This document explains how to configure **Claude Code** and **Codex App** to
work with the `ai-teacher-stack` pre-release.

These instructions are **runtime-safe**. They are intended for the user release
package and do not depend on repo-only files such as `AGENTS.md` or
`CLAUDE.md`.

## Shared Assumptions

- The stack is started locally through the pre-release scripts.
- The workspace root is this extracted `ai-teacher-stack` folder.
- Claude-OS is available locally at `http://localhost:8051`.
- The teacher-tools API is available locally at `http://localhost:8010`.
- The only default Claude-OS memory target is `vault/Wiki/`.

## Common Working Rules

Paste these rules into your client-specific custom instructions or project
instructions.

```text
This workspace is a local-first teacher planning stack.

Use vault/ as the visible source of truth for notes and planning material.
Treat Claude-OS as the core local memory service, but only for privacy-checked
content in vault/Wiki/.
Do not move raw notes from vault/Sources/ into Claude-OS memory without a
privacy review.
Do not suggest storing student names, grades, diagnoses, parent communication,
health information, or confidential school records in notes, exports, or memory.
Prefer local files, Markdown, and DOCX export workflows over inventing a large
custom UI.
Use http://localhost:8010/status to check stack readiness when the local
services may not be available yet.
Use the Claude-OS web UI at http://localhost:8051 only as an admin and review
surface, not as the main teacher planning interface.
```

## Claude Code

### 1. Open the workspace

Open the extracted `ai-teacher-stack` folder in Claude Code.

### 2. Add the local Claude-OS MCP server

Claude Code supports remote HTTP MCP servers.

```bash
claude mcp add-json claude-os '{"type":"http","url":"http://localhost:8051"}'
```

Verify it:

```bash
claude mcp get claude-os
```

Inside Claude Code, use `/mcp` to confirm the server is connected.

### 3. Recommended starter prompt

```text
This is the ai-teacher-stack pre-release workspace. First check
http://localhost:8010/status. Then use vault/, exports/, prompts/, and the
privacy boundary rules as the primary working context.
```

## Codex App

### 1. Open the workspace

Open the extracted `ai-teacher-stack` folder in Codex App.

### 2. Add the local Claude-OS MCP server

You can add the local Claude-OS MCP server with the Codex CLI:

```bash
codex mcp add claudeOs --url http://localhost:8051
```

Verify it:

```bash
codex mcp list
```

If you prefer configuration snippets, add this to `~/.codex/config.toml`:

```toml
[mcp_servers.claudeOs]
url = "http://localhost:8051"
```

### 3. Recommended starter prompt

```text
This is the ai-teacher-stack pre-release workspace. Check the local stack
status first at http://localhost:8010/status. Use vault/ as the working area,
exports/ for generated files, and treat Claude-OS on localhost:8051 as the
admin and memory surface for privacy-checked wiki notes only.
```

## Example Local URLs

- Claude-OS admin and review UI: `http://localhost:8051`
- Claude-OS health: `http://localhost:8051/health`
- teacher-tools API: `http://localhost:8010`
- Aggregated stack status: `http://localhost:8010/status`

## What To Ask The Agent To Do

- review or improve a lesson draft in `vault/Unterricht/`
- prepare a weekly plan in `vault/Schriftwesen/`
- convert a reviewed Markdown note into a local export workflow
- summarize what is already in `vault/Wiki/`
- inspect `http://localhost:8010/status` when startup looks unhealthy

## What Not To Ask The Agent To Store

- student names
- grades
- diagnoses
- parent communication
- health data
- school credentials
- confidential school documents

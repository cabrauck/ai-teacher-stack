# Spec: Enduser Pre-Release

Status: Done

## Purpose

Turn the current local-first stack into an enduser-bedienbares pre-release for
teachers without introducing a new teacher web app or changing Claude-OS away
from its role as the core local memory runtime.

## Product Boundary

- Claude Code and Codex App are the primary working surfaces.
- Claude-OS remains the core local memory service over privacy-checked
  `vault/Wiki/` content.
- The existing Claude-OS web UI is positioned as an admin, review, and status
  surface, not as the main teacher workspace.
- The first pre-release remains a Docker Compose runtime package, not a native
  installer.

## Runtime Shape

- The user release package includes guided start, stop, and readiness helper
  scripts for Windows and macOS/Linux shells.
- `teacher_tools` exposes an aggregated stack status endpoint that reports local
  runtime readiness for the teacher-tools API, Claude-OS reachability, vault
  structure, export structure, and memory bootstrap basics.
- Existing lesson, Schriftwesen, export, and memory endpoints remain stable.

## Documentation Shape

- The release package includes teacher-facing pre-release documentation.
- The release package includes Claude Code and Codex App setup guidance with
  runtime-safe copy-paste snippets for MCP, instructions, and starter prompts.
- Repo-only agent files such as `AGENTS.md` and `CLAUDE.md` remain excluded from
  user packages.

## Non-goals

- Do not add a new large teacher web frontend.
- Do not make the Claude-OS web UI the primary teaching workflow.
- Do not add student-data forms, fields, or examples.
- Do not require native Claude-OS installation.
- Do not add a native installer in this phase.

## Acceptance Criteria

- User-facing helper scripts can check prerequisites, ensure `.env` exists,
  start and stop the stack, wait for local readiness, and print the relevant
  local URLs.
- `teacher_tools` exposes an aggregated stack status endpoint suitable for
  helper scripts and user diagnostics.
- The release package includes user docs, agent-client docs, and runtime-safe
  snippets while keeping dev-only agent files out of the package.
- Tests cover healthy and degraded status responses, updated release boundaries,
  and the presence of new runtime helper files.

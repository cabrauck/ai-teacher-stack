# Obsidian LTM and Claude-OS Core Runtime Plan

Status: In Progress

## Goal

Make Claude-OS a core Dockerized runtime service and make Obsidian-compatible
Markdown the visible long-term-memory layer for teacher workflows.

## Plan Shape

- Add deterministic memory file operations under `teacher_tools.memory`.
- Add thin FastAPI memory endpoints for frontend-agnostic clients.
- Add Docker integration files for pinned upstream Claude-OS.
- Add default Compose services for Claude-OS and Redis.
- Update release packaging so runtime integration files and empty skeletons ship,
  while real memory state stays local.

## Decision

Agent-OS remains the development gate. Claude-OS is the runtime memory service.
Teacher-facing clients are interchangeable.

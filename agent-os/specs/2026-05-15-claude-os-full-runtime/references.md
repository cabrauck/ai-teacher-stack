# References: Claude-OS Full Runtime Integration

## Repository Context

- `docker-compose.yml`
- `integrations/claude-os/Dockerfile`
- `integrations/claude-os/entrypoint.sh`
- `integrations/claude-os/bootstrap_vault.py`
- `integrations/librechat/librechat.yaml`
- `services/teacher_tools/src/teacher_tools/stack_status.py`
- `services/teacher_tools/src/teacher_tools/memory.py`
- `docs/architecture.md`
- `docs/roadmap.md`
- `docs/privacy-boundary.md`
- `agent-os/specs/2026-05-14-obsidian-vault-workflow/spec.md`
- `agent-os/specs/2026-05-15-librechat-v1-frontend/spec.md`

## Verified Runtime Context

- Upstream Claude-OS frontend exists in the built image under
  `/opt/claude-os/frontend`.
- Current wrapper starts `python mcp_server/server.py`, exposing API/MCP on
  `8051`.
- Current wrapper does not start the Vite frontend on `5173`.
- Current database has one `ai-teacher-stack` project, four knowledge bases,
  one `project_memories` folder hook to `/workspace/vault/Wiki`, and zero
  documents in the tested runtime instance.

## External Context

- `https://github.com/brobertsaz/claude-os`
- `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`

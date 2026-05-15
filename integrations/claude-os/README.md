# Claude-OS runtime integration

This directory contains the Docker wrappers that make `brobertsaz/claude-os`
a core ai-teacher-stack runtime service.

The wrapper pins the upstream repository to commit
`ee7b62bc5bf36541018a1c14592bcac2b59022f9`. Update the pin only through a
dedicated Agent-OS-scoped task.

Runtime data is written below `.claude-os/` in the workspace. Do not commit
real databases, logs, uploads, or indexed teacher memory.

`Dockerfile` runs the Claude-OS API/MCP service on container port `8051`.
`frontend.Dockerfile` runs the upstream React/Vite UI on container port `5173`.
The frontend entrypoint rewrites the Vite proxy target to `claude-os:8051` for
container-to-container calls and exposes browser calls through `VITE_API_URL`.

On container startup, `bootstrap_vault.py` creates the local Claude-OS project,
wiki knowledge base, and `project_memories` autosync hook for
`/workspace/vault/Wiki`. It creates empty `index.md` and `log.md` files when
needed. Initial KB sync is best-effort and is skipped when Ollama is not
reachable or the configured embedding model is missing, so basic Docker startup
does not depend on a model runtime.

The API image patches upstream hardcoded `localhost:11434` embedding calls to
use `OLLAMA_HOST`, because Docker containers need the host gateway address for a
native Ollama runtime.

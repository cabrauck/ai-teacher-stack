# Claude-OS runtime integration

This directory contains the Docker wrapper that makes `brobertsaz/claude-os`
a core ai-teacher-stack runtime service.

The wrapper pins the upstream repository to commit
`ee7b62bc5bf36541018a1c14592bcac2b59022f9`. Update the pin only through a
dedicated Agent-OS-scoped task.

Runtime data is written below `.claude-os/` in the workspace. Do not commit
real databases, logs, uploads, or indexed teacher memory.

On container startup, `bootstrap_vault.py` creates the local Claude-OS project,
wiki knowledge base, and `project_memories` autosync hook for
`/workspace/vault/Wiki`. It creates empty `index.md` and `log.md` files when
needed. Initial KB sync is best-effort and is skipped when Ollama is not
reachable or the configured embedding model is missing, so basic Docker startup
does not depend on a model runtime.

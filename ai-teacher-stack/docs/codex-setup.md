# Codex setup

## Recommended use

Use Codex as a coding agent for this repository:

```bash
codex
```

Useful first prompt:

```text
Read AGENTS.md, README.md, and docs/architecture.md. Then run the checks and propose the smallest next implementation step.
```

## MCP docs

OpenAI provides a public documentation MCP server for developer docs. You can add it to Codex with:

```bash
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
codex mcp list
```

## Local commands Codex should know

```bash
make check
make test
make lint
make up
make down
```

## Approval discipline

Ask before:

- installing new system dependencies
- adding external network calls
- changing the privacy boundary
- adding cloud sync features
- adding any student-data data model

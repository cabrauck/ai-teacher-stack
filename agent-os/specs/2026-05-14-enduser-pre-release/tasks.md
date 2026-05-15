# Tasks: Enduser Pre-Release

Status: Done

## Implementation

- [x] Add an Agent-OS spec for the enduser pre-release boundary.
- [x] Add an aggregated `teacher_tools` stack status endpoint.
- [x] Add guided start, stop, and readiness scripts for Windows and POSIX
  shells.
- [x] Let the pre-release start scripts move occupied default host ports to the
  next free local ports and keep derived runtime URLs in sync.
- [x] Update the release package allowlist and required runtime files.
- [x] Add teacher-facing pre-release and agent-client documentation with
  runtime-safe snippets.
- [x] Add Windows PowerShell unblock and per-command ExecutionPolicy bypass
  guidance to user-facing pre-release docs and GitHub Release notes.

## Verification

- [x] Add tests for healthy and degraded stack status behavior.
- [x] Add release-boundary assertions for helper scripts and new docs.
- [x] Run `uv run ruff check .`.
- [x] Run `uv run pytest`.
- [x] Run `python scripts/build_release.py --version dev --check`.

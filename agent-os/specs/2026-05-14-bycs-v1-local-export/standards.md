# Standards for ByCS v1 Local Export

The following repository standards apply:

- `agent-os/standards/python.md`
- `agent-os/standards/privacy-boundary.md`
- `agent-os/standards/document-output.md`

Key implications:

- Keep ByCS behavior in focused modules under `teacher_tools.bycs`.
- Keep exports local-first and deterministic.
- Treat ByCS as a later target system, not as a runtime dependency.
- Keep student names, grades, diagnoses, parent communication, credentials, and
  school-internal confidential data out of examples, tests, manifests, and
  generated package metadata.
- Use Markdown and Office-compatible target formats before any UI or cloud
  integration work.

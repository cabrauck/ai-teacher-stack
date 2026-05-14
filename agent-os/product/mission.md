# Mission

`ai-teacher-stack` is a local-first teacher workspace for material planning,
curriculum-grounded lesson design, Obsidian-based long-term memory, Claude-OS
memory services, and document generation.

The project keeps the normal teacher workflow small and practical:

- Docker Compose runs the local workstation stack.
- The Obsidian-compatible vault is the teacher's durable workspace.
- Claude-OS is the local runtime memory engine over privacy-checked vault wiki content.
- `teacher_tools` provides local service and export behavior.
- Curriculum grounding happens before generated lesson content.
- Markdown and DOCX exports come before UI complexity.
- Teacher frontends stay interchangeable: Claude Code, Codex, a chat LLM, or a
  later UI can use the same local stack.
- Optional local AI support can be added without making it required.
- Contributors can clone the repository, attach their preferred coding IDE or
  agent, run the documented checks, and start from public repo context.

## v1 Boundary

v1 is teacher-only. It supports planning, generic materials, public curriculum references, generated worksheets, generated lesson plans, and anonymized class-level reflection.

v1 does not handle sensitive student data. It must not request, store, generate, or normalize student names, grades, diagnoses, parent communication, health data, behavior incidents, credentials, or school-internal confidential documents.

The project is designed to support compliance-conscious workflows under German
data protection expectations. German data protection expectations are mandatory
project policy. BSI and NIS2 are best-effort engineering alignment targets, not
certification claims.

## Agent-OS Role

Agent-OS is a developer and specification layer for product planning, feature
specs, tasks, and implementation control. It is the first development gate for
larger changes. It is not a teacher frontend, not the runtime memory layer, and
not part of the normal teacher workflow.

Agent-OS also captures contributor workflow and security/compliance standards
so contributors can work from public repository context. Contributors may
propose roadmap changes through issues, specs, or pull requests; maintainer
review decides final roadmap direction, milestone priority, and release timing.

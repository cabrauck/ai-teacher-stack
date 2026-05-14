# Mission

`ai-teacher-stack` is a local-first teacher workspace for material planning, curriculum-grounded lesson design, Obsidian-based material organization, and document generation.

The project keeps the normal teacher workflow small and practical:

- Docker Compose runs the local workstation stack.
- The Obsidian-compatible vault is the teacher's durable workspace.
- `teacher_tools` provides local service and export behavior.
- Curriculum grounding happens before generated lesson content.
- Markdown and DOCX exports come before UI complexity.
- Optional local AI support can be added without making it required.

## v1 Boundary

v1 is teacher-only. It supports planning, generic materials, public curriculum references, generated worksheets, generated lesson plans, and anonymized class-level reflection.

v1 does not handle sensitive student data. It must not request, store, generate, or normalize student names, grades, diagnoses, parent communication, health data, behavior incidents, credentials, or school-internal confidential documents.

## Agent-OS Role

Agent-OS is a developer and specification layer for product planning, feature specs, tasks, and implementation control. It is not a runtime component for teachers and is not part of the normal end-user bootstrap.

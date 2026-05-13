#!/usr/bin/env bash
set -euo pipefail

mkdir -p vault/Lehrplan vault/Unterricht vault/Materialien vault/Reflexion exports data/rag

touch exports/.gitkeep

cat > vault/README.md <<'MD'
# Teacher Vault

This folder is intended to be opened as an Obsidian vault.

Do not commit real student data, private school documents, credentials, or non-public teaching materials.
MD

cat > vault/Unterricht/_template_lesson.md <<'MD'
---
type: lesson
subject:
grade_band:
topic:
date:
curriculum:
---

# Thema

## Lehrplanbezug

## Planung

## Materialien

## Reflexion
MD

echo "Vault initialized."

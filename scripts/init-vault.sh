#!/usr/bin/env bash
set -euo pipefail

mkdir -p \
  vault/Lehrplan \
  vault/Unterricht \
  vault/Materialien \
  vault/Reflexion \
  vault/Schriftwesen \
  vault/Sources \
  vault/Templates/Schriftwesen \
  vault/Wiki \
  vault/Policies \
  exports \
  data/rag \
  .claude-os/data \
  .claude-os/logs \
  .claude-os/uploads \
  .claude-os/redis

touch \
  exports/.gitkeep \
  vault/Sources/.gitkeep \
  vault/Wiki/.gitkeep \
  .claude-os/.gitkeep \
  .claude-os/data/.gitkeep \
  .claude-os/logs/.gitkeep \
  .claude-os/uploads/.gitkeep \
  .claude-os/redis/.gitkeep

cat > vault/README.md <<'MD'
# Teacher Vault

This folder is intended to be opened as an Obsidian vault.

Do not commit real student data, private school documents, credentials, or non-public teaching materials.
MD

cat > vault/Wiki/index.md <<'MD'
# Long-Term Memory Index

Obsidian ist die sichtbare Long-Term-Memory-Oberflaeche. Claude-OS darf nur privacy-gepruefte Wiki-Inhalte indexieren.

## Wiki-Seiten

_Noch keine Wiki-Seiten._
MD

cat > vault/Wiki/log.md <<'MD'
# Long-Term Memory Log

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

cat > vault/Templates/Schriftwesen/wochenplan.template.md <<'MD'
---
typ: wochenplan
woche:
klasse:
personenbezogene_daten: false
status: entwurf
---

# Wochenplan

## Lehrplanbezug

## Tage

## Vertretungsrelevant

MD

cat > vault/Templates/Schriftwesen/top-tagesorganisationsplan.template.md <<'MD'
---
typ: tagesorganisationsplan
datum:
klasse:
personenbezogene_daten: false
status: entwurf
---

# Tagesorganisationsplan

## Tagesziel

## Stunden

## Offene Punkte Fuer Morgen

MD

cat > vault/Templates/Schriftwesen/klassenuebergabe-anonym.template.md <<'MD'
---
typ: klassenuebergabe_anonym
klasse:
zeitraum:
personenbezogene_daten: false
status: entwurf
---

# Klassenuebergabe Anonymisiert

## Aktueller Stand

## Laufende Reihen

## Routinen

## Offene To-dos

MD

cat > vault/Policies/schriftwesen.md <<'MD'
# Schriftwesen Policy

Schriftwesen umfasst Wochenplan, Tagesorganisationsplan, Vertretungsplan und anonymisierte Uebergabeunterlagen.

Erlaubt sind nur organisatorische, didaktische und materialbezogene Informationen ohne personenbezogene Daten.

Nicht erfassen: Schuelernamen, Schuelerbeobachtungen, Noten, Diagnosen, Krankheitsdaten, Elternkommunikation, sensible Einzelfaelle oder Leistungsaufschreibungen.
MD

echo "Vault initialized."

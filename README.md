# ai-teacher-stack

**Ein freies, lokales Arbeitstool für Lehrkräfte.**

`ai-teacher-stack` soll Lehrkräfte bei der täglichen Unterrichtsvorbereitung entlasten: Lehrplanbezug herstellen, Materialien überarbeiten, differenzierte Arbeitsaufträge erstellen, digitale Tafelbilder vorbereiten, Vertretungen strukturieren und bewährte Unterrichtsideen wieder auffindbar machen.

Es ist ausdrücklich **nicht** als weitere kommerzielle App, Plattform oder Abo-Lösung gedacht. Der Stack orientiert sich an offenen, nachvollziehbaren Arbeitsweisen: lokale Dateien, klare Ordnerstruktur, transparente Prompts, exportierbare Materialien und möglichst wenig Abhängigkeit von einzelnen Anbietern.

> Ziel ist ein zentrales Lehrerarbeitswerkzeug, das vorhandene Materialien respektiert, Unterrichtsideen weiterentwickelt und Zusammenarbeit erleichtert — ohne Lehrkräfte in eine geschlossene kommerzielle Plattform zu zwingen.

## Wofür ist das gedacht?

Viele Lehrkräfte arbeiten mit über Jahre gewachsenen Materialien: alte Arbeitsblätter, Word-Dateien, Tafelbilder, Proben, Notizen, Jahrgangsstufenordner, Messenger-Gruppen und Cloud-Ablagen. Das funktioniert im Alltag, wird aber schnell unübersichtlich.

`ai-teacher-stack` setzt genau dort an:

- **Unterricht soll Spaß machen**: Aus einem Thema entstehen motivierende Einstiege, Aufgabenideen, Tafelimpulse und kindgerechte Materialien.
- **Unterricht soll individuell sein**: Ein Lernziel kann in mehrere Niveaustufen, Hilfen, Zusatzaufgaben oder offene Arbeitsformen übersetzt werden.
- **Lehrplaninhalte sollen sichtbar vermittelt werden**: Materialien werden mit Kompetenzen, Themen und Jahrgangsstufen verknüpft.
- **Altes Material soll nicht weggeworfen werden**: Bewährte Arbeitsblätter können aktualisiert, vereinfacht, differenziert und neu formatiert werden.
- **Digitale Tafeln brauchen passende Inhalte**: Der Stack soll helfen, aus Unterrichtsideen schnell tafelgeeignete Impulse, Abläufe und Sicherungen zu erzeugen.
- **Routineaufgaben sollen weniger belasten**: Verlaufspläne, Lösungen, Vertretungshinweise, Materiallisten und einfache Dokumente sollen schneller entstehen.
- **Zusammenarbeit soll leichter werden**: Lehrkräfte einer Jahrgangsstufe können Materialien strukturierter teilen, überarbeiten und wiederverwenden.

## Was ist der Unterschied zu einer kommerziellen Bildungs-App?

`ai-teacher-stack` ist als **lokal-first Werkzeugkasten** gedacht, nicht als zentraler kommerzieller Dienst.

| Kommerzielle App | ai-teacher-stack |
|---|---|
| geschlossenes Produkt | nachvollziehbarer Projektordner |
| häufig Account-, Abo- oder Plattformbindung | lokale Nutzung mit Docker und Dateien |
| Daten und Workflows liegen oft beim Anbieter | Vault, Exporte und Materialien bleiben lokal |
| Funktionsumfang vom Anbieter vorgegeben | anpassbare Prompts, Vorlagen und Tools |
| schwer in eigene Arbeitsweise integrierbar | orientiert an bestehenden Ordnern, DOCX, Markdown, BYCS/Drive-Export |

Das Projekt ist bewusst offen lesbar und anpassbar. Gleichzeitig ist die **kommerzielle Nutzung untersagt**. Siehe [Lizenz](#lizenz-und-nutzung).

## Grundprinzipien

1. **Lehrkraft bleibt verantwortlich**  
   KI macht Vorschläge, erstellt Entwürfe und hilft beim Strukturieren. Die fachliche und pädagogische Entscheidung bleibt bei der Lehrkraft.

2. **Lokal vor Cloud**  
   Materialien, Vault und Exporte sollen standardmäßig auf dem eigenen Rechner liegen. Cloud-Systeme wie BYCS Drive oder OneDrive sind Exportziele, nicht der Kern des Systems.

3. **Material statt Schülerdaten**  
   Der Stack ist in v1 ein Werkzeug für Unterrichtsmaterialien, Planung und Reflexion. Er ist kein Notenbuch, keine Schülerakte und kein Diagnosesystem.

4. **Vorhandenes Material ist wertvoll**  
   Ziel ist nicht, alles neu zu generieren. Ziel ist, vorhandene Materialien besser zu finden, zu modernisieren, zu differenzieren und lehrplankonform weiterzuentwickeln.

5. **Offen, aber nicht kommerziell**  
   Der Code soll einsehbar, lernbar und für nicht-kommerzielle Bildungszwecke anpassbar sein. Eine kommerzielle Verwertung ist nicht erlaubt.

## Typische Anwendungsfälle

### 1. Unterricht planen

```text
Thema: Orientierung mit Karten, Klasse 3
Ziel: 45-Minuten-Stunde mit Einstieg, Partnerarbeit, Sicherung und Lehrplanbezug
Ausgabe: Verlaufsplan, Arbeitsblatt, Lösung, Tafelbild-Idee
```

### 2. Material differenzieren

```text
Aus einem Arbeitsblatt entstehen:
- Basisversion
- Version mit Hilfekarten
- Zusatzaufgaben
- Lösung
- kurze Erklärung in einfacher Sprache
```

### 3. Digitale Tafel vorbereiten

```text
Aus einer Unterrichtsidee entstehen:
- Einstieg mit Bild-/Denkimpuls
- Ablauf für die Stunde
- Sicherungsfolie
- Reflexionsfrage
```

### 4. Vertretung vorbereiten

```text
Aus vorhandener Planung entstehen:
- Thema und Lernziel
- benötigte Materialien
- Ablauf in 5 Schritten
- Arbeitsauftrag für die Klasse
- Lösung oder Erwartungshorizont
```

### 5. Jahrgangsstufenarbeit strukturieren

```text
Gemeinsame Materialien werden nicht mehr nur in Chats verteilt,
sondern in einem geordneten Vault abgelegt, beschrieben und wiederverwendbar gemacht.
```

## Datenschutzgrenze für v1

Bitte keine sensiblen personenbezogenen Daten in den Stack legen.

**Geeignet:**

- eigene Unterrichtsmaterialien
- selbst erstellte Arbeitsblätter
- allgemeine Unterrichtsnotizen ohne Namen
- Lehrplanbezüge
- Reflexionen ohne personenbezogene Details
- leere oder beispielhafte Vorlagen

**Nicht geeignet:**

- Schülernamen
- Notenlisten
- Förderdiagnosen
- Elternkommunikation mit Klarnamen
- sensible Einzelfallbeschreibungen
- private BYCS-/OneDrive-Dateien im öffentlichen Repository
- kommerzielle Schulbuchinhalte ohne Nutzungsrecht

## Installation: lokale Nutzung

### Voraussetzungen

- Git
- Docker Desktop oder Docker Engine mit Docker Compose
- optional: Ollama für lokale KI-Modelle
- optional: GitHub CLI `gh`, wenn du ein eigenes GitHub-Repo bootstrappen willst

### Repository klonen

```bash
git clone https://github.com/cabrauck/ai-teacher-stack.git
cd ai-teacher-stack
```

### Umgebung anlegen

```bash
cp .env.example .env
```

### Stack starten

```bash
docker compose up --build
```

### API prüfen

```bash
curl http://localhost:8010/health
curl "http://localhost:8010/curriculum/search?q=lesen"
```

### Beispiel: Unterrichtsidee erzeugen

```bash
curl -X POST http://localhost:8010/lessons \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "HSU",
    "grade_band": "3/4",
    "topic": "Orientierung mit Karten",
    "duration_minutes": 45
  }'
```

## Bootstrap: eigenes öffentliches Repo aus dem Scaffold erstellen

Das Repository enthält ein Bootstrap-Skript für ein eigenes öffentliches GitHub-Repo.

```bash
./scripts/bootstrap-github-public.sh cabrauck ai-teacher-stack
```

Allgemeines Muster:

```bash
./scripts/bootstrap-github-public.sh <github-owner> <repo-name>
```

Das Skript prüft `git` und `gh`, initialisiert bei Bedarf ein Git-Repository, erstellt einen ersten Commit und legt das GitHub-Repository öffentlich an oder verbindet ein bereits bestehendes Repository.

Manuell geht es auch so:

```bash
git init
git add .
git commit -m "Initial ai-teacher-stack scaffold"
gh repo create <github-owner>/<repo-name> --public --source=. --remote=origin --push
```

## Ordner, die für Lehrkräfte wichtig sind

```text
vault/                 eigener Arbeits- und Materialbereich
exports/               erzeugte Dokumente und Exportpakete
data/curriculum/       strukturierte Lehrplan-/Beispieldaten
prompts/               wiederverwendbare Arbeitsanweisungen
templates/             Dokumentvorlagen, z. B. für DOCX
```

Der Entwicklungsbereich, Agenten-Workflow und technische Details sind ausgelagert: siehe [CONTRIBUTING.md](CONTRIBUTING.md).

## Lizenz und Nutzung

Dieses Projekt verwendet die **PolyForm Noncommercial License 1.0.0**.

Das bedeutet:

- nicht-kommerzielle Nutzung, Anpassung und Weitergabe sind gewollt,
- Einsatz im persönlichen, schulischen oder gemeinnützigen Bildungskontext ist Ziel des Projekts,
- kommerzielle Nutzung, kommerzielle Weiterverwertung oder Einbau in kommerzielle Produkte ist nicht erlaubt,
- die Lizenz ist bewusst nicht als OSI-Open-Source-Lizenz einzuordnen, weil kommerzielle Nutzung ausgeschlossen wird.

Namensnennung ist erwünscht, wenn du das Projekt veröffentlichst, in Fortbildungen nutzt oder daraus abgeleitete Materialien teilst. Siehe `NOTICE.md` und `CITATION.cff`.

## Kurz gesagt

`ai-teacher-stack` soll ein freies, zentrales und lokales Arbeitstool für Lehrkräfte werden: offen nachvollziehbar, nicht-kommerziell, lehrplannah, materialorientiert und darauf ausgelegt, echten Schulalltag einfacher zu machen.

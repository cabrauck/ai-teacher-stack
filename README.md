# ai-teacher-stack

<p align="center">
  <a href="#lizenz-und-nutzung"><img alt="License: PolyForm Noncommercial" src="https://img.shields.io/badge/License-PolyForm%20NC-555555?style=flat-square"></a>
  <a href="services/teacher_tools/pyproject.toml"><img alt="Python 3.12+" src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white"></a>
  <a href="docker-compose.yml"><img alt="Docker Compose" src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white"></a>
  <a href="#typische-anwendungsfalle"><img alt="Claude-OS Memory" src="https://img.shields.io/badge/Claude--OS-Memory-111827?style=flat-square"></a>
  <a href="#ordner-die-fur-lehrkrafte-wichtig-sind"><img alt="Obsidian Vault" src="https://img.shields.io/badge/Obsidian-Vault-7C3AED?style=flat-square&logo=obsidian&logoColor=white"></a>
  <a href="#datenschutzgrenze-fur-v1"><img alt="Datenschutz: keine Schuelerdaten" src="https://img.shields.io/badge/Datenschutz-keine%20Schuelerdaten-0F766E?style=flat-square"></a>
</p>

<p align="center">
  <a href="#wofur-ist-das-gedacht"><img alt="Ueberblick" src="https://img.shields.io/badge/Ueberblick-fuer%20Lehrkraefte-111827?style=flat-square"></a>
  <a href="#typische-anwendungsfalle"><img alt="Anwendungsfaelle" src="https://img.shields.io/badge/Anwendungsfaelle-Unterricht%20planen-2563EB?style=flat-square"></a>
  <a href="CONTRIBUTING.md"><img alt="Mitwirken" src="https://img.shields.io/badge/Mitwirken-Contributing-7C3AED?style=flat-square"></a>
  <a href="https://github.com/sponsors/cabrauck"><img alt="GitHub Sponsors" src="https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-EA4AAA?style=flat-square&logo=githubsponsors&logoColor=white"></a>
</p>

**Nutzerinfo fur Lehrkrafte und Interessierte.**

Diese `README.md` ist bewusst als **Nutzerinfo und Projektuberblick** geschrieben.
Wenn du am Stack mitarbeiten, entwickeln oder Releases mit vorbereiten willst,
lies bitte zuerst [CONTRIBUTING.md](CONTRIBUTING.md). Dort stehen der
Entwicklungsablauf, alle Checks, die Release-Grenzen und die Regeln fur
Beitrage.

`ai-teacher-stack` ist ein lokal-first Arbeitsbereich fur Lehrkrafte fur
lehrplangebundene Unterrichtsplanung, Materialuberarbeitung,
Obsidian-basiertes Langzeitwissen, Claude-OS als lokale Memory-Laufzeit und
optionale lokale Inferenz.

`ai-teacher-stack` soll Lehrkrafte bei der taglichen Unterrichtsvorbereitung
entlasten: Lehrplanbezug herstellen, Materialien uberarbeiten, differenzierte
Arbeitsauftrage erstellen, digitale Tafelbilder vorbereiten, Vertretungen
strukturieren und bewahrte Unterrichtsideen wieder auffindbar machen.

Es ist ausdrucklich **nicht** als weitere kommerzielle App, Plattform oder
Abo-Losung gedacht. Der Stack orientiert sich an offenen, nachvollziehbaren
Arbeitsweisen: lokale Dateien, klare Ordnerstruktur, transparente Prompts,
exportierbare Materialien und moglichst wenig Abhangigkeit von einzelnen
Anbietern.

> Ziel ist ein zentrales Lehrerarbeitswerkzeug, das vorhandene Materialien
> respektiert, Unterrichtsideen weiterentwickelt und Zusammenarbeit erleichtert,
> ohne Lehrkrafte in eine geschlossene kommerzielle Plattform zu zwingen.

## Wofur ist das gedacht?

Viele Lehrkrafte arbeiten mit uber Jahre gewachsenen Materialien: alte
Arbeitsblatter, Word-Dateien, Tafelbilder, Proben, Notizen,
Jahrgangsstufenordner, Messenger-Gruppen und Cloud-Ablagen. Das funktioniert
im Alltag, wird aber schnell unubersichtlich.

- Lokalbetrieb ist der Standard.
- Obsidian-Vault und erzeugte Dokumente bleiben auf dem eigenen Rechner.
- LibreChat ist die Lehreroberflaeche fuer v1.
- Claude-OS ist der zentrale lokale Memory-Dienst.
- LibreChat ist eng mit Claude-OS und den lokalen teacher-tools verbunden.
- OpenRouter ist der Standardweg fuer LLM-Zugriff; BYOK fuer ausgewaehlte
  Frontier-Anbieter bleibt lokal moeglich.
- Der Einstieg beginnt mit Lehrkraft-Ablaufen, nicht mit
  Schulerdaten-Ablaufen.
- Unterrichtsplanung wird an strukturierte Lehrplandaten angebunden.
- Materialien sollen wiederverwendbar als Markdown, DOCX und spater PDF
  entstehen.
- Lokales Ollama wird unterstutzt, wenn die Hardware es zulasst.
- BYCS Drive, OneDrive oder andere Schul-Clouds bleiben Exportziele, nicht die
  eigentliche Laufzeitbasis.

`ai-teacher-stack` setzt genau dort an:

- **Unterricht soll SpaB machen**: Aus einem Thema entstehen motivierende
  Einstiege, Aufgabenideen, Tafelimpulse und kindgerechte Materialien.
- **Unterricht soll individuell sein**: Ein Lernziel kann in mehrere
  Niveaustufen, Hilfen, Zusatzaufgaben oder offene Arbeitsformen ubersetzt
  werden.
- **Lehrplaninhalte sollen sichtbar vermittelt werden**: Materialien werden mit
  Kompetenzen, Themen und Jahrgangsstufen verknupft.
- **Altes Material soll nicht weggeworfen werden**: Bewahrte Arbeitsblatter
  konnen aktualisiert, vereinfacht, differenziert und neu formatiert werden.
- **Digitale Tafeln brauchen passende Inhalte**: Der Stack soll helfen, aus
  Unterrichtsideen schnell tafelgeeignete Impulse, Ablaufe und Sicherungen zu
  erzeugen.
- **Routineaufgaben sollen weniger belasten**: Verlaufsplane, Losungen,
  Vertretungshinweise, Materiallisten und einfache Dokumente sollen schneller
  entstehen.
- **Zusammenarbeit soll leichter werden**: Lehrkrafte einer Jahrgangsstufe
  konnen Materialien strukturierter teilen, uberarbeiten und wiederverwenden.

## Was ist der Unterschied zu einer kommerziellen Bildungs-App?

`ai-teacher-stack` ist als **lokal-first Werkzeugkasten** gedacht, nicht als
zentraler kommerzieller Dienst.

| Kommerzielle App | ai-teacher-stack |
|---|---|
| geschlossenes Produkt | nachvollziehbarer Projektordner |
| haufig Account-, Abo- oder Plattformbindung | lokale Nutzung mit Docker und Dateien |
| Daten und Arbeitsablaufe liegen oft beim Anbieter | Vault, Exporte und Materialien bleiben lokal |
| Funktionsumfang vom Anbieter vorgegeben | anpassbare Prompts, Vorlagen und Tools |
| schwer in eigene Arbeitsweise integrierbar | orientiert an bestehenden Ordnern, DOCX, Markdown, BYCS/Drive-Export |

Das Projekt ist bewusst offen lesbar und anpassbar. Gleichzeitig ist die
**kommerzielle Nutzung untersagt**. Siehe [Lizenz](#lizenz-und-nutzung).

## Grundprinzipien

1. **Lehrkraft bleibt verantwortlich**  
   KI macht Vorschlage, erstellt Entwurfe und hilft beim Strukturieren. Die
   fachliche und padagogische Entscheidung bleibt bei der Lehrkraft.

2. **Lokal vor Cloud**  
   Materialien, Vault und Exporte sollen standardmaBig auf dem eigenen Rechner
   liegen. Cloud-Systeme wie BYCS Drive oder OneDrive sind Exportziele, nicht
   der Kern des Systems.

3. **Material statt Schulerdaten**  
   Der Stack ist in v1 ein Werkzeug fur Unterrichtsmaterialien, Planung und
   Reflexion. Er ist kein Notenbuch, keine Schulerakte und kein Diagnosesystem.

4. **Vorhandenes Material ist wertvoll**  
   Ziel ist nicht, alles neu zu generieren. Ziel ist, vorhandene Materialien
   besser zu finden, zu modernisieren, zu differenzieren und
   lehrplankonform weiterzuentwickeln.

5. **Offen, aber nicht kommerziell**  
   Der Code soll einsehbar, lernbar und fur nicht-kommerzielle Bildungszwecke
   anpassbar sein. Eine kommerzielle Verwertung ist nicht erlaubt.

## Typische Anwendungsfalle

### 1. Unterricht planen

```text
Thema: Orientierung mit Karten, Klasse 3
Ziel: 45-Minuten-Stunde mit Einstieg, Partnerarbeit, Sicherung und Lehrplanbezug
Ausgabe: Verlaufsplan, Arbeitsblatt, Losung, Tafelbild-Idee
```

### 2. Material differenzieren

```text
Aus einem Arbeitsblatt entstehen:
- Basisversion
- Version mit Hilfekarten
- Zusatzaufgaben
- Losung
- kurze Erklarung in einfacher Sprache
```

### 3. Digitale Tafel vorbereiten

```text
Aus einer Unterrichtsidee entstehen:
- Einstieg mit Bild-/Denkimpuls
- Ablauf fur die Stunde
- Sicherungsfolie
- Reflexionsfrage
```

### 4. Vertretung vorbereiten

```text
Aus vorhandener Planung entstehen:
- Thema und Lernziel
- benotigte Materialien
- Ablauf in 5 Schritten
- Arbeitsauftrag fur die Klasse
- Losung oder Erwartungshorizont
```

### 5. Jahrgangsstufenarbeit strukturieren

```text
Gemeinsame Materialien werden nicht mehr nur in Chats verteilt,
sondern in einem geordneten Vault abgelegt, beschrieben und wiederverwendbar gemacht.
```

## Datenschutzgrenze fur v1

Bitte keine sensiblen personenbezogenen Daten in den Stack legen.

**Geeignet:**

- eigene Unterrichtsmaterialien
- selbst erstellte Arbeitsblatter
- allgemeine Unterrichtsnotizen ohne Namen
- Lehrplanbezuge
- Reflexionen ohne personenbezogene Details
- leere oder beispielhafte Vorlagen

**Nicht geeignet:**

- Schulernamen
- Notenlisten
- Forderdiagnosen
- Elternkommunikation mit Klarnamen
- sensible Einzelfallbeschreibungen
- private BYCS-/OneDrive-Dateien im offentlichen Repository
- kommerzielle Schulbuchinhalte ohne Nutzungsrecht

## Ordner, die fur Lehrkrafte wichtig sind

```text
vault/                 eigener Arbeits- und Materialbereich
exports/               erzeugte Dokumente und Exportpakete
data/curriculum/       strukturierte Lehrplan-/Beispieldaten
prompts/               wiederverwendbare Arbeitsanweisungen
templates/             Dokumentvorlagen, z. B. fur DOCX
```

Das Standard-Scaffold ist fur ein offentliches Repository geeignet, weil es nur
beispielhafte curriculare Daten und leere Platzhalter im Vault enthalt.
Echte Schulerdaten, private BYCS-/OneDrive-Dateien, Tokens, Exporte,
Claude-OS-Datenbanken, Logs, Uploads oder nicht-offentliche Unterrichtsmaterialien
sollten nicht eingecheckt werden.

## Unterstutzung

Wenn dir das Projekt hilft und du seine Weiterentwicklung fordern willst,
freue ich mich uber freiwillige finanzielle Unterstutzung. `ai-teacher-stack`
ist ein Freizeitprojekt, das in der freien Zeit entsteht und gepflegt wird.

Finanzielle Unterstutzung ist uber GitHub Sponsors vorgesehen:
[Sponsor werden](https://github.com/sponsors/cabrauck)

## Mitwirken

Die `README` bleibt bewusst nutzerorientiert. Entwicklungsablauf,
Agenten-Regeln, Checklisten und Release-Grenzen stehen in
[CONTRIBUTING.md](CONTRIBUTING.md).

## Lizenz und Nutzung

Dieses Projekt verwendet die **PolyForm Noncommercial License 1.0.0**.

Das bedeutet:

- nicht-kommerzielle Nutzung, Anpassung und Weitergabe sind gewollt,
- Einsatz im personlichen, schulischen oder gemeinnutzigen Bildungskontext ist
  Ziel des Projekts,
- kommerzielle Nutzung, kommerzielle Weiterverwertung oder Einbau in
  kommerzielle Produkte ist nicht erlaubt,
- die Lizenz ist bewusst nicht als OSI-Open-Source-Lizenz einzuordnen, weil
  kommerzielle Nutzung ausgeschlossen wird.

Namensnennung ist erwunscht, wenn du das Projekt veroffentlichst, in
Fortbildungen nutzt oder daraus abgeleitete Materialien teilst. Siehe
`NOTICE.md` und `CITATION.cff`.

## Kurz gesagt

`ai-teacher-stack` soll ein freies, zentrales und lokales Arbeitstool fur
Lehrkrafte werden: offen nachvollziehbar, nicht-kommerziell, lehrplannah,
materialorientiert und darauf ausgelegt, echten Schulalltag einfacher zu
machen.

from __future__ import annotations

from datetime import date
from pathlib import Path

from teacher_tools.documents import export_schriftwesen_docx
from teacher_tools.schriftwesen import (
    ClassRoutines,
    DailyTopHour,
    DailyTopRequest,
    HandoverSummaryRequest,
    RunningUnit,
    SubstitutionPlanRequest,
    WeeklyPlanRequest,
    generate_daily_top,
    generate_handover_summary,
    generate_substitution_plan,
    generate_weekly_plan,
    schriftwesen_to_markdown,
)


def test_generate_weekly_plan_is_privacy_safe_and_markdown_ready():
    plan = generate_weekly_plan(
        WeeklyPlanRequest(
            woche="2026-KW21",
            klasse="Klasse 3a",
            themen=["Kartenarbeit", "Lesestrategien"],
        )
    )

    assert plan.typ == "wochenplan"
    assert plan.personenbezogene_daten is False
    assert plan.tage["montag"].themen == ["Kartenarbeit"]
    assert plan.tage["dienstag"].themen == ["Lesestrategien"]

    markdown = schriftwesen_to_markdown(plan)
    assert "personenbezogene_daten: false" in markdown
    assert "Automatisch erzeugter Entwurf" in markdown
    assert "## Vertretungsrelevant" in markdown


def test_generate_daily_top_uses_supplied_hours():
    plan = generate_daily_top(
        DailyTopRequest(
            datum=date(2026, 5, 18),
            klasse="Klasse 3a",
            tagesziel="Karten sicher lesen.",
            stunden=[
                DailyTopHour(
                    zeit="08:00-08:45",
                    fach="HSU",
                    ziel="Kartensymbole nutzen.",
                    ablauf="Einstieg, Partnerarbeit, Sicherung.",
                    material=["Karten", "Arbeitsblatt"],
                    sozialform="Partnerarbeit",
                    vertretungshinweis="Aufgabe kann ohne Zusatzwissen bearbeitet werden.",
                )
            ],
        )
    )

    assert plan.typ == "tagesorganisationsplan"
    assert plan.stunden[0].fach == "HSU"
    assert "Kartensymbole" in schriftwesen_to_markdown(plan)


def test_generate_substitution_plan_has_default_safe_tasks():
    plan = generate_substitution_plan(
        SubstitutionPlanRequest(
            datum=date(2026, 5, 19),
            klasse="Klasse 3a",
            material_bereitgelegt=["Wochenplan im Klassenraum"],
        )
    )

    assert plan.typ == "vertretungsplan"
    assert "Wochenplanarbeit fortsetzen." in plan.sichere_aufgaben
    assert plan.personenbezogene_daten is False


def test_generate_handover_summary_is_anonymized():
    summary = generate_handover_summary(
        HandoverSummaryRequest(
            klasse="Klasse 3a",
            zeitraum="Mai 2026",
            aktueller_stand={"deutsch": "Lesestrategien eingefuehrt"},
            laufende_reihen=[
                RunningUnit(
                    thema="Kartenarbeit",
                    begonnen_am=date(2026, 5, 4),
                    letzter_stand="Legende und Symbole gesichert",
                    naechster_schritt="Wege auf Karten beschreiben",
                    materialpfad="vault/Materialien/HSU/Kartenarbeit",
                )
            ],
            routinen=ClassRoutines(tagesbeginn="Morgenritual und Tagesvorschau"),
        )
    )

    assert summary.typ == "klassenuebergabe_anonym"
    assert summary.personenbezogene_daten is False
    markdown = schriftwesen_to_markdown(summary)
    assert "Klassenuebergabe Anonymisiert" in markdown
    assert "Morgenritual" in markdown


def test_export_schriftwesen_docx(tmp_path: Path):
    plan = generate_weekly_plan(
        WeeklyPlanRequest(woche="2026-KW21", klasse="Klasse 3a", themen=["Kartenarbeit"])
    )

    out = export_schriftwesen_docx(plan, tmp_path)

    assert out.exists()
    assert out.parent == tmp_path / "schriftwesen"
    assert out.name.endswith(".docx")


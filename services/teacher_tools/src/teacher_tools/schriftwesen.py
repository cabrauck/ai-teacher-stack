from __future__ import annotations

import re
from datetime import date as dt_date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from teacher_tools.privacy import PrivacyValidationResult, assert_no_personal_data, validate_privacy

TEACHER_REVIEW_NOTE = (
    "Automatisch erzeugter Entwurf. Vor Ablage, Export oder Einsatz fachlich, "
    "organisatorisch und datenschutzbezogen prüfen."
)
WEEKDAYS = ("montag", "dienstag", "mittwoch", "donnerstag", "freitag")


class SchriftwesenBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CurriculumLink(SchriftwesenBaseModel):
    fach: str
    kompetenzbereich: str = ""
    ziel: str
    quelle: str | None = None

    @field_validator("fach", "ziel")
    @classmethod
    def require_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value must not be empty")
        return cleaned


class WeeklyFocus(SchriftwesenBaseModel):
    deutsch: list[str] = Field(default_factory=list)
    mathematik: list[str] = Field(default_factory=list)
    hsu: list[str] = Field(default_factory=list)
    sonstiges: list[str] = Field(default_factory=list)


class WeeklyPlanDay(SchriftwesenBaseModel):
    themen: list[str] = Field(default_factory=list)
    material: list[str] = Field(default_factory=list)
    hausaufgaben: list[str] = Field(default_factory=list)
    offene_punkte: list[str] = Field(default_factory=list)


class WeeklyPlanRequest(SchriftwesenBaseModel):
    woche: str
    klasse: str
    themen: list[str] = Field(default_factory=list)
    schwerpunkte: WeeklyFocus = Field(default_factory=WeeklyFocus)
    lehrplanbezug: list[CurriculumLink] = Field(default_factory=list)
    personenbezogene_daten: Literal[False] = False
    status: str = "entwurf"


class WeeklyPlan(WeeklyPlanRequest):
    typ: Literal["wochenplan"] = "wochenplan"
    tage: dict[str, WeeklyPlanDay]
    vertretungsrelevant: list[str]
    teacher_review_note: str = TEACHER_REVIEW_NOTE


class DailyOrganization(SchriftwesenBaseModel):
    gruppen: str = "nur anonym, z. B. Gruppe A/B"
    raumwechsel: list[str] = Field(default_factory=list)
    externe_termine: list[str] = Field(default_factory=list)


class DailyTopHour(SchriftwesenBaseModel):
    zeit: str = ""
    fach: str = ""
    ziel: str = ""
    ablauf: str = ""
    material: list[str] = Field(default_factory=list)
    sozialform: str = ""
    tafelbild_datei: str | None = None
    arbeitsblatt_datei: str | None = None
    hausaufgabe: str = ""
    vertretungshinweis: str = ""


class DailyTopRequest(SchriftwesenBaseModel):
    datum: dt_date
    klasse: str
    tagesziel: str = ""
    material_bereitgelegt: list[str] = Field(default_factory=list)
    rituale: list[str] = Field(default_factory=list)
    besondere_organisation: DailyOrganization = Field(default_factory=DailyOrganization)
    stunden: list[DailyTopHour] = Field(default_factory=list)
    offene_punkte_fuer_morgen: list[str] = Field(default_factory=list)
    personenbezogene_daten: Literal[False] = False
    status: str = "entwurf"


class DailyTop(DailyTopRequest):
    typ: Literal["tagesorganisationsplan"] = "tagesorganisationsplan"
    teacher_review_note: str = TEACHER_REVIEW_NOTE


class SubstitutionPlanRequest(SchriftwesenBaseModel):
    datum: dt_date
    klasse: str
    zeitraum: str = "ein Tag"
    tagesziel: str = ""
    material_bereitgelegt: list[str] = Field(default_factory=list)
    rituale: list[str] = Field(default_factory=list)
    sichere_aufgaben: list[str] = Field(default_factory=list)
    auslassbar: list[str] = Field(default_factory=list)
    vertretungshinweise: list[str] = Field(default_factory=list)
    personenbezogene_daten: Literal[False] = False
    status: str = "entwurf"


class SubstitutionPlan(SubstitutionPlanRequest):
    typ: Literal["vertretungsplan"] = "vertretungsplan"
    teacher_review_note: str = TEACHER_REVIEW_NOTE


class RunningUnit(SchriftwesenBaseModel):
    thema: str
    begonnen_am: dt_date | None = None
    letzter_stand: str = ""
    naechster_schritt: str = ""
    materialpfad: str = ""


class ClassRoutines(SchriftwesenBaseModel):
    tagesbeginn: str = ""
    wochenplanarbeit: str = ""
    hausaufgaben: str = ""
    materialorganisation: str = ""
    klassenregeln_allgemein: str = ""


class HandoverSummaryRequest(SchriftwesenBaseModel):
    klasse: str
    zeitraum: str
    aktueller_stand: dict[str, str] = Field(default_factory=dict)
    laufende_reihen: list[RunningUnit] = Field(default_factory=list)
    routinen: ClassRoutines = Field(default_factory=ClassRoutines)
    wichtig_fuer_vertretung: list[str] = Field(default_factory=list)
    offene_to_dos: list[str] = Field(default_factory=list)
    personenbezogene_daten: Literal[False] = False
    status: str = "entwurf"


class HandoverSummary(HandoverSummaryRequest):
    typ: Literal["klassenuebergabe_anonym"] = "klassenuebergabe_anonym"
    teacher_review_note: str = TEACHER_REVIEW_NOTE


SchriftwesenDocument = WeeklyPlan | DailyTop | SubstitutionPlan | HandoverSummary


def _default_topic(index: int, topics: list[str]) -> str:
    if topics:
        return topics[index % len(topics)]
    return "Wochenplanarbeit, Uebung und Sicherung nach Lehrplanbezug"


def _default_material(topic: str) -> list[str]:
    return [
        "Wochenplan oder Aufgabenuebersicht",
        f"Material zu: {topic}",
        "Loesungs- oder Kontrollmoeglichkeit fuer die Lehrkraft",
    ]


def generate_weekly_plan(request: WeeklyPlanRequest) -> WeeklyPlan:
    assert_no_personal_data(request, context="Schriftwesen weekly plan request")
    tage = {
        day: WeeklyPlanDay(
            themen=[topic := _default_topic(index, request.themen)],
            material=_default_material(topic),
            hausaufgaben=[],
            offene_punkte=[],
        )
        for index, day in enumerate(WEEKDAYS)
    }
    plan = WeeklyPlan(
        **request.model_dump(),
        tage=tage,
        vertretungsrelevant=[
            "Welche Materialien liegen bereit?",
            "Welche Aufgaben koennen ohne Vorwissen bearbeitet werden?",
            "Was darf ausgelassen werden?",
        ],
    )
    assert_no_personal_data(plan, context="Schriftwesen weekly plan")
    return plan


def generate_daily_top(request: DailyTopRequest) -> DailyTop:
    assert_no_personal_data(request, context="Schriftwesen daily TOP request")
    stunden = request.stunden or [
        DailyTopHour(
            zeit="nach Stundenplan",
            fach="fachuebergreifend",
            ziel=request.tagesziel or "Tagesstruktur klaeren und Unterricht fortsetzen.",
            ablauf="Ablauf durch die Lehrkraft oder Vertretung anhand der Materialien ergaenzen.",
            material=request.material_bereitgelegt,
            sozialform="Einzel-, Partner- oder Gruppenarbeit nach Situation",
            vertretungshinweis="Kann ohne personenbezogene Zusatzinformationen genutzt werden.",
        )
    ]
    plan = DailyTop(**request.model_dump(exclude={"stunden"}), stunden=stunden)
    assert_no_personal_data(plan, context="Schriftwesen daily TOP")
    return plan


def generate_substitution_plan(request: SubstitutionPlanRequest) -> SubstitutionPlan:
    assert_no_personal_data(request, context="Schriftwesen substitution request")
    sichere_aufgaben = request.sichere_aufgaben or [
        "Wochenplanarbeit fortsetzen.",
        "Wiederholungs- oder Sicherungsaufgaben bearbeiten.",
    ]
    vertretungshinweise = request.vertretungshinweise or [
        "Nur organisatorische Hinweise nutzen.",
        "Keine personenbezogenen Beobachtungen oder Leistungsdaten erfassen.",
    ]
    plan = SubstitutionPlan(
        **request.model_dump(exclude={"sichere_aufgaben", "vertretungshinweise"}),
        sichere_aufgaben=sichere_aufgaben,
        vertretungshinweise=vertretungshinweise,
    )
    assert_no_personal_data(plan, context="Schriftwesen substitution plan")
    return plan


def generate_handover_summary(request: HandoverSummaryRequest) -> HandoverSummary:
    assert_no_personal_data(request, context="Schriftwesen handover request")
    wichtig = request.wichtig_fuer_vertretung or [
        "keine personenbezogenen Hinweise",
        "nur organisatorische Ablaeufe",
        "Materialpfade und offene Aufgaben pruefen",
    ]
    summary = HandoverSummary(
        **request.model_dump(exclude={"wichtig_fuer_vertretung"}),
        wichtig_fuer_vertretung=wichtig,
    )
    assert_no_personal_data(summary, context="Schriftwesen handover summary")
    return summary


def _bullet(items: list[str]) -> str:
    if not items:
        return "- "
    return "\n".join(f"- {item}" for item in items)


def _curriculum_links(links: list[CurriculumLink]) -> str:
    if not links:
        return "- Kein Lehrplanbezug hinterlegt. Manuell ergaenzen."
    return "\n".join(
        f"- {link.fach} / {link.kompetenzbereich}: {link.ziel}"
        + (f" ({link.quelle})" if link.quelle else "")
        for link in links
    )


def _frontmatter(document: SchriftwesenDocument) -> str:
    return "\n".join(
        [
            "---",
            f"typ: {document.typ}",
            f"klasse: {document.klasse}",
            "personenbezogene_daten: false",
            f"status: {document.status}",
            "---",
            "",
        ]
    )


def _weekly_plan_to_markdown(plan: WeeklyPlan) -> str:
    day_sections = []
    for day in WEEKDAYS:
        details = plan.tage[day]
        day_sections.append(
            "\n".join(
                [
                    f"### {day.title()}",
                    "",
                    "**Themen**",
                    _bullet(details.themen),
                    "",
                    "**Material**",
                    _bullet(details.material),
                    "",
                    "**Hausaufgaben**",
                    _bullet(details.hausaufgaben),
                    "",
                    "**Offene Punkte**",
                    _bullet(details.offene_punkte),
                ]
            )
        )
    return (
        _frontmatter(plan)
        + f"# Wochenplan {plan.woche}\n\n"
        + f"- Klasse: {plan.klasse}\n"
        + f"- Status: {plan.status}\n\n"
        + "## Lehrplanbezug\n\n"
        + _curriculum_links(plan.lehrplanbezug)
        + "\n\n## Tage\n\n"
        + "\n\n".join(day_sections)
        + "\n\n## Vertretungsrelevant\n\n"
        + _bullet(plan.vertretungsrelevant)
        + "\n\n## Hinweis\n\n"
        + plan.teacher_review_note
        + "\n"
    )


def _daily_top_to_markdown(plan: DailyTop) -> str:
    hours = []
    for hour in plan.stunden:
        hours.append(
            "\n".join(
                [
                    f"### {hour.zeit or 'Stunde'} - {hour.fach or 'fachuebergreifend'}",
                    "",
                    f"- Ziel: {hour.ziel}",
                    f"- Ablauf: {hour.ablauf}",
                    f"- Sozialform: {hour.sozialform}",
                    f"- Material: {', '.join(hour.material) if hour.material else ''}",
                    f"- Tafelbild: {hour.tafelbild_datei or ''}",
                    f"- Arbeitsblatt: {hour.arbeitsblatt_datei or ''}",
                    f"- Hausaufgabe: {hour.hausaufgabe}",
                    f"- Vertretungshinweis: {hour.vertretungshinweis}",
                ]
            )
        )
    return (
        _frontmatter(plan)
        + f"# Tagesorganisationsplan {plan.datum.isoformat()}\n\n"
        + f"- Klasse: {plan.klasse}\n"
        + f"- Tagesziel: {plan.tagesziel}\n\n"
        + "## Material Bereitgelegt\n\n"
        + _bullet(plan.material_bereitgelegt)
        + "\n\n## Rituale\n\n"
        + _bullet(plan.rituale)
        + "\n\n## Besondere Organisation\n\n"
        + f"- Gruppen: {plan.besondere_organisation.gruppen}\n"
        + f"- Raumwechsel: {', '.join(plan.besondere_organisation.raumwechsel)}\n"
        + f"- Externe Termine: {', '.join(plan.besondere_organisation.externe_termine)}\n\n"
        + "## Stunden\n\n"
        + "\n\n".join(hours)
        + "\n\n## Offene Punkte Fuer Morgen\n\n"
        + _bullet(plan.offene_punkte_fuer_morgen)
        + "\n\n## Hinweis\n\n"
        + plan.teacher_review_note
        + "\n"
    )


def _substitution_plan_to_markdown(plan: SubstitutionPlan) -> str:
    return (
        _frontmatter(plan)
        + f"# Vertretungsplan {plan.datum.isoformat()}\n\n"
        + f"- Klasse: {plan.klasse}\n"
        + f"- Zeitraum: {plan.zeitraum}\n"
        + f"- Tagesziel: {plan.tagesziel}\n\n"
        + "## Material Bereitgelegt\n\n"
        + _bullet(plan.material_bereitgelegt)
        + "\n\n## Rituale\n\n"
        + _bullet(plan.rituale)
        + "\n\n## Sichere Aufgaben\n\n"
        + _bullet(plan.sichere_aufgaben)
        + "\n\n## Auslassbar\n\n"
        + _bullet(plan.auslassbar)
        + "\n\n## Vertretungshinweise\n\n"
        + _bullet(plan.vertretungshinweise)
        + "\n\n## Hinweis\n\n"
        + plan.teacher_review_note
        + "\n"
    )


def _handover_summary_to_markdown(summary: HandoverSummary) -> str:
    current = "\n".join(
        f"- {subject}: {state}" for subject, state in sorted(summary.aktueller_stand.items())
    ) or "- "
    units = "\n".join(
        f"- {unit.thema}: letzter Stand: {unit.letzter_stand}; naechster Schritt: "
        f"{unit.naechster_schritt}; Material: {unit.materialpfad}"
        for unit in summary.laufende_reihen
    ) or "- "
    return (
        _frontmatter(summary)
        + "# Klassenuebergabe Anonymisiert\n\n"
        + f"- Klasse: {summary.klasse}\n"
        + f"- Zeitraum: {summary.zeitraum}\n\n"
        + "## Aktueller Stand\n\n"
        + current
        + "\n\n## Laufende Reihen\n\n"
        + units
        + "\n\n## Routinen\n\n"
        + f"- Tagesbeginn: {summary.routinen.tagesbeginn}\n"
        + f"- Wochenplanarbeit: {summary.routinen.wochenplanarbeit}\n"
        + f"- Hausaufgaben: {summary.routinen.hausaufgaben}\n"
        + f"- Materialorganisation: {summary.routinen.materialorganisation}\n"
        + f"- Klassenregeln allgemein: {summary.routinen.klassenregeln_allgemein}\n\n"
        + "## Wichtig Fuer Vertretung\n\n"
        + _bullet(summary.wichtig_fuer_vertretung)
        + "\n\n## Offene To-dos\n\n"
        + _bullet(summary.offene_to_dos)
        + "\n\n## Hinweis\n\n"
        + summary.teacher_review_note
        + "\n"
    )


def schriftwesen_to_markdown(document: SchriftwesenDocument) -> str:
    assert_no_personal_data(document, context="Schriftwesen document")
    if isinstance(document, WeeklyPlan):
        return _weekly_plan_to_markdown(document)
    if isinstance(document, DailyTop):
        return _daily_top_to_markdown(document)
    if isinstance(document, SubstitutionPlan):
        return _substitution_plan_to_markdown(document)
    return _handover_summary_to_markdown(document)


def safe_filename_part(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    return cleaned.strip("._") or "schriftwesen"


def schriftwesen_filename_stem(document: SchriftwesenDocument) -> str:
    if isinstance(document, WeeklyPlan):
        return safe_filename_part(f"{document.woche}_wochenplan_{document.klasse}")
    if isinstance(document, DailyTop):
        return safe_filename_part(f"{document.datum.isoformat()}_TOP_{document.klasse}")
    if isinstance(document, SubstitutionPlan):
        return safe_filename_part(f"{document.datum.isoformat()}_vertretung_{document.klasse}")
    return safe_filename_part(f"uebergabe_{document.klasse}_{document.zeitraum}")


__all__ = [
    "ClassRoutines",
    "CurriculumLink",
    "DailyOrganization",
    "DailyTop",
    "DailyTopHour",
    "DailyTopRequest",
    "HandoverSummary",
    "HandoverSummaryRequest",
    "PrivacyValidationResult",
    "RunningUnit",
    "SchriftwesenDocument",
    "SubstitutionPlan",
    "SubstitutionPlanRequest",
    "WeeklyFocus",
    "WeeklyPlan",
    "WeeklyPlanDay",
    "WeeklyPlanRequest",
    "generate_daily_top",
    "generate_handover_summary",
    "generate_substitution_plan",
    "generate_weekly_plan",
    "safe_filename_part",
    "schriftwesen_filename_stem",
    "schriftwesen_to_markdown",
    "validate_privacy",
]

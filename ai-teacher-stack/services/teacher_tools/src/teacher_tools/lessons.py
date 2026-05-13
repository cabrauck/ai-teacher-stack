from teacher_tools.curriculum import map_topic_to_curriculum
from teacher_tools.models import CurriculumRecord, LessonPlan, LessonRequest


def generate_lesson_plan(
    request: LessonRequest,
    records: list[CurriculumRecord],
) -> LessonPlan:
    """Generate a deterministic starter lesson plan.

    This is intentionally rule-based for the scaffold. LLM-powered planning can be
    added later as an optional, review-gated enhancement.
    """
    curriculum_refs = map_topic_to_curriculum(
        records,
        subject=request.subject,
        grade_band=request.grade_band,
        topic=request.topic,
    )

    return LessonPlan(
        title=f"{request.subject}: {request.topic}",
        subject=request.subject,
        grade_band=request.grade_band,
        topic=request.topic,
        duration_minutes=request.duration_minutes,
        curriculum_references=curriculum_refs,
        learning_goals=[
            f"Die Schülerinnen und Schüler können zentrale Aspekte von '{request.topic}' erklären.",
            "Sie bearbeiten eine passende Aufgabe selbstständig oder mit Partnerunterstützung.",
            "Sie sichern ein Ergebnis in altersgerechter Sprache.",
        ],
        materials=[
            "Tafel oder digitales Board",
            "Arbeitsblatt",
            "Stifte",
            "ggf. Anschauungsmaterial",
        ],
        phases=[
            "Einstieg: Vorwissen aktivieren und Ziel der Stunde klären.",
            "Erarbeitung: Gemeinsame Beispielaufgabe oder Materialerkundung.",
            "Übung: Einzel- oder Partnerarbeit mit differenzierten Aufgaben.",
            "Sicherung: Ergebnisse vergleichen und zentrale Begriffe festhalten.",
            "Ausblick: Kurze Reflexionsfrage oder Anschlussaufgabe.",
        ],
        differentiation=[
            "Unterstützung: reduzierte Aufgabenmenge und Satzstarter.",
            "Erweiterung: offene Zusatzaufgabe mit Begründung.",
            "Partnerarbeit: stärkere und schwächere Lernende können sich sprachlich stützen.",
        ],
        assessment=[
            "Kann das Kind den zentralen Begriff in eigenen Worten erklären?",
            "Kann das Kind eine Aufgabe mit passendem Verfahren lösen?",
            "Kann das Kind ein Ergebnis verständlich sichern?",
        ],
        teacher_review_note=(
            "Automatisch erzeugter Entwurf. Vor dem Einsatz fachlich, pädagogisch "
            "und mit Blick auf die Lerngruppe prüfen."
        ),
    )

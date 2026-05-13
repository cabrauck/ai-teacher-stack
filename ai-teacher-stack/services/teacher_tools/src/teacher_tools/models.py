from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str
    url: str
    retrieved_at: str | None = None


class CurriculumRecord(BaseModel):
    id: str
    jurisdiction: str
    school_type: str
    grade_band: str
    subject: str
    learning_area: str
    competency: str
    content_examples: list[str] = Field(default_factory=list)
    source: Source


class LessonRequest(BaseModel):
    subject: str
    grade_band: str = "3/4"
    topic: str
    duration_minutes: int = 45


class LessonPlan(BaseModel):
    title: str
    subject: str
    grade_band: str
    topic: str
    duration_minutes: int
    curriculum_references: list[CurriculumRecord]
    learning_goals: list[str]
    materials: list[str]
    phases: list[str]
    differentiation: list[str]
    assessment: list[str]
    teacher_review_note: str


class ExportRequest(BaseModel):
    lesson: LessonPlan
    filename: str | None = None

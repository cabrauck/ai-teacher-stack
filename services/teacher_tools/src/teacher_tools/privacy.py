from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel

FORBIDDEN_PERSONAL_FIELDS = {
    "student_name",
    "student_names",
    "student_id",
    "student_ids",
    "pupil_name",
    "pupil_names",
    "schueler_name",
    "schueler_names",
    "schuelerinnen_name",
    "birthdate",
    "date_of_birth",
    "geburtsdatum",
    "grade",
    "grades",
    "note",
    "noten",
    "diagnosis",
    "diagnoses",
    "diagnose",
    "foerderdiagnose",
    "krankheitstage",
    "health_data",
    "parent_contact",
    "parent_contacts",
    "parent_message",
    "parent_communication",
    "elternkontakt",
    "elternnachricht",
    "elternkommunikation",
    "behavior_incident",
    "sensitive_case",
    "sensibler_einzelfall",
    "schuelerbeobachtung",
    "schuelerbeobachtungen",
    "student_observation",
    "student_observations",
    "leistungsaufschreibung",
    "leistungsaufschreibungen",
    "leistungsaufzeichnung",
    "leistungsaufzeichnungen",
    "credential",
    "credentials",
    "password",
    "token",
}

EXPLICIT_PERSONAL_DATA_FLAGS = {
    "contains_personal_data",
    "contains_student_data",
    "personenbezogene_daten",
    "student_data",
}


@dataclass(frozen=True)
class PrivacyIssue:
    field_path: str
    field_name: str
    message: str


@dataclass(frozen=True)
class PrivacyValidationResult:
    blocked_fields: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.blocked_fields

    @property
    def privacy_status(self) -> str:
        if self.ok:
            return "no_personal_data_detected"
        return "blocked_personal_data_fields"


class PrivacyError(ValueError):
    """Raised when a payload crosses the v1 no-student-data boundary."""


def normalize_field_name(name: str) -> str:
    translations = str.maketrans(
        {
            "ä": "ae",
            "ö": "oe",
            "ü": "ue",
            "ß": "ss",
            "Ä": "ae",
            "Ö": "oe",
            "Ü": "ue",
        }
    )
    return name.strip().translate(translations).casefold().replace("-", "_").replace(" ", "_")


def is_forbidden_field_name(name: str) -> bool:
    return normalize_field_name(name) in FORBIDDEN_PERSONAL_FIELDS


def _iter_items(payload: Any, prefix: str = "") -> Iterable[PrivacyIssue]:
    if isinstance(payload, BaseModel):
        payload = payload.model_dump(mode="json")
    elif isinstance(payload, Path):
        payload = str(payload)

    if isinstance(payload, dict):
        for key, value in payload.items():
            key_text = str(key)
            path = f"{prefix}.{key_text}" if prefix else key_text
            normalized = normalize_field_name(key_text)
            if normalized in FORBIDDEN_PERSONAL_FIELDS:
                yield PrivacyIssue(
                    field_path=path,
                    field_name=key_text,
                    message=f"Field '{path}' is outside the v1 privacy boundary.",
                )
            if normalized in EXPLICIT_PERSONAL_DATA_FLAGS and value is True:
                yield PrivacyIssue(
                    field_path=path,
                    field_name=key_text,
                    message=f"Field '{path}' explicitly marks personal data.",
                )
            yield from _iter_items(value, path)
    elif isinstance(payload, list | tuple | set):
        for index, value in enumerate(payload):
            path = f"{prefix}[{index}]"
            yield from _iter_items(value, path)


def validate_privacy(payload: Any, *, warn_only: bool = False) -> PrivacyValidationResult:
    issues = tuple(_iter_items(payload))
    messages = tuple(issue.message for issue in issues)
    if warn_only:
        return PrivacyValidationResult(warnings=messages)
    return PrivacyValidationResult(blocked_fields=tuple(issue.field_path for issue in issues))


def assert_no_personal_data(*payloads: Any, context: str = "payload") -> PrivacyValidationResult:
    blocked: list[str] = []
    warnings: list[str] = []
    for payload in payloads:
        result = validate_privacy(payload)
        blocked.extend(result.blocked_fields)
        warnings.extend(result.warnings)

    validation = PrivacyValidationResult(
        blocked_fields=tuple(dict.fromkeys(blocked)),
        warnings=tuple(dict.fromkeys(warnings)),
    )
    if not validation.ok:
        joined = ", ".join(validation.blocked_fields)
        raise PrivacyError(f"{context} blocked by privacy policy: {joined}")
    return validation

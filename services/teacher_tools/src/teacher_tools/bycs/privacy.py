from typing import Any

from teacher_tools.privacy import (
    PrivacyError,
    PrivacyIssue,
    PrivacyValidationResult,
    assert_no_personal_data,
    is_forbidden_field_name,
    normalize_field_name,
    validate_privacy,
)


class ByCSPrivacyError(PrivacyError):
    """Raised when an export payload crosses the v1 privacy boundary."""


def assert_export_privacy(*payloads: Any) -> PrivacyValidationResult:
    try:
        return assert_no_personal_data(*payloads, context="ByCS export")
    except PrivacyError as exc:
        raise ByCSPrivacyError(str(exc)) from exc


__all__ = [
    "ByCSPrivacyError",
    "PrivacyIssue",
    "PrivacyValidationResult",
    "assert_export_privacy",
    "is_forbidden_field_name",
    "normalize_field_name",
    "validate_privacy",
]

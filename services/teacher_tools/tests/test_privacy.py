from __future__ import annotations

import pytest

from teacher_tools.privacy import PrivacyError, assert_no_personal_data, validate_privacy


def test_neutral_privacy_blocks_personal_fields_and_markers():
    result = validate_privacy(
        {
            "schuelerbeobachtung": "nicht erfassen",
            "topic": "Kartenarbeit",
            "contains_personal_data": True,
        }
    )

    assert not result.ok
    assert result.blocked_fields == ("schuelerbeobachtung", "contains_personal_data")


def test_neutral_privacy_allows_class_level_schriftwesen_fields():
    payload = {
        "klasse": "Klasse 3a",
        "personenbezogene_daten": False,
        "material": ["Wochenplan"],
        "gruppen": "Gruppe A/B",
    }

    assert validate_privacy(payload).ok
    assert assert_no_personal_data(payload).privacy_status == "no_personal_data_detected"


def test_neutral_privacy_blocks_leistungsaufschreibungen():
    with pytest.raises(PrivacyError):
        assert_no_personal_data({"leistungsaufschreibungen": []})


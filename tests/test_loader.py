import json
import logging
from pathlib import Path

import pytest
from pydantic import ValidationError

from live_commentator.statsbomb.loader import load_events
from live_commentator.statsbomb.models import BaseEvent, PassEvent, StartingXIEvent

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "events_8658_sample.json"


def test_load_events() -> None:
    events = load_events(FIXTURE_PATH)
    assert len(events) == 3
    assert type(events[0]) is StartingXIEvent
    assert type(events[1]) is PassEvent
    assert type(events[2]) is BaseEvent


def test_log_warning_on_duplicates_load(caplog: pytest.LogCaptureFixture) -> None:
    duplicate_id = "4a44199a-3111-4e28-b567-9c1393e68dff"

    load_events(FIXTURE_PATH)
    log_records = caplog.records

    assert len(log_records) == 1
    assert duplicate_id in log_records[0].getMessage()
    assert log_records[0].levelno == logging.WARNING


def test_exception_on_broken_data_load(tmp_path: Path) -> None:
    broken_event = """
    [
    {"type": "Pass"}
    ]
    """
    broken_file_path = tmp_path / "broken.json"

    broken_file_path.write_text(broken_event, encoding="utf-8")
    with pytest.raises(ValidationError) as exec_info:
        load_events(broken_file_path)

    validation_errors = exec_info.value.errors()
    assert len(validation_errors) == 1
    assert validation_errors[0]["type"] == "union_tag_not_found"


def test_file_not_found(tmp_path: Path) -> None:
    file_not_exists = tmp_path / "file_not_exists.json"

    with pytest.raises(FileNotFoundError):
        load_events(file_not_exists)


def test_validate_timestamp(tmp_path: Path) -> None:
    events = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    events[0]["timestamp"] = "abc"
    bad_path = tmp_path / "bad_events.json"
    bad_path.write_text(json.dumps(events), encoding="utf-8")
    with pytest.raises(ValidationError) as exception_info:
        load_events(bad_path)

    validation_errors = exception_info.value.errors()
    assert len(validation_errors) == 1
    assert validation_errors[0]["type"] == "string_pattern_mismatch"

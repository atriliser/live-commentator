import json
from pathlib import Path

import pytest

from live_commentator.replay import pause_seconds, timestamp_to_seconds
from live_commentator.statsbomb.models import BaseEvent

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "events_8658_sample.json"
EVENTS = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def make_event(period: int, timestamp: str) -> BaseEvent:
    new_event = {**EVENTS[0], "period": period, "timestamp": timestamp}
    return BaseEvent.model_validate(new_event)


@pytest.mark.parametrize(
    ("timestamp_given", "timestamp_expected"),
    [("00:00:00.000", 0.0), ("00:01:02.500", 62.5), ("01:00:00.000", 3600.0)],
)
def test_timestamp_to_seconds(timestamp_given: str, timestamp_expected: float) -> None:
    assert timestamp_to_seconds(timestamp_given) == timestamp_expected


@pytest.mark.parametrize(
    (
        "period_prev",
        "timestamp_prev",
        "period_curr",
        "timestamp_curr",
        "pause_expected",
    ),
    [
        (1, "00:00:01.000", 1, "00:00:01.000", 0.0),
        (1, "00:00:01.000", 1, "00:00:03.500", 2.5),
        (1, "00:00:59.500", 1, "00:01:00.250", 0.75),
        (1, "00:47:10.000", 2, "00:00:00.000", 0.0),
    ],
)
def test_pause_seconds(
    period_prev: int,
    timestamp_prev: str,
    period_curr: int,
    timestamp_curr: str,
    pause_expected: float,
) -> None:
    event_prev = make_event(period_prev, timestamp_prev)
    event_curr = make_event(period_curr, timestamp_curr)
    assert pause_seconds(event_prev, event_curr) == pause_expected

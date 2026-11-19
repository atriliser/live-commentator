import json
from pathlib import Path
from typing import Any

import pytest

from live_commentator.statsbomb.loader import load_events
from live_commentator.statsbomb.models import StatsBombEvent


@pytest.fixture
def sample_events_path() -> Path:
    return Path(__file__).parent / "fixtures" / "events_8658_sample.json"


@pytest.fixture
def sample_events(sample_events_path: Path) -> list[StatsBombEvent]:
    return load_events(sample_events_path)


@pytest.fixture
def sample_raw_events(sample_events_path: Path) -> list[dict[str, Any]]:
    raw: list[dict[str, Any]] = json.loads(
        sample_events_path.read_text(encoding="utf-8")
    )
    return raw

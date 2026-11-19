from pathlib import Path

import pytest

from live_commentator.statsbomb.loader import load_events
from live_commentator.statsbomb.models import StatsBombEvent


@pytest.fixture
def sample_events_path() -> Path:
    return Path(__file__).parent / "fixtures" / "events_8658_sample.json"


@pytest.fixture
def sample_events(sample_events_path: Path) -> list[StatsBombEvent]:
    return load_events(sample_events_path)

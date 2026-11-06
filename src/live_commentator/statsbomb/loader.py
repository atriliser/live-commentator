from pathlib import Path

from pydantic import TypeAdapter

from live_commentator.statsbomb.models import StatsBombEvent

_EVENTS_ADAPTER = TypeAdapter(list[StatsBombEvent])


def load_events(path: Path) -> list[StatsBombEvent]:
    return _EVENTS_ADAPTER.validate_json(path.read_bytes())

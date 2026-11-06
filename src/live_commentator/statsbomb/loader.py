import logging
from pathlib import Path

from pydantic import TypeAdapter

from live_commentator.statsbomb.models import StatsBombEvent

_EVENTS_ADAPTER = TypeAdapter(list[StatsBombEvent])
logger = logging.getLogger(__name__)


def _drop_duplicates(events: list[StatsBombEvent]) -> list[StatsBombEvent]:
    event_ids: set[str] = set()
    unique_events = []

    for event in events:
        if event.id not in event_ids:
            unique_events.append(event)
            event_ids.add(event.id)
        else:
            logger.warning(
                "Dropping duplicate event_id: %s and event_name %s",
                event.id,
                event.type.name,
            )

    return unique_events


def load_events(path: Path) -> list[StatsBombEvent]:
    return _drop_duplicates(_EVENTS_ADAPTER.validate_json(path.read_bytes()))

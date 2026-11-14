from pathlib import Path

from live_commentator.messages import MatchEventMessage
from live_commentator.statsbomb.loader import load_events

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "events_8658_sample.json"
MATCH_ID = 8658


def test_match_event_message_survives_json_round_trip() -> None:
    events = load_events(FIXTURE_PATH)

    for event in events:
        message = MatchEventMessage(match_id=MATCH_ID, event=event)

        restored = MatchEventMessage.model_validate_json(message.model_dump_json())

        assert restored == message
        assert type(restored.event) is type(message.event)

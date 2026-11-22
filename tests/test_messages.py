from live_commentator.messages import MatchEventMessage
from live_commentator.statsbomb.models import StatsBombEvent

MATCH_ID = 8658


def test_match_event_message_survives_json_round_trip(
    sample_events: list[StatsBombEvent],
) -> None:
    for event in sample_events:
        message = MatchEventMessage(match_id=MATCH_ID, event=event)

        restored = MatchEventMessage.model_validate_json(message.model_dump_json())

        assert restored == message
        assert type(restored.event) is type(message.event)

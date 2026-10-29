import pytest
from pydantic import ValidationError

from live_commentator.events import EventType, MatchEvent, MatchPlayer

player = MatchPlayer(id=11, name="Lionel Messi")
event_type = EventType(id=1, name="match")
event = MatchEvent(minute=1, type=event_type, player=player, location=(10.0, 10.0))
json_event_str = '{"minute": "1", "type": {"id": "1", "name": "match"}, "player": {"id": "11", "name": "Lionel Messi"}, "location": [10.0, 10.0]}'
json_invalid_event_str = '{"minute": "1", "type": {"id": "1", "name": "match"}, "player": {"id": "Uno", "name": "Lionel Messi"}, "location": [10.0, 10.0]}'


def test_parse_json_positive() -> None:
    assert MatchEvent.model_validate_json(json_event_str) == event


def test_parse_json_negative() -> None:
    with pytest.raises(ValidationError):
        MatchEvent.model_validate_json(json_invalid_event_str)

import asyncio

from live_commentator.messages import MatchEventMessage
from live_commentator.publisher import publish
from live_commentator.statsbomb.models import BaseEvent, StatsBombEvent

TOPIC = "match-events"
MATCH_ID = 8658


class FakeProducer:
    def __init__(self) -> None:
        self.sent: list[tuple[str, bytes, bytes]] = []

    async def send_and_wait(self, topic: str, value: bytes, key: bytes) -> None:
        self.sent.append((topic, value, key))


def test_publish_sends_one_message_per_event_in_order(
    sample_events: list[StatsBombEvent],
) -> None:
    queue: asyncio.Queue[BaseEvent | None] = asyncio.Queue()
    for event in sample_events:
        queue.put_nowait(event)
    queue.put_nowait(None)
    producer = FakeProducer()

    asyncio.run(publish(queue, producer, TOPIC, MATCH_ID))

    assert len(producer.sent) == len(sample_events)
    assert all(topic == TOPIC for topic, _, _ in producer.sent)
    assert all(key == b"8658" for _, _, key in producer.sent)
    assert all(type(value) is bytes for _, value, _ in producer.sent)
    received = [
        MatchEventMessage.model_validate_json(value).event
        for _, value, _ in producer.sent
    ]
    assert received == sample_events

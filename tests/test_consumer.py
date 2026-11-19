import asyncio
from collections.abc import AsyncIterator

from live_commentator.consumer import consume
from live_commentator.messages import MatchEventMessage
from live_commentator.statsbomb.models import StatsBombEvent

MATCH_ID = 8658


class FakeRecord:
    def __init__(self, value: bytes) -> None:
        self.value = value


async def fake_consumer(records: list[FakeRecord]) -> AsyncIterator[FakeRecord]:
    for record in records:
        yield record


def test_consume_puts_decoded_messages_in_order(
    sample_events: list[StatsBombEvent],
) -> None:
    expected = [MatchEventMessage(match_id=MATCH_ID, event=e) for e in sample_events]
    records = [FakeRecord(m.model_dump_json().encode()) for m in expected]
    queue: asyncio.Queue[MatchEventMessage] = asyncio.Queue()

    asyncio.run(consume(fake_consumer(records), queue))

    received = [queue.get_nowait() for _ in range(queue.qsize())]
    assert received == expected

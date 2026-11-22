import asyncio

from live_commentator.broadcaster import Broadcaster
from live_commentator.messages import MatchEventMessage
from live_commentator.statsbomb.models import StatsBombEvent

MATCH_ID = 8658


def test_run_delivers_all_messages_to_every_subscriber_in_order(
    sample_events: list[StatsBombEvent],
) -> None:
    expected = [MatchEventMessage(match_id=MATCH_ID, event=e) for e in sample_events]

    async def scenario() -> tuple[list[MatchEventMessage], list[MatchEventMessage]]:
        broadcaster = Broadcaster()
        q1 = broadcaster.subscribe()
        q2 = broadcaster.subscribe()
        source: asyncio.Queue[MatchEventMessage] = asyncio.Queue()

        task = asyncio.create_task(broadcaster.run(source))
        for message in expected:
            source.put_nowait(message)

        received_1 = [await q1.get() for _ in range(len(expected))]
        received_2 = [await q2.get() for _ in range(len(expected))]
        task.cancel()
        return received_1, received_2

    received_1, received_2 = asyncio.run(scenario())

    assert received_1 == expected
    assert received_2 == expected

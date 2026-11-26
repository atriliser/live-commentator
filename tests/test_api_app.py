import asyncio
from collections.abc import AsyncGenerator
from typing import cast

from live_commentator.api_app import broadcaster, match_events
from live_commentator.messages import MatchEventMessage
from live_commentator.statsbomb.models import StatsBombEvent

MATCH_ID = 8658


def test_match_events_streams_messages_and_unsubscribes_on_close(
    sample_events: list[StatsBombEvent],
) -> None:
    expected = [MatchEventMessage(match_id=MATCH_ID, event=e) for e in sample_events]

    async def scenario() -> tuple[list[MatchEventMessage], int, int]:
        source: asyncio.Queue[MatchEventMessage] = asyncio.Queue()
        task = asyncio.create_task(broadcaster.run(source))
        stream = cast(AsyncGenerator[MatchEventMessage, None], match_events(MATCH_ID))

        first = asyncio.create_task(anext(stream))
        await asyncio.sleep(0)
        subscribed = len(broadcaster._subscribers)

        for message in expected:
            source.put_nowait(message)
        received = [await first]
        received += [await anext(stream) for _ in range(len(expected) - 1)]

        await stream.aclose()
        left = len(broadcaster._subscribers)
        task.cancel()
        return received, subscribed, left

    received, subscribed, left = asyncio.run(scenario())

    assert subscribed == 1
    assert received == expected
    assert left == 0

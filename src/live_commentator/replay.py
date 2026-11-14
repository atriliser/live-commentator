import asyncio
import itertools
from collections.abc import Sequence

from live_commentator.statsbomb.models import BaseEvent


def timestamp_to_seconds(timestamp: str) -> float:
    hours, minutes, seconds = timestamp.split(":")
    return int(hours) * 60 * 60 + int(minutes) * 60 + float(seconds)


def pause_seconds(prev: BaseEvent, curr: BaseEvent) -> float:
    if prev.period != curr.period:
        return 0.0
    return timestamp_to_seconds(curr.timestamp) - timestamp_to_seconds(prev.timestamp)


async def replay(
    events: Sequence[BaseEvent],
    queue: asyncio.Queue[BaseEvent | None],
    speedup: float,
) -> None:
    if events:
        await queue.put(events[0])
    for event_prev, event_curr in itertools.pairwise(events):
        delay = pause_seconds(event_prev, event_curr) / speedup
        await asyncio.sleep(delay)
        await queue.put(event_curr)

    await queue.put(None)

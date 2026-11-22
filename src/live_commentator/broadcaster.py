import asyncio
import logging

from live_commentator.messages import MatchEventMessage

SUBSCRIBER_QUEUE_SIZE = 100
logger = logging.getLogger(__name__)


class Broadcaster:
    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue[MatchEventMessage]] = set()

    def subscribe(self) -> asyncio.Queue[MatchEventMessage]:
        events_queue: asyncio.Queue[MatchEventMessage] = asyncio.Queue(
            maxsize=SUBSCRIBER_QUEUE_SIZE
        )
        self._subscribers.add(events_queue)
        return events_queue

    def unsubscribe(self, events_queue: asyncio.Queue[MatchEventMessage]) -> None:
        self._subscribers.discard(events_queue)

    async def run(self, source: asyncio.Queue[MatchEventMessage]) -> None:
        while True:
            message = await source.get()
            for subscriber in self._subscribers:
                try:
                    subscriber.put_nowait(message)
                except asyncio.QueueFull:
                    logger.warning(
                        "Subscriber queue full, dropping event %s of match %s",
                        message.event.id,
                        message.match_id,
                    )

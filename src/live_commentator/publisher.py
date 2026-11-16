import asyncio
from typing import Protocol

from live_commentator.messages import MatchEventMessage
from live_commentator.statsbomb.models import BaseEvent


class Producer(Protocol):
    async def send_and_wait(self, topic: str, value: bytes, key: bytes) -> object: ...


async def publish(
    queue: asyncio.Queue[BaseEvent | None],
    producer: Producer,
    topic: str,
    match_id: int,
) -> None:
    while True:
        event = await queue.get()

        if event is None:
            return

        event_msg = MatchEventMessage(match_id=match_id, event=event)

        await producer.send_and_wait(
            topic,
            key=str(match_id).encode("utf-8"),
            value=event_msg.model_dump_json().encode(encoding="utf-8"),
        )

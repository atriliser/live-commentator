import asyncio
from collections.abc import AsyncIterable
from typing import Protocol

from live_commentator.messages import MatchEventMessage


class Record(Protocol):
    value: bytes


async def consume(
    consumer: AsyncIterable[Record], queue: asyncio.Queue[MatchEventMessage]
) -> None:
    async for msg in consumer:
        message = MatchEventMessage.model_validate_json(msg.value)
        await queue.put(message)

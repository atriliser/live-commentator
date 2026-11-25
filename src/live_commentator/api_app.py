import asyncio
from collections.abc import AsyncIterable, AsyncIterator
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse

from live_commentator.broadcaster import Broadcaster
from live_commentator.consumer import consume
from live_commentator.messages import MatchEventMessage

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "match-events"
broadcaster = Broadcaster()


@asynccontextmanager
async def lifespan(api: FastAPI) -> AsyncIterator[None]:
    consumer = AIOKafkaConsumer(
        TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset="earliest"
    )
    await consumer.start()
    source: asyncio.Queue[MatchEventMessage] = asyncio.Queue()
    consume_task = asyncio.create_task(consume(consumer, source))
    broadcast_task = asyncio.create_task(broadcaster.run(source))
    try:
        yield
    finally:
        consume_task.cancel()
        broadcast_task.cancel()
        await consumer.stop()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/matches/{match_id}/events", response_class=EventSourceResponse)
async def matches(match_id: int) -> AsyncIterable[MatchEventMessage]:
    events_queue = broadcaster.subscribe()
    try:
        while True:
            yield await events_queue.get()
    finally:
        broadcaster.unsubscribe(events_queue)

from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.sse import EventSourceResponse

from live_commentator.broadcaster import Broadcaster
from live_commentator.messages import MatchEventMessage

app = FastAPI()
broadcaster = Broadcaster()


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

import asyncio
import os
from pathlib import Path

from aiokafka import AIOKafkaProducer

from live_commentator.publisher import publish
from live_commentator.replay import replay
from live_commentator.statsbomb.loader import load_events
from live_commentator.statsbomb.models import BaseEvent

EVENTS_DATA_PATH = Path("data/raw/8658.json")
BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
MATCH_ID = int(os.environ.get("MATCH_ID", "8658"))
TOPIC = os.environ.get("KAFKA_TOPIC", "match-events")
SPEEDUP = float(os.environ.get("REPLAY_SPEEDUP", "60.0"))
START_DELAY_SECONDS = int(os.environ.get("REPLAY_START_DELAY_SECONDS", "0"))


async def main() -> None:
    events = load_events(EVENTS_DATA_PATH)
    queue: asyncio.Queue[BaseEvent | None] = asyncio.Queue()
    producer = AIOKafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    await producer.start()

    try:
        await asyncio.sleep(START_DELAY_SECONDS)
        await asyncio.gather(
            replay(events, queue, SPEEDUP),
            publish(queue, producer, TOPIC, MATCH_ID),
        )
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())

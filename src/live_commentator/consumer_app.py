import asyncio

from aiokafka import AIOKafkaConsumer

from live_commentator.consumer import consume
from live_commentator.messages import MatchEventMessage

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "match-events"


async def print_events(queue: asyncio.Queue[MatchEventMessage]) -> None:
    while True:
        msg = await queue.get()
        print(f"{msg.event.minute}' {msg.event.type.name} — {msg.event.team.name}")


async def main() -> None:
    consumer = AIOKafkaConsumer(
        TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset="earliest"
    )
    queue: asyncio.Queue[MatchEventMessage] = asyncio.Queue()
    await consumer.start()

    try:
        await asyncio.gather(consume(consumer, queue), print_events(queue))
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio


async def main() -> None:
    queue: asyncio.Queue[str] = asyncio.Queue()
    await queue.put("Starting XI")
    await queue.put("Half Start")
    await queue.put("Pass")

    while not queue.empty():
        print(await queue.get())


asyncio.run(main())

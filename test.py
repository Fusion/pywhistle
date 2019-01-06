import asyncio
from aiohttp import ClientSession
from pywhistle import Client


async def main() -> None:
    async with ClientSession() as websession:
        client = Client(USERNAME, PASSWORD, websession)
        await client.async_init()
        print(await client.get_pets())
        print(await client.get_places())


asyncio.get_event_loop().run_until_complete(main())

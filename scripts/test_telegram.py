import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from tg_client import client

async def main():
    await client.start()

    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")

    await client.disconnect()

asyncio.run(main())
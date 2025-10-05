from telethon import TelegramClient, events, sync, types
import os, dotenv, time, json, datetime, random, asyncio
from ai import get_prices
import pandas as pd
import re
from pytz import timezone

dotenv.load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

client = TelegramClient('session_name', api_id, api_hash)

correct_dates = False

async def load_messages():
    group = -1002708000057
    async for message in client.iter_messages(group, limit=5000):
        output = get_prices(message.message)

        if output:
            with open("data.json", "r") as f:
                data = json.load(f)
            data.append(output)
            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)

            time.sleep(2.1)

async def main():
    await load_messages()

with client:
    client.loop.run_until_complete(main())
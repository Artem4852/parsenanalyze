from telethon import TelegramClient, events, sync, types
import os, dotenv, time, json, datetime, random, asyncio
import pandas as pd
import re
from pytz import timezone

dotenv.load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')

client = TelegramClient('session_name', api_id, api_hash)

correct_dates = False

async def load_messages():
    group = -1001330198986
    async for message in client.iter_messages(group, limit=5000):
        if not message.photo:
            continue

        # save image in images/id.jpg
        image_path = f"images/{message.id}.jpg"
        if not os.path.exists(image_path):
            await message.download_media(file=image_path)

            await asyncio.sleep(2.1)

async def main():
    await load_messages()

with client:
    client.loop.run_until_complete(main())
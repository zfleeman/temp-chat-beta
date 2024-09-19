import asyncio
from datetime import datetime, timedelta
import logging
import os
from zoneinfo import ZoneInfo

import discord
from discord.ext import tasks

# configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# create our client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# config from environment
token = os.getenv("BOT_TOKEN")
temp_chat_beta = int(os.getenv("CHANNEL_ID"))
delay = int(os.getenv("BEFORE_MINUTES", "60"))
loop_time = int(os.getenv("LOOP_TIME", "30"))
sleep_time = float(os.getenv("SLEEP_TIME", "0.25"))
tz = os.getenv("TZ")


@tasks.loop(seconds=loop_time)
async def delete_old_messages():
    try:
        channel = client.get_channel(temp_chat_beta)
        before_time = datetime.now() - timedelta(minutes=delay)
        async for message in channel.history(before=before_time):
            try:
                await message.delete()
                logging.info(
                    f"Deleted message {message.id}, sent at {message.created_at.astimezone(ZoneInfo(tz)).strftime("%H:%M%p")}"
                )
                await asyncio.sleep(sleep_time)
            except Exception as e:
                logging.warning(f"An error occurred: {e}")

    except Exception as e:
        logging.warning(f"An error occurred {e}")


@delete_old_messages.before_loop
async def startup():
    logging.info("Waiting until the client is ready")
    await client.wait_until_ready()


@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")
    delete_old_messages.start()


client.run(token=token)

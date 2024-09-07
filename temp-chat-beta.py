import discord
import asyncio
from datetime import datetime, timedelta
import os

from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# config from environment
token = os.getenv("BOT_TOKEN")
temp_chat_beta = int(os.getenv("CHANNEL_ID"))
delay = int(os.getenv("BEFORE_MINUTES", default="60"))
loop_time = int(os.getenv("LOOP_TIME", default="30"))
sleep_time = float(os.getenv("SLEEP_TIME", default="0.25"))


@tasks.loop(seconds=loop_time)
async def delete_old_messages():
    try:
        channel = client.get_channel(temp_chat_beta)
        before_time = datetime.now() - timedelta(minutes=delay)
        messages = channel.history(before=before_time)

        if messages:
            async for message in messages:
                await message.delete()
            await asyncio.sleep(sleep_time)

    except Exception as e:
        print(f"An error occurred {e}")


@delete_old_messages.before_loop
async def startup():
    print("Waiting until the client is ready")
    await client.wait_until_ready()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    delete_old_messages.start()


client.run(token=token)

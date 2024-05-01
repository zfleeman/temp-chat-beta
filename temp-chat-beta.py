import discord
import asyncio
from datetime import datetime, timedelta
import os
import logging

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# config from environment
token = os.getenv("BOT_TOKEN")
temp_chat_beta = int(os.getenv("CHANNEL_ID"))
delay = int(os.getenv("BEFORE_MINUTES", default="60"))
sleep_time = int(os.getenv("SLEEP_TIME", default="30"))

async def retrieve_messages():

    channel = client.get_channel(temp_chat_beta)
    before_time = datetime.now() - timedelta(minutes=delay)
    messages = channel.history(before=before_time)
    messages_len = 0
    async for message in messages:
        await message.delete()
        messages_len += 1
    if messages_len > 0:
        logging.info(f"deleted {messages_len} messages")


async def main():
    while True:
        await retrieve_messages()
        await asyncio.sleep(sleep_time)

@client.event
async def on_ready():
    await main()

client.run(token=token)

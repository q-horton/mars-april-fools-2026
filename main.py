import discord
import os
from dotenv import load_dotenv
from agent import run_agent

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} is connected!')


@client.event
async def on_message(message: discord.Message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    if client.user in message.mentions:
        # Pre-processing
        msg_words = message.content.split(" ")
        for i in range(len(msg_words)):
            if msg_words[i] == f"<@{client.user.id}>":
                msg_words[i] = f"@{client.user.name}"
        formatted_msg = " ".join(msg_words)
        print(f"User {message.author.name} said: {formatted_msg}")

        # Feed to LLM
        response = run_agent(formatted_msg)
        response = (f"<@{message.author.id}>").join(response.split("%USER%"))
        response = (f"<#{message.channel.id}>").join(response.split("%CHANNEL%"))

        # Send back and log
        print(f"===<RESPONSE>===\r\n{response}\r\n==========")
        await message.reply(response)

client.run(DISCORD_TOKEN)

import discord
from discord import Intents
import openai
import os
import re
from config import OPENAI_API_KEY, DISCORD_TOKEN


# Set up intents and Discord client
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Set up OpenAI API
openai.api_key = OPENAI_API_KEY

# Function to send prompt to ChatGPT and get a response
async def get_gpt_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# Event handler for bot initialization
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

# Event handler for messages
@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Prepare the mention pattern and command pattern
    mention_pattern = f'<@!?{client.user.id}>'
    command_pattern = f'^(?:{mention_pattern}[\s]*)?!gpt(.*)'

    # Check if the message is a direct message or if it mentions the bot and starts with the command prefix (e.g., !gpt)
    if isinstance(message.channel, discord.DMChannel) or re.match(mention_pattern, message.content):
        match = re.match(command_pattern, message.content)
        if match:
            prompt = match.group(1).strip()
            if not prompt:
                await message.channel.send("Please provide a prompt after !gpt")
                return

            response = await get_gpt_response(prompt)
            await message.channel.send(response)


# Start the bot
client.run(DISCORD_TOKEN)

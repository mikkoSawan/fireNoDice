import discord
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Get the token from the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the intents so the bot can read message content
intents = discord.Intents.default()
intents.message_content = True

# Initialize the client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Successfully logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent infinite loops
    if message.author == client.user:
        return

    # Check if the word "fire" is in the message (converted to lowercase for easier checking)
    if 'fire' in message.content.lower():
        try:
            # React with the unicode emojis for :no_entry_sign: and :game_die:
            await message.add_reaction('🚫')
            await message.add_reaction('🎲')
            print(f'Reacted to a message from {message.author}')
        except discord.errors.HTTPException as e:
            print(f'Failed to add reaction: {e}')

if TOKEN is None:
    print("Error: DISCORD_TOKEN is not set in the .env file.")
else:
    client.run(TOKEN)
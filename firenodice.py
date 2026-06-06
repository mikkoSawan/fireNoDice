import discord
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Get the token from the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Default file path for the announcement image
DEFAULT_ANNOUNCEMENT_IMAGE = 'announcement.png'

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

    lower_content = message.content.lower()

    # Command to announce an image and ping everyone in the channel
    if lower_content.startswith('!announce_image'):
        allowed_mentions = discord.AllowedMentions(everyone=True)
        parts = message.content.split(maxsplit=1)
        image_source = parts[1].strip() if len(parts) > 1 else None

        if image_source:
            if image_source.startswith(('http://', 'https://')):
                embed = discord.Embed()
                embed.set_image(url=image_source)
                await message.channel.send(content='@everyone', embed=embed, allowed_mentions=allowed_mentions)
            elif os.path.isfile(image_source):
                await message.channel.send(content='@everyone', file=discord.File(image_source), allowed_mentions=allowed_mentions)
            else:
                await message.channel.send(
                    'Image not found. Provide a valid local path or URL, or omit the argument to use the default image.',
                    allowed_mentions=allowed_mentions,
                )
        elif os.path.isfile(DEFAULT_ANNOUNCEMENT_IMAGE):
            await message.channel.send(content='@everyone', file=discord.File(DEFAULT_ANNOUNCEMENT_IMAGE), allowed_mentions=allowed_mentions)
        else:
            await message.channel.send(
                'No default announcement image found. Add announcement.png to the bot folder, or use `!announce_image <path|url>`.',
                allowed_mentions=allowed_mentions,
            )
        return

    # Check if the word "fire" is in the message (converted to lowercase for easier checking)
    if 'fire' in lower_content:
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
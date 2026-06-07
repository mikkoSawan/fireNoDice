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
intents.reactions = True

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


@client.event
async def on_reaction_add(reaction, user):
    # Ignore reactions added by the bot itself
    if user == client.user:
        return

    # Determine if the added reaction is a fire emoji (unicode or custom named "fire")
    try:
        emoji_str = str(reaction.emoji)
        is_fire = emoji_str == '🔥' or getattr(reaction.emoji, 'name', None) == 'fire'
    except Exception:
        is_fire = False

    if not is_fire:
        return

    message = reaction.message
    try:
        # For each emoji we want to add, only add it if the bot hasn't already reacted with it
        needed = ('🚫', '🎲')
        # Build a map of existing reactions on the message for quick lookup
        existing = {str(r.emoji): r for r in message.reactions}

        for em in needed:
            already = False
            if em in existing:
                # Check whether the bot is already one of the users who reacted with this emoji
                async for u in existing[em].users():
                    if u == client.user:
                        already = True
                        break
            if not already:
                await message.add_reaction(em)

        # print a message to the console for debugging purposes
        print(f'Reacted to message {message.id} with NO and DIE emote because it was reacted to with the FIRE emote by {user}')
    except discord.errors.HTTPException as e:
        print(f'Failed to add reaction after fire: {e}')

if TOKEN is None:
    print("Error: DISCORD_TOKEN is not set in the .env file.")
else:
    client.run(TOKEN)
from discord.ext import commands
import discord
import json
from dotenv import load_dotenv
import os

with open("user_emojis.json", "r") as file:
    user_emojis = json.load(file)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    author_id = str(message.author.id)
    if author_id in user_emojis:
        emoji = user_emojis[author_id]
        await message.add_reaction(emoji)
    await bot.process_commands(message)


@bot.command(name="add_react")
async def add_react(ctx, user: discord.User, emoji: str):
    user_id = str(user.id)
    user_emojis[user_id] = emoji

    with open("user_emojis.json", "w") as file:
        json.dump(user_emojis, file, indent=4)

    await ctx.send(f"Reaction added for {user.mention}: {emoji}")


# Run the bot with the token
load_dotenv()
bot_token = os.getenv("EMOJI_REACT_TOKEN")
print(bot_token)
bot.run(bot_token)

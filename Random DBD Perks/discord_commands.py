import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from random_perks import (
    update_perks_from_wiki,
    read_perks_from_csv,
    get_random_perks,
    reroll_perks,
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
user_perks = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="get_random_perks")
async def get_random_perks_command(ctx):
    all_perks = read_perks_from_csv()
    user_id = str(ctx.author.id)
    user_perks[user_id] = get_random_perks(all_perks)
    perks = user_perks[user_id]
    await ctx.send("\n".join(perks))


@bot.command(name="reroll")
async def reroll_perks_command(ctx, *reroll_values):
    reroll_values = " ".join(reroll_values).split(", ")
    all_perks = read_perks_from_csv()

    user_id = str(ctx.author.id)
    if user_id not in user_perks:
        await ctx.send(
            "You don't have any perks. Generate random perks using `!get_random_perks`."
        )
        return
    current_perks = user_perks[user_id]
    perks = reroll_perks(all_perks, current_perks, reroll_values)
    user_perks[user_id] = perks
    await ctx.send("\n".join(perks))


if __name__ == "__main__":
    load_dotenv()
    bot_token = os.getenv("RANDOM_PERKS_TOKEN")
    print(bot_token)
    if bot_token is None:
        print("ERROR: No token found in .env")
    update_perks_from_wiki()
    bot.run(bot_token)

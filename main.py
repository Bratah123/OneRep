import discord
from discord.ext import commands

token = ""

with open("token.txt") as f:
    lines = f.read()
    token += lines.split('\n', 1)[0]

bot = commands.Bot(command_prefix='!')

print("Loading all commands via cogs...")

# bot.load_extension("commands")


@bot.event
async def on_ready():
    print("Bot is now online!")


if __name__ == '__main__':
    print("Loading bot...")
    bot.run(token)

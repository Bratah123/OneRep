from discord.ext import commands

token = ""

try:
    with open("token.txt") as f:  # Reading the first line of token.txt in this directory
        lines = f.read()
        token += lines.split('\n', 1)[0]
except Exception as e:
    print("Error trying to open token.txt, consider making a token.txt file?", e)

bot = commands.Bot(command_prefix='!')

print("Loading all commands via cogs...")


bot.load_extension("commands")


@bot.event
async def on_ready():
    print("Bot is now online!")


if __name__ == '__main__':
    print("Loading bot...")
    bot.run(token)

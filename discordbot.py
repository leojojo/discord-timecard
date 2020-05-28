import os, traceback, discord
import cogs.timecard
from discord.ext import commands

PREFIX = os.environ['DISCORD_PREFIX']
TOKEN = os.environ['DISCORD_BOT_TOKEN']
CONFIG = []
bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print(f'========== Logged in as {bot.user} ==========')
    cogs.timecard.setup(bot, CONFIG)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, 'original', error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

bot.run(TOKEN)

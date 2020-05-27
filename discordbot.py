import os, traceback
from datetime import datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='/')
TOKEN = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, 'original', error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def echo(ctx, *args):
    if len(args) > 0:
        await ctx.send(f'{datetime.now()}\t{ctx.author} gave me {len(args)} arguments: {str(args)}')
    else:
        await ctx.send('ほげ')

bot.run(TOKEN)

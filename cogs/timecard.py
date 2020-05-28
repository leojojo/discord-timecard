import os, re
from misc import get_google_sheet, sec2hourmin, humor
from datetime import datetime, timedelta
from discord.ext import commands

def setup(bot, config):
    bot.add_cog(Timecard(bot, config))

class Timecard(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(brief='返事をするよ/Echoes your words back')
    async def echo(self, ctx, *args):
        if len(args) > 0:
            await ctx.send(f'{datetime.now()}\t{ctx.author} gave me {len(args)} arguments: {str(args)}')
        else:
            await ctx.send('ほげ')
    
    @commands.command(brief='勤怠を記録するよ/Records timestamp')
    async def timecard(self, ctx):
        wks = get_google_sheet().sheet1
        author = ctx.author.display_name
        now = datetime.now()
    
        wks.append_row([author, str(now)])
    
        text = f'{humor()} {author} registered at **{now.strftime("%I:%M %p")}**'
        await ctx.send(text)
    
    @commands.command(brief='勤務時間を表示するよ/Displays how long you worked')
    async def worktime(self, ctx):
        wks = get_google_sheet().sheet1
        now = datetime.now()
        now_regex = re.compile(now.strftime('%Y-%m-%d'))
    
        # check the value of cell next to the c(date with cell), filter out if not the author
        # list of strings => list of strings that matches today's date
        author = ctx.author.display_name
        today_list = wks.findall(now_regex, in_column=2)
        filter_author = lambda c : wks.cell(c.row, 1).value == author
        my_today_list = list( filter(filter_author, today_list) )
        if len(my_today_list) == 0:
            await ctx.send('You seem *perfectly* ready to start working... *right* now. amirite?')
            return
    
        # get datetime value from each cell
        # list of strings that matches today => list of datetimes
        dt_format = '%Y-%m-%d %H:%M:%S.%f'
        timeify = lambda s : datetime.strptime(s.value, dt_format)
        times_today = list( map(timeify, my_today_list) )
        if len(times_today) % 2 == 1:
            times_today.append(now)
    
        # list datetimes => list of pairs of datetimes
        sessions = list( zip(times_today[::2], times_today[1::2]) )
        # list of pairs => list of timedelta of each pair
        sessions = list( map(lambda x : (x[1]-x[0]).total_seconds(), sessions) )
    
        # sum of timedeltas
        hours, minutes = sec2hourmin(sum(sessions))
        period = 'today'
        text = f'{author} worked **{hours} hours {minutes} minutes** {period}'
        print(text)
        await ctx.send(text)

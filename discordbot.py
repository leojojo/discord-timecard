import os, traceback, gspread, random
from datetime import datetime, timedelta
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
import re

prefix = os.environ['DISCORD_PREFIX']
TOKEN = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(command_prefix=prefix)

def secs2hoursmins(seconds):
    hours = int(seconds / 3600)
    minutes = int(seconds / 60) % 60
    return hours, minutes

def get_google_sheet():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credential_dict = {
            "type": "service_account",
            "project_id": os.environ['SHEET_PROJECT_ID'],
            "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
            "private_key": os.environ['SHEET_PRIVATE_KEY'].replace(r'\n', '\n'),
            "client_email": os.environ['SHEET_CLIENT_EMAIL'],
            "client_id": os.environ['SHEET_CLIENT_ID'],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
            }
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential_dict, scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_url(os.environ['SHEET_URL'])

def humor():
    entertain = ["Woo! :partying_face:", "Good Job :+1:", "Let's do this :muscle:"]
    return random.choice(entertain)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, 'original', error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command(brief='返事をするよ/Echoes your words back')
async def echo(ctx, *args):
    if len(args) > 0:
        await ctx.send(f'{datetime.now()}\t{ctx.author} gave me {len(args)} arguments: {str(args)}')
    else:
        await ctx.send('ほげ')

@bot.command(brief='勤怠を記録するよ/Records timestamp')
async def timecard(ctx):
    wks = get_google_sheet().sheet1
    author = str(ctx.author)
    now = datetime.now()

    wks.append_row([author, str(now)])

    text = f'{humor()} {author} registered at **{now.strftime("%I:%M %p")}**'
    await ctx.send(text)

@bot.command(brief='勤務時間を表示するよ/Displays how long you worked')
async def worktime(ctx):
    wks = get_google_sheet().sheet1
    now = datetime.now()
    now_regex = re.compile(str(now.strftime('%Y-%m-%d')))

    # check the value of cell next to the c(date with cell), filter out if not the author
    # list of strings => list of strings that matches today's date
    author = str(ctx.author)
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
    hours, minutes = secs2hoursmins(sum(sessions))
    period = 'today'
    text = f'{author} worked **{hours} hours {minutes} minutes** {period}'
    print(text)
    await ctx.send(text)

bot.run(TOKEN)

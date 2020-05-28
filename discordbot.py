import os, traceback
from datetime import datetime
from discord.ext import commands
import gspread, random
from oauth2client.service_account import ServiceAccountCredentials

prefix = os.environ['DISCORD_PREFIX']
TOKEN = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(command_prefix=prefix)

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

@bot.command(brief='返事をするよ')
async def echo(ctx, *args):
    if len(args) > 0:
        await ctx.send(f'{datetime.now()}\t{ctx.author} gave me {len(args)} arguments: {str(args)}')
    else:
        await ctx.send('ほげ')

@bot.command(brief='勤怠を記録するよ')
async def timecard(ctx):
    wks = get_google_sheet().sheet1
    author = str(ctx.author)
    now = datetime.now()

    wks.append_row([author, str(now)])

    text = f'{humor()} {author} registered at {now.strftime("%I:%M %p")}'
    await ctx.send(text)

bot.run(TOKEN)

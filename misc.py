import os, re, gspread, random
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

def parse_period(now, period='today'):
    # default is today
    datetime_str = now.strftime('%Y-%m-%d')
    period_out = 'today'

    if period == 'today':
        pass
    elif period == 'month':
        datetime_str = now.strftime('%Y-%m')
        period_out = 'this month'
    elif period == 'year':
        datetime_str = now.strftime('%Y')
        period_out = 'this year'
    else:
        search = re.search('^(\d{1,4})/(\d{1,2})(/(\d{1,2}))?$', period)
        if not search:
            pass
        else:
            # Y-m-d
            if search.group(4):
                datetime_str = f'{search.group(1)}-{search.group(2)}-{search.group(4)}'
                period_out = 'on ' + datetime_str
            # Y-m
            elif len(search.group(1)) == 4 and not search.group(4):
                datetime_str = f'{search.group(1)}-{search.group(2)}'
                period_out = 'on ' + datetime_str
            # m-d
            elif int(search.group(1)) <= 12 and int(search.group(2)) <= 31 and not search.group(4):
                datetime_str = f'{search.group(1)}-{search.group(2)}'
                period_out = 'on ' + datetime_str

    return re.compile(datetime_str), period_out

def sec2hourmin(seconds):
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


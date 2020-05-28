# Discord Timecard
## for users
```
/help
```
```
No Category:
  echo     返事をするよ/Echoes your words back
  help     Shows this message
  timecard 勤怠を記録するよ/Records timestamp
  worktime 勤務時間を表示するよ/Displays how long you worked

Type /help command for more info on a command.
You can also type /help category for more info on a category.
```

## setup
https://qiita.com/1ntegrale9/items/aa4b373e8895273875a8

## dev
```sh
cp .env.sample .env
vim .env
docker build -t discordbot .
docker run --env-file .env discordbot
```

## references
- GCP gspread
  - https://tanuhack.com/operate-spreadsheet
- Heroku gspread os.environ
  - https://qiita.com/a-r-i/items/bb8b8317840e3a87771a

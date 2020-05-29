# Discord Timecard
## for users
```
/help
```
```
Timecard:
  echo     返事をするよ/Echoes your words back
  timecard 勤怠を記録するよ/Records timestamp
  worktime 勤務時間を表示するよ/Displays how long you worked
No Category:
  help     Shows this message

Type /help command for more info on a command.
You can also type /help category for more info on a category.
```
```
/help worktime
```
```
/worktime <period_input>

勤務時間を表示するよ/Displays how long you worked
- specify a day: `/worktime today`, `worktime 5/29`, `worktime 2020/05/29`
- specify a month: `/worktime month`, `/worktime 2020/05`
- specify an year: `/worktime year`
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

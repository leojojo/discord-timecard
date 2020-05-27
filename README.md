# Discord Timecard

## setup
https://qiita.com/1ntegrale9/items/aa4b373e8895273875a8

## dev
```sh
cp .env.sample .env
vim .env
docker build -t discordbot .
docker run --env-file .env discordbot
```

FROM python:3.7-slim

ENV HOME=/app
WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "discordbot.py"]

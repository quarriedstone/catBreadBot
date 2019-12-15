FROM python:3

WORKDIR /bot
COPY bot /bot/bot
COPY main.py /bot
COPY requirements.txt /bot

ENV BOT_TOKEN = 1234

RUN pip install -r requirements.txt

CMD python3 main.py

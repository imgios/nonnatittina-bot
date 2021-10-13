FROM python:3

ARG TG_BOT_TOKEN

ENV TELEGRAM_BOT_TOKEN=$TG_BOT_TOKEN
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python bot.py

CMD ["python", "./bot.py"]

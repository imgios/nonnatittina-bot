FROM python:3.9-slim

# Python env variables
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

# Bot env variables
ENV TELEGRAM_BOT_TOKEN ${TELEGRAM_BOT_TOKEN}

RUN mkdir -p /telegram-bot
COPY __init.py__ /telegram-bot/
COPY bot.py /telegram-bot/
COPY requirements.txt /telegram-bot/
ADD utils /telegram-bot/

RUN pip3 install -r requirements.txt
RUN chmod +x /codebase/bot.py

CMD python3 /codebase/bot.py;
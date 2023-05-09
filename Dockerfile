
FROM python:3.9-slim
LABEL org.opencontainers.image.source="https://github.com/imgios/nonnatittina-bot"

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

ADD . /telegram-bot

WORKDIR /telegram-bot/
RUN pip3 install -r requirements.txt
RUN chmod +x bot.py

CMD python3 bot.py;
# 👵🏼 Nonna Tittina Bot

NonnaTittina ([👵🏼 @NonnaTittinaBot](https://t.me/nonnatittinabot)) is a Telegram Bot that allows you to fetch the restaurant menu from the [official website](https://nonnatittina.eu/) and reading it within the app.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python (used v3.9)
- pip
- Virtualenv
- Telegram Bot (use [BotFather](https://t.me/botfather))

### Installing

1. First of all, you need to clone the repository:

```bash
$ git clone https://github.com/imgios/nonnatittina-bot.git
$ cd nonnatittina-bot
```

2. Then create a virtualenv and activate it:

```bash
$ python -m venv venv
$ source venv/bin/activate # Linux
$ .\venv\Scripts\activate.bat # Windows
```

3. Install dependencies inside the virtualenv using pip:

```bash
$ pip install -r requirements.txt
```

4. Replace `os.environ['TELEGRAM_BOT_TOKEN']` with your Telegram Bot token or create an environment variable named `TELEGRAM_BOT_TOKEN` and use the bot token as value.
5. Start the bot:
```bash
$ python bot.py
```

Now you are ready to interact with it!

## Built With

* [Python](https://www.python.org/)
* [python-telegram-bot Wrapper](https://github.com/python-telegram-bot/python-telegram-bot)

## Contributors

<a href="https://github.com/imgios/nonnatittina-bot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=imgios/nonnatittina-bot" />
</a>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

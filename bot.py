#!/usr/bin/env python
# pylint: disable=C0116,W0613

"""
TO-DO: Bot description.
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Ciao {user.mention_markdown_v2()}, hai fame\?'
        + '\nCon questo bot puoi visionare il menù del Ristorante Nonna Tittina, presente al centro direzionale\! '
        + 'Per iniziare digita /menu oppure utilizza i bottoni presenti in basso\!',
    )

def menu_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /menu is issued."""
    keyboard = [
        [
            InlineKeyboardButton("🍕 Pizze", callback_data='pizza'),
            InlineKeyboardButton("🥗 Insalate", callback_data='salad'),
        ],
        [InlineKeyboardButton("🍱 Menù del giorno", callback_data='daily')],
    ]
    update.message.reply_text('I menù vengono presi direttamente dal sito web ufficiale del ristorante.'
        + '\nQuale menù intendi consultare?', reply_markup=InlineKeyboardMarkup(keyboard)
    )

def keyboard_callback(update: Update, context: CallbackContext) -> None:
    """Parses CallbackQuery and updates the message text when InlineKeyboard's buttons are pressed."""
    query = update.callback_query
    query.answer()

    keyboard = [
        [InlineKeyboardButton("Pagina successiva ➡", callback_data='page-' + query.data + '-1')],
    ]

    if 'pizza' in query.data:
        query.edit_message_text(text="Menù Pizze!", reply_markup=InlineKeyboardMarkup(keyboard))
    elif 'salad' in query.data:
        query.edit_message_text(text="Menù Insalate!", reply_markup=InlineKeyboardMarkup(keyboard))
    elif 'daily' in query.data:
        query.edit_message_text(text="Menù del giorno!", reply_markup=InlineKeyboardMarkup(keyboard))

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    #updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])
    updater = Updater('2031198008:AAFVQQ7ChoLhrslfdMU5Yrrpbw7QgUmgZno')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("menu", menu_command))
    dispatcher.add_handler(CallbackQueryHandler(keyboard_callback, pattern='^pizza|salad|daily$'))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
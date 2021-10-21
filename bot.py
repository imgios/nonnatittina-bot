#!/usr/bin/env python
# pylint: disable=C0116,W0613

"""
TO-DO: Bot description.
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from utils.scraper import retrieve_menu

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

def selection_keyboard_callback(update: Update, context: CallbackContext) -> None:
    """Parses CallbackQuery and updates the message text when InlineKeyboard's buttons are pressed."""
    query = update.callback_query
    query.answer()

    # Message text & inline keyboard
    message = ''
    keyboard = None

    # Retrieve menu
    menu = retrieve_menu(query.data)

    if (menu is none) or (len(menu) == 0):
        # Menu empty    
        keyboard = [
            [InlineKeyboardButton("🔙 Torna indietro", callback_data='menu')],
        ]
        message = "Purtroppo non sono riuscito ad ottenere il menu!\n\nRiprova più tardi, oppure consultalo online su https://nonnatittina.eu/menu-cdn/"
    else:
        # Menu not empty    
        keyboard = [
            [InlineKeyboardButton("Pagina successiva ➡", callback_data='page-' + query.data + '-2')],
        ]
        message = "Ecco a te il menù 😋\n\n"
        for course in menu[:5]:
            message += course['name'] + '\t\t' + course['price'] + '\n'
            if 'daily' not in query.data:
                message += course['desc'] + '\n\n' 

    query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))

def menu_keyboard_callback(update: Update, context: CallbackContext) -> None:
    """Parses CallbackQuery in order to provide a dynamic menu with pages."""
    query = update.callback_query
    query.answer()
    
    # query should be page-x-y where x is the menu requested and y is the page number
    query_splitted = query.data.split('-')
    page_number = int(query_splitted[2])

    # InlineKeyboard for pagination
    keyboard = [
        [
            InlineKeyboardButton("⬅ Pagina precedente", callback_data=f'page-{query_splitted[1]}-{page_number - 1}'),
            InlineKeyboardButton("Pagina successiva ➡", callback_data=f'page-{query_splitted[1]}-{page_number + 1}')
        ],
    ]

    # Print 5 courses at a time
    last_course_index = page_number * 5
    first_course_index = last_course_index - 5

    # Retrieve again the menu
    # This will be optimized adding persistent storage
    menu = retrieve_menu(query_splitted[1])

    # Check if this is the first page
    if page_number == 1:
        keyboard = [
            [InlineKeyboardButton("Pagina successiva ➡", callback_data=f'page-{query_splitted[1]}-{page_number + 1}')],
        ]
    
    # Check if this is the last page comparing last item index with list length
    if len(menu) - 1 < last_course_index:
        last_course_index = len(menu) - 1
        keyboard = [
            [InlineKeyboardButton("⬅ Pagina precedente", callback_data=f'page-{query_splitted[1]}-{page_number - 1}')],
        ]

    # Let's build the message to return to the user
    message = ''
    for course in menu[first_course_index:last_course_index]:
        message += course['name'] + '\t\t' + course['price'] + '\n'
        if 'daily' not in query_splitted[1]:
            message += course['desc'] + '\n\n'

    query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard))

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("menu", menu_command))
    dispatcher.add_handler(CallbackQueryHandler(selection_keyboard_callback, pattern='^pizza|salad|daily$'))
    dispatcher.add_handler(CallbackQueryHandler(menu_keyboard_callback, pattern='^page-[a-zA-Z]+-[0-9]+$'))

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
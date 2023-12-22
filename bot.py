import os

from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater


def echo(update, context):
    update.message.reply_text(update.message.text)


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()

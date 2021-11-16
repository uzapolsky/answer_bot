import logging
import os

from dotenv import load_dotenv
from telegram import ForceReply, Update
import telegram
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from dialogflow_answer import detect_intent_texts
from logger import TelegramLogsHandler


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def error(update, context):
    logger.exception('Telegram bot error')


def send_message(update: Update, context: CallbackContext) -> None:
    _, message = detect_intent_texts(
        os.getenv('PROJECT_ID'),
        update.message.from_user.id,
        update.message.text,
        'ru-RU'
    )
    update.message.reply_text(message)


def main() -> None:
    load_dotenv()
    log_bot = telegram.Bot(token=os.getenv('LOG_BOT_TOKEN'))
    
    logger.setLevel(logging.WARNING)
    logger.addHandler(TelegramLogsHandler(log_bot, os.getenv('LOG_CHAT_ID')))
    
    updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

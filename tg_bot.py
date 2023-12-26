import logging
import os

# from redis import ConnectionPool, StrictRedis
import redis
from dotenv import load_dotenv
from telegram import (Bot, InlineKeyboardMarkup, KeyboardButton,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from quiz import quiz_answers, quiz_questions

QUESTION, ANSWER = range(2)
QUESTION_ID = 0
logger = logging.getLogger(__name__)


def start(update, context):
    custom_keyboard = [['Новый вопрос', 'Сдаться'], 
                       ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.sendMessage(chat_id=update.message.chat_id, 
                            text="Привет! Я бот для викторин!",
                            reply_markup=reply_markup)
    return QUESTION


def handle_new_question_request(update, context):
    global QUESTION_ID
    r.set(update.effective_user.id, quiz_questions[f'Вопрос {QUESTION_ID}'])
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=r.get(update.effective_user.id))
    return ANSWER


def handle_solution_attempt(update, context):
    global QUESTION_ID
    if update.message.text.split('.')[0] in quiz_answers[f'Ответ {QUESTION_ID}']:
        context.bot.sendMessage(chat_id=update.message.chat_id,
                                text='Правильно!')
    else:
        context.bot.sendMessage(chat_id=update.message.chat_id,
                                text='Неправильно… Попробуешь ещё раз?')
        return ANSWER
    QUESTION_ID += 1
    return QUESTION


def handle_give_up(update, context):
    global QUESTION_ID
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=quiz_answers[f'Ответ {QUESTION_ID}'])
    QUESTION_ID += 1
    return handle_new_question_request(update, context)


def cancel(bot, update):
    global QUESTION_ID
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    QUESTION_ID = 0
    return ConversationHandler.END


if __name__ == '__main__':
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    load_dotenv()
    
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            QUESTION: [MessageHandler(Filters.regex('^Новый вопрос'),
                                      handle_new_question_request)],

            ANSWER: [MessageHandler(Filters.regex('^Сдаться'),
                                    handle_give_up),
                     MessageHandler(Filters.text & ~Filters.command,
                                    handle_solution_attempt),
                     ],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

    

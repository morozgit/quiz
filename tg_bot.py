import logging
import os

import redis
from dotenv import find_dotenv, load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from quiz import (create_parser, create_quiz_answers, create_quiz_questions,
                  parse_question_file)

QUESTION, ANSWER = range(2)
logger = logging.getLogger(__name__)


def start(update, context):
    context.chat_data['tg_question_id'] = 0
    custom_keyboard = [['Новый вопрос', 'Сдаться'], 
                       ['Мой счет']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.sendMessage(chat_id=update.message.chat_id, 
                            text="Привет! Я бот для викторин!",
                            reply_markup=reply_markup)
    return QUESTION


def handle_new_question_request(update, context, quiz_questions, r):
    question_text = quiz_questions[f'Вопрос {context.chat_data["tg_question_id"]}']
    r.set(update.effective_user.id, question_text)
    context.bot.sendMessage(chat_id=update.message.chat_id, text=question_text)

    return ANSWER


def handle_solution_attempt(update, context, quiz_answers, r):
    if update.message.text.split('.')[0] in quiz_answers[f'Ответ {context.chat_data["tg_question_id"]}']:
        context.bot.sendMessage(chat_id=update.message.chat_id,
                                text='Правильно!')
    else:
        context.bot.sendMessage(chat_id=update.message.chat_id,
                                text='Неправильно… Попробуешь ещё раз?')
        return ANSWER
    context.chat_data['tg_question_id'] += 1
    return QUESTION


def handle_give_up(update, context, quiz_questions, quiz_answers, r):
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=quiz_answers[f'Ответ {context.chat_data["tg_question_id"]}'])
    context.chat_data['tg_question_id'] += 1
    return handle_new_question_request(update, context, quiz_questions, r)


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    context.chat_data['tg_question_id'] = 0
    return ConversationHandler.END


def main():
    load_dotenv(find_dotenv())
    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")
    password = os.environ.get("REDIS_PASSWORD")
    r = redis.Redis(
        host=host,
        port=int(port),
        password=password,
        decode_responses=True
    )
    parser = create_parser()
    args = parser.parse_args()
    path = args.path
    file_contents = parse_question_file(path)
    quiz_questions = create_quiz_questions(file_contents)
    quiz_answers = create_quiz_answers(file_contents)
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            QUESTION: [MessageHandler(Filters.regex('^Новый вопрос'),
                                      lambda update, context: handle_new_question_request(update, context, quiz_questions, r))],

            ANSWER: [MessageHandler(Filters.regex('^Сдаться'),
                                    lambda update, context: handle_give_up(update, context, quiz_questions, quiz_answers, r)),
                     MessageHandler(Filters.text & ~Filters.command,
                                    lambda update, context: handle_solution_attempt(update, context, quiz_answers, r)),
                     ],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
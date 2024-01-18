import os
import random

import redis
import vk_api as vk
from dotenv import find_dotenv, load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from quiz import QuestionsLibrary


def discussion_with_bot(event, vk_api):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.SECONDARY)

    if event.text == 'Начать':
        text = 'Привет! Я бот для викторин!'
    elif event.text == 'Новый вопрос':
        text = handle_new_question_request(event, vk_api)
    elif event.text == 'Сдаться':
        text = handle_give_up(event, vk_api)
    else:
        text = handle_solution_attempt(event, vk_api)

    vk_api.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message=text,
    )


def handle_new_question_request(event, vk_api):
    r.set(event.user_id, quiz_questions[f'Вопрос {library.get_question_count()}'])
    return r.get(event.user_id)


def handle_solution_attempt(event, vk_api):
    global QUESTION_ID
    if event.text.split('.')[0] in quiz_answers[f'Ответ {library.get_question_count()}']:
        library.set_question_count(1)
        return 'Правильно!'
    else:
        return 'Неправильно… Попробуешь ещё раз?'


def handle_give_up(update, context):
    vk_api.messages.send(
        user_id=event.user_id,
        message=quiz_answers[f'Ответ {library.get_question_count()}'],
        random_id=random.randint(1, 1000)
    )
    library.set_question_count(1)
    return handle_new_question_request(update, context)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    vk_token = os.environ.get("VK_TOKEN")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    library = QuestionsLibrary()
    library.read_file()
    quiz_questions = library.create_quiz_questions()
    quiz_answers = library.create_quiz_answers()

    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")
    password = os.environ.get("REDIS_PASSWORD")
    r = redis.Redis(
        host=host,
        port=int(port),
        password=password,
        decode_responses=True
    )

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            discussion_with_bot(event, vk_api)

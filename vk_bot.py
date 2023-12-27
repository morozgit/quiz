import os
import random

import redis
import vk_api as vk
from dotenv import find_dotenv, load_dotenv
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from quiz import quiz_answers, quiz_questions

QUESTION_ID = 0


def discussion_with_bot(event, vk_api):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.SECONDARY)

    if event.text == 'Начать':
        text = 'Привет! Да начнётся викторина!'
        # keyboard = keyboard.get_keyboard(),
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
    global QUESTION_ID
    r.set(event.user_id, quiz_questions[f'Вопрос {QUESTION_ID}'])
    return r.get(event.user_id)


def handle_solution_attempt(event, vk_api):
    global QUESTION_ID
    if event.text.split('.')[0] in quiz_answers[f'Ответ {QUESTION_ID}']:
        QUESTION_ID += 1
        return 'Правильно!'
    else:
        return 'Неправильно… Попробуешь ещё раз?'


def handle_give_up(update, context):
    global QUESTION_ID
    vk_api.messages.send(
        user_id=event.user_id,
        message=quiz_answers[f'Ответ {QUESTION_ID}'],
        random_id=random.randint(1, 1000)
    )
    QUESTION_ID += 1
    return handle_new_question_request(update, context)


if __name__ == '__main__':
    r = redis.Redis(
        host='redis-10444.c327.europe-west1-2.gce.cloud.redislabs.com',
        port=10444,
        password='WdsJFjUOsMSF7foxK7rUPTZitodsuSfW',
        decode_responses=True
    )
    load_dotenv(find_dotenv())
    vk_token = os.environ.get("VK_TOKEN")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            discussion_with_bot(event, vk_api)

import argparse
import os


def create_quiz_questions():
    for file_content in file_contents:
        rounds = file_content.split('\n\n')
        questions = [round[10:].strip(':') for round in rounds if round.strip().startswith('Вопрос')]
        for id_question, question in enumerate(questions):
            quiz_questions[f'Вопрос {id_question}'] = question
    return quiz_questions


def create_quiz_answers():
    for file_content in file_contents:
        rounds = file_content.split('\n\n')
        answers = [round.split('\n')[1] for round in rounds if round.split('\n')[0].startswith('Ответ')]
        for id_answer, answer in enumerate(answers):
            quiz_answers[f'Ответ {id_answer}'] = answer
    return quiz_answers


def count_question_id(num):
    question_id += num


def get_question_id():
    return question_id


def reset_question_id():
    question_id = 0


if __name__ == '__main__':
    question_id = 0
    file_contents = []
    quiz_questions = {}
    quiz_answers = {}
    parser = argparse.ArgumentParser(
        description='Скрипт парсит вопросы'
    )
    parser.add_argument('path', help='Путь до вопросов')
    args = parser.parse_args()
    for filename in os.listdir(args.path):
        with open(f'{args.path}/' + filename, 'r', encoding='KOI8-R') as file:
            file_contents.append(file.read())


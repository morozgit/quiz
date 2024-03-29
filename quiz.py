import argparse
import os


def create_quiz_questions(file_contents):
    quiz_questions = {}
    for file_content in file_contents:
        rounds = file_content.split('\n\n')
        questions = [round[10:].strip(':') for round in rounds if round.strip().startswith('Вопрос')]
    for question_id, question in enumerate(questions):
        quiz_questions[f'Вопрос {question_id}'] = question
    return quiz_questions


def create_quiz_answers(file_contents):
    quiz_answers = {}
    for file_content in file_contents:
        rounds = file_content.split('\n\n')
        answers = [round.split('\n')[1] for round in rounds if round.split('\n')[0].startswith('Ответ')]
        for answer_id, answer in enumerate(answers):
            quiz_answers[f'Ответ {answer_id}'] = answer
    return quiz_answers


def parse_question_file(path='./questions'):
    file_contents = []
    for filename in os.listdir(path):
        with open(f'{path}/' + filename, 'r', encoding='KOI8-R') as file:
            file_contents.append(file.read())
    return file_contents


def create_parser():
    parser = argparse.ArgumentParser(
        description='Скрипт парсит вопросы'
    )
    parser.add_argument('--path', help='Путь до вопросов', default='./questions')
    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    path = args.path
    file_contents = parse_question_file(path)
    quiz_questions = create_quiz_questions(file_contents)
    quiz_answers = create_quiz_answers(file_contents)


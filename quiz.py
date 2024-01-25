import argparse
import os


def create_quiz_questions(file_contents):
    quiz_questions = {}
    for file_content in file_contents:
        rounds = file_content.split('\n\n')
        questions = [round[10:].strip(':') for round in rounds if round.strip().startswith('Вопрос')]
    for id_question, question in enumerate(questions):
        quiz_questions[f'Вопрос {id_question}'] = question
    return quiz_questions


def create_quiz_answers(file_contents):
    quiz_answers = {}
    for file_content in file_contents:
        rounds = file_content.split('\n\n')
        answers = [round.split('\n')[1] for round in rounds if round.split('\n')[0].startswith('Ответ')]
        for id_answer, answer in enumerate(answers):
            quiz_answers[f'Ответ {id_answer}'] = answer
    return quiz_answers


def parse_question_file():
    file_contents = []
    parser = argparse.ArgumentParser(
        description='Скрипт парсит вопросы'
    )
    parser.add_argument('path', help='Путь до вопросов')
    args = parser.parse_args()
    for filename in os.listdir(args.path):
        with open(f'{args.path}/' + filename, 'r', encoding='KOI8-R') as file:
            file_contents.append(file.read())
    return file_contents


if __name__ == '__main__':
    file_contents = parse_question_file()
    quiz_questions = create_quiz_questions(file_contents)
    quiz_answers = create_quiz_answers(file_contents)


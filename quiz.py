import argparse
import os


class QuestionsLibrary:
    def __init__(self):
        self.file_contents = []
        self.quiz_questions = {}
        self.quiz_answers = {}
        self.question_id = 0

    def read_file(self):
        parser = argparse.ArgumentParser(
            description='Скрипт парсит вопросы'
        )
        parser.add_argument('path', help='Путь до вопросов')
        args = parser.parse_args()
        for filename in os.listdir(args.path):
            with open(f'{args.path}/' + filename, 'r', encoding='KOI8-R') as file:
                self.file_contents.append(file.read())
    
    def create_quiz_questions(self):
        for self.file_content in self.file_contents:
            rounds = self.file_content.split('\n\n')
            questions = [round[10:].strip(':') for round in rounds if round.strip().startswith('Вопрос')]
            for id_question, question in enumerate(questions):
                self.quiz_questions[f'Вопрос {id_question}'] = question
        return self.quiz_questions
    
    def create_quiz_answers(self):
        for self.file_content in self.file_contents:
            rounds = self.file_content.split('\n\n')
            answers = [round.split('\n')[1] for round in rounds if round.split('\n')[0].startswith('Ответ')]
            for id_answer, answer in enumerate(answers):
                self.quiz_answers[f'Ответ {id_answer}'] = answer
        return self.quiz_answers

    def set_question_count(self, num):
        self.question_id += num

    def get_question_count(self):
        return self.question_id

    def reset_question_count(self):
        self.question_id = 0

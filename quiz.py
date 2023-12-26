with open("questions/1vs1200.txt", "r", encoding="KOI8-R") as my_file:
    file_contents = my_file.read()
quiz_questions = {}
quiz_answers = {}

rounds = file_contents.split('\n\n')
questions = [round[10:].strip(':') for round in rounds if round.strip().startswith('Вопрос')]
for id, question in enumerate(questions):
    quiz_questions[f'Вопрос {id}'] = question

answers = [round.split('\n')[1] for round in rounds if round.split('\n')[0].startswith('Ответ')]
for id, answer in enumerate(answers):
    quiz_answers[f'Ответ {id}'] = answer

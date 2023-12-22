with open("questions/1vs1200.txt", "r", encoding="KOI8-R") as my_file:
    file_contents = my_file.read()
questions = {}
answers = {}
rounds = file_contents.split('\n\n')
for id, round in enumerate(rounds):
    if round.strip().startswith('Вопрос'):
        questions[round[:9].strip(':'), id] = round[10:].strip(':')
for id, round in enumerate(rounds):
    if round.split('\n')[0].startswith('Ответ'):
        answers[round[:6].strip(':'), id] = round.split('\n')[1]

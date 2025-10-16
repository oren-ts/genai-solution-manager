"""
Übung 4.4.Ü.01
Task (DE): Entwickle ein Python-Programm, das die Rolle eines einfachen Quizspiels übernimmt.\n
           Das Spiel soll aus drei Fragen bestehen, die nacheinander gestellt werden. Für jede Frage\n
           gibt es drei Antwortmöglichkeiten (a, b, c), von denen genau eine richtig ist. Nachdem der\n
           Spieler alle Fragen beantwortet hat, soll das Programm die Anzahl der richtig beantworteten\n
           Fragen ausgeben und eine Rückmeldung geben. Verwende für jede Frage eine if-elif-else-Struktur,\n
           um zu überprüfen, ob die Antwort des Spielers richtig oder falsch ist. Nutze zudem eine while-Schleife,\n
           um sicherzustellen, dass das Spiel nur fortgesetzt wird, wenn der Spieler eine gültige Antwort\n
           (a, b, oder c) eingegeben hat. Wenn eine ungültige Eingabe erfolgt, soll der Spieler erneut zur\n
           Eingabe aufgefordert werden, bis eine gültige Antwort gegeben wird.
Task (EN): Develop a Python program that acts as a simple quiz game. The game should consist of three questions\n
           presented one after the other. Each question should have three answer choices (a, b, c), with exactly\n
           one correct answer. After the player has answered all the questions, the program should display the\n
           number of correctly answered questions and provide feedback. Use an if-elif-else structure for each\n
           question to check whether the player's answer is correct or incorrect. Also, use a while loop to ensure\n
           that the game only continues if the player enters a valid answer (a, b, or c). If an invalid input is given,\n
           the player should be prompted again until a valid answer is provided.
Notes: <what you learned / edge cases>
"""

print('Welcome to our quiz')
score = 0
questions = ['What is the capital of Germany?', 'What is the capital of England?', 'What is the capital of Italy?']
options = ['a.London b.Rome c.Berlin', 'a.Paris b.London c.Amsterdam', 'a.Rome b.Warsaw c.Prague']
answers = {'a', 'b', 'c'}

# question 1
question_1 = print(questions[0] + ' ' + options[0])
answer1 = input('Please enter your answer a/b/c: ')
while answer1 not in answers:
    answer1 = input('Please enter your answer a/b/c: ')

if answer1 == 'c':
    score += 1
elif answer1 == 'b':
    print('incorrect')
else:
    print('incorrect')

# question 2
question_2 = print(questions[1] + ' ' + options[1])
answer2 = input('Please enter your answer a/b/c: ')
while answer2 not in answers:
    answer2 = input('Please enter your answer a/b/c: ')

if answer2 == 'b':
    score += 1
elif answer2 == 'a':
    print('incorrect')
else:
    print('incorrect')

# question 3
question_3 = print(questions[2] + ' ' + options[2])
answer3 = input('Please enter your answer a/b/c: ')
while answer3 not in answers:
    answer3 = input('Please enter your answer a/b/c: ')

if answer3 == 'a':
    score += 1
elif answer3 == 'b':
    print('incorrect')
else:
    print('incorrect')

# score and feedback
if score == 3:
    print(f'You answered {score}/3 correctly. Excellent.')
elif score == 2:
    print(f'You answered {score}/3 correctly. Good Job.')
elif score == 1:
    print(f'You answered {score}/3 correctly. Keep Practicing.')
else:
    print(f'You answered {score}/3 correctly. Try again!')
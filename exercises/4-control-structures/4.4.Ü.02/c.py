"""
Übung 4.4.Ü.02/c
Task (DE): Füge einen Kommentar über jede Kontrollstruktur hinzu, um zu erklären, was sie tut.
Task (EN): Add a comment above each control structure to explain what it does.
Notes: <what you learned / edge cases>
"""

# Define emotions list and get clean input
emotions = ['happy', 'sad', 'tired']
mood = input(f'How are you feeling today ({emotions[0]}/{emotions[1]}/{emotions[2]})? ').lower().strip()

# Provide feedback based on input
if mood == emotions[0]:
    print("It's great to hear that you're happy!")
elif mood == emotions[1]:
    print("I'm sorry to hear that you're sad. I hope you feel better soon!")
elif mood == emotions[2]:
    print('Maybe you should get some rest. Rest is important.')
else:
    print('I am not familiar with this emotion.')
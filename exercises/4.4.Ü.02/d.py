"""
Übung 4.4.Ü.02/d
Task (DE): Verwende eine while-Schleife, um den Benutzer zu fragen, ob er das Programm beenden möchte\n
           ("Ja" oder "Nein"). Wenn der Benutzer "Nein" eingibt, wiederhole die Schritte a) bis c). 
Task (EN): Use a while loop to ask the user whether they want to exit the program ("Yes" or "No").\n
           If the user enters "No", repeat steps a) through c).
Notes: <what you learned / edge cases>
"""

# Define emotions list and loop-control variable 
emotions = ['happy', 'sad', 'tired']
quit_input = 'no'

# Repeat the mood prompt until the user confirms they want to quit by entering an affirmative response
while quit_input != 'yes':
    # Read and normalize the user's mood input (lowercase and trim spaces) so comparisons are consistent
    mood = input(f'How are you feeling today ({emotions[0]}/{emotions[1]}/{emotions[2]})? ').lower().strip()
    # Select and print a response that matches the user's normalized mood; use else for unknown moods
    if mood == emotions[0]:
        print("It's great to hear that you're happy!")
    elif mood == emotions[1]:
        print("I'm sorry to hear that you're sad. I hope you feel better soon!")
    elif mood == emotions[2]:
        print('Maybe you should get some rest. Rest is important.')
    else:
        print('I am not familiar with this emotion.')
    quit_input = input('Do you want to quit yes/no? ').lower().strip()
"""
Übung 4.4.Ü.02/b
Task (DE): Überprüfe die Eingabe des Benutzers. Wenn der Benutzer "glücklich" eingibt, soll das Programm ausgeben:\n
           "Es ist toll zu hören, dass du glücklich bist!". Wenn der Benutzer "traurig" eingibt, soll das Programm\n
           ausgeben: "Es tut mir leid zu hören, dass du traurig bist. Ich hoffe, es geht dir bald besser!".\n
           Bei der Eingabe von "müde" soll das Programm ausgeben: "Vielleicht solltest du dich etwas ausruhen.\n
           Ruhe ist wichtig.". Für alle anderen Eingaben soll das Programm ausgeben: "Interessant! Ich weiß nicht viel\n
           über diese Stimmung."
Task (EN): Check the user's input. If the user enters "happy", the program should output: "It's great to hear that\n
           you're happy!" If the user enters "sad", the program should output: "I'm sorry to hear that you're sad.\n
           I hope you feel better soon!" If the user enters "tired", the program should output: "Maybe you should get\n
           some rest. Rest is important." For all other inputs, the program should output: "Interesting! I don't know\n
           much about that mood."
Notes: <what you learned / edge cases>
"""

emotions = ['happy', 'sad', 'tired']
mood = input(f'How are you feeling today ({emotions[0]}/{emotions[1]}/{emotions[2]})? ').lower().strip()

if mood == emotions[0]:
    print("It's great to hear that you're happy!")
elif mood == emotions[1]:
    print("I'm sorry to hear that you're sad. I hope you feel better soon!")
elif mood == emotions[2]:
    print('Maybe you should get some rest. Rest is important.')
else:
    print('I am not familiar with this emotion.')
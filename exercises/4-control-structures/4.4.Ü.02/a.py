"""
Übung 4.4.Ü.02/a
Task (DE): Frage den Benutzer nach seiner aktuellen Stimmung (z.B. "glücklich", "traurig", "müde").\n
           Speichere die Eingabe in einer Variablen
Task (EN): Ask the user about their current mood (e.g., "happy", "sad", "tired"). Store the input in a variable.
Notes: <what you learned / edge cases>
"""

emotions = ['happy', 'sad', 'tired']
mood = input(f'How are you feeling today ({emotions[0]}/{emotions[1]}/{emotions[2]})? ')
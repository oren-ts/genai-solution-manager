"""
Übung 4.1.A.01/c
Task (DE): Erstelle eine Funktion, die eine gegebene Zeichenkette in eine ganze Zahl umwandelt (Typecasting).
Task (EN): Create a function that converts a given string into an integer (typecasting).
Notes: <what you learned / edge cases>
"""

def string_to_integer(string):
    integer = int(string)
    print(f"The converted string is: {integer}")
    return integer

string_to_integer('42')
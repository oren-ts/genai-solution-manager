"""
Übung 3.6.Ü.01/d
Task (DE): Finde und korrigiere die Fehler im folgenden Python-Skript. Kommentiere, was falsch war und wie du es behoben hast.
Task (EN): Find and correct the errors in the following Python script. Comment on what was wrong and how you fixed it.
Notes: <what you learned / edge cases>
"""
# Original erroneous code:
print("Willkommen zum Fehlerfindungs-Quiz!")
zahl1 = input("Bitte gib eine Zahl ein: ")
zahl2 = input("Bitte gib eine andere Zahl ein: ")
ergebnis = zahl1 + zahl2
print("Das Ergebnis der Addition ist: ", ergebnis) # expected a number but got a string

# Corrections:
# 1. The input function returns a string, so we need to convert the inputs to integers or floats before performing arithmetic operations.
print("Willkommen zum Fehlerfindungs-Quiz!")
zahl1 = float(input("Bitte gib eine Zahl ein: "))         # Convert input to float
zahl2 = float(input("Bitte gib eine andere Zahl ein: "))  # Convert input to float
ergebnis = zahl1 + zahl2                                  # Now this will correctly add the two numbers
print("Das Ergebnis der Addition ist: ", ergebnis)        # This will now correctly display the sum of the two numbers
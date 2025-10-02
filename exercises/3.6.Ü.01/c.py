"""
Übung 3.6.Ü.01/c
Task (DE): Definiere ein Python-Skript, das ein einfaches Beispiel für das EVA-Prinzip demonstriert: Es soll vom Benutzer zwei Zahlen einlesen (Eingabe), diese multiplizieren (Verarbeitung) und das Ergebnis ausgeben (Ausgabe). Kommentiere jeden Schritt im Skript.
Task (EN): Define a Python script that demonstrates a simple example of the EVA principle: It should read two numbers from the user (Input), multiply them (Processing), and output the result (Output). Comment each step in the script.
Notes: <what you learned / edge cases>
"""

# Input
num1 = float(input("Enter the first number: "))  # Prompting the user to enter the first number and converting it to float
num2 = float(input("Enter the second number: ")) # Prompting the user to enter the second number and converting it to float

# Process
result = num1 * num2                             # Multiplying the two numbers

# Output
print(f"The result of multiplying {num1} and {num2} is {result}")
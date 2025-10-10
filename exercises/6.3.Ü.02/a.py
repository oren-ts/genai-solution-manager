"""
Übung 6.3.Ü.02
Task (DE): Erstelle ein Python-Programm, das folgende Aufgaben erfüllt:
           a) Importiere das Modul random und verwende eine Funktion aus diesem Modul, um eine Zufallszahl
           zwischen 1 und 10 zu generieren. Speichere diese Zahl in einer Variablen.
           b) Definiere eine Funktion namens berechne_quadrat, die einen Parameter nimmt, dessen Quadrat berechnet
           und das Ergebnis zurückgibt.
           c) Verwende eine if-Kontrollstruktur, um zu überprüfen, ob die generierte Zufallszahl größer als 5 ist.
           Falls ja, rufe die Funktion berechne_quadrat mit der Zufallszahl als Argument auf und gib das Ergebnis aus.
           Falls nein, gib eine Nachricht aus, die besagt, dass die Zahl kleiner oder gleich 5 ist.
           d) Implementiere eine Schleife, die von 1 bis zur generierten Zufallszahl läuft und dabei jedes Mal die aktuelle Zahl ausgibt.
Task (EN): Create a Python program that performs the following tasks:
           a) Import the random module and use a function from this module to generate a random number between 1 and 10. Store this number in a variable.
           b) Define a function named calculate_square that takes a parameter, calculates its square, and returns the result.
           c) Use an if control structure to check if the generated random number is greater than 5. If yes, call the function
           calculate_square with the random number as an argument and output the result. If no, output a message stating that the number is smaller or equal to 5.
           d) Implement a loop that runs from 1 to the generated random number and outputs the current number each time.
"""

import random  # Import the random module for generating random numbers


# Generate a random integer between 1 and 10 (inclusive)
random_num = random.randint(1, 10)
print(f"Number selected randomly: {random_num}")


def calculate_square(number: int) -> int:
    """Calculate the square of a given number."""
    return number**2  # Use exponentiation for squaring


# Check if the random number is greater than 5
if random_num > 5:
    # Compute and print the square if condition is met
    print(f"The square of {random_num} is: {calculate_square(random_num)}")
else:
    print(
        f"The number {random_num} is less than or equal to 5."
    )  # Fallback message for numbers <= 5


# Loop from 1 to random_num, printing the current iteration value each time
for i in range(1, random_num + 1):
    print(f"Iteration {i}: {i}")

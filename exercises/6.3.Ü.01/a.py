"""
Übung 6.3.Ü.01
Task (DE): Erstelle ein Python-Programm, das folgende Aufgaben erfüllt:
           a) Importiere das Modul random und das Modul math.
           b) Definiere eine Variable zahl, die eine zufällige Ganzzahl zwischen 1 und 100 speichert.
           c) Schreibe eine Funktion quadratwurzel, die die Quadratwurzel einer Zahl berechnet und zurückgibt.
           Verwende dafür eine Funktion aus dem Modul math.
           d) Verwende eine if-else-Kontrollstruktur, um zu überprüfen, ob die zahl größer als 50 ist. Wenn ja,
           rufe die Funktion quadratwurzel mit zahl als Argument auf und drucke das Ergebnis aus. Andernfalls drucke "Zahl ist 50 oder kleiner".
           e) Erstelle eine for-Schleife, die Zahlen von 1 bis 5 durchläuft, und für jede Zahl die Funktion quadratwurzel aufruft und das Ergebnis ausdruckt.
Task (EN): Create a Python program that fulfills the following tasks:
           a) Import the random module and the math module.
           b) Define a variable zahl (number) that stores a random integer between 1 and 100.
           c) Write a function quadratwurzel (square root) that calculates and returns the square root of a number.
           Use a function from the math module for this.
           d) Use an if-else control structure to check if zahl is greater than 50. If yes, call the function
           quadratwurzel with zahl as an argument and print the result. Otherwise print "Number is 50 or smaller".
           e) Create a for loop that iterates through numbers from 1 to 5, and for each number calls the function quadratwurzel and prints the result.
"""

# Import required modules for mathematical operations and random number generation
import math
import random


# Generate a random integer between 1 and 100 (inclusive)
random_num = random.randint(1, 100)
print(random_num)


def square_root(number: int) -> float:
    """Calculate and return the square root of a given number.

    Args:
        number: The number to calculate the square root of

    Returns:
        The square root of the input number
    """
    return math.sqrt(number)


# Check if the random number is greater than 50 and handle accordingly
if random_num > 50:
    print(
        f"The square root of the number {random_num} is: {square_root(random_num):.2f}"
    )
else:
    print("The number is 50 or smaller")


# Calculate and display square roots for numbers 1 through 5
for i in range(1, 6):
    print(f"The square root of iteration {i} is: {square_root(i):.2f}")

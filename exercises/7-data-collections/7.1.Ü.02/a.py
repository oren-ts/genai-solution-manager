"""
Übung 7.1.Ü.02
Task (DE): Entwickle ein Python-Skript, das folgende Anforderungen erfüllt:
           a) Importiere das Modul random und das Modul math.
           b) Erstelle eine Funktion namens erzeuge_zufallszahlen_liste, die zwei Parameter akzeptiert:
           anzahl (die Anzahl der Zufallszahlen in der Liste) und max_wert (der maximale Wert einer Zufallszahl).
           Die Funktion soll eine Liste von anzahl Zufallszahlen generieren, wobei jede Zufallszahl zwischen
           1 und max_wert (inklusive) liegt. Nutze die Funktion randint aus dem Modul random zur Generierung der Zufallszahlen.
           c) Erstelle eine Funktion namens berechne_durchschnitt, die eine Liste von Zahlen als Parameter akzeptiert
           und den Durchschnittswert dieser Zahlen zurückgibt.
           d) Erstelle eine Funktion namens sortiere_und_teile, die eine Liste von Zahlen akzeptiert und die Liste in
           zwei Hälften teilt. Die Funktion soll zunächst die Liste aufsteigend sortieren. Dann soll die Funktion zwei
           Listen zurückgeben: die erste Hälfte und die zweite Hälfte der ursprünglichen Liste. Wenn die Liste eine
           ungerade Anzahl von Elementen hat, soll das mittlere Element zur ersten Hälfte hinzugefügt werden.
           e) Verwende die Funktion erzeuge_zufallszahlen_liste, um eine Liste mit 10 Zufallszahlen zu erzeugen, wobei max_wert 100 ist.
           f) Gib die erzeugte Liste aus.
           g) Berechne und gib den Durchschnittswert der Zufallszahlenliste mit der Funktion berechne_durchschnitt aus.
           h) Verwende die Funktion sortiere_und_teile, um die Zufallszahlenliste zu sortieren und in zwei Hälften zu teilen.
           Gib beide Hälften aus.
Task (EN): Develop a Python script that meets the following requirements:
           a) Import the random module and the math module.
           b) Create a function named generate_random_numbers_list that accepts two parameters:
           number (the number of random numbers in the list) and max_value (the maximum value of a random number).
           The function should generate a list of random numbers, where each random number is between
           1 and max_value (inclusive). Use the randint function from the random module to generate the random numbers.
           c) Create a function named calculate_average that accepts a list of numbers as a parameter
           and returns the average value of these numbers.
           d) Create a function named sort_and_split that accepts a list of numbers and splits the list into
           two halves. The function should first sort the list in ascending order. Then the function should return two
           lists: the first half and the second half of the original list. If the list has an odd number of elements,
           the middle element should be added to the first half.
           e) Use the function generate_random_numbers_list to generate a list with 10 random numbers, where max_value is 100.
           f) Print the generated list.
           g) Calculate and print the average value of the random numbers list using the function calculate_average.
           h) Use the function sort_and_split to sort the random numbers list and split it into two halves. Print both halves.
"""

import random
import math


def generate_random_numbers_list(number, max_value):
    return [random.randint(1, max_value) for _ in range(number)]


def calculate_average(numbers_list):
    return sum(numbers_list) / len(numbers_list) if numbers_list else 0


def sort_and_split(numbers_list):
    numbers_list.sort()
    half = (len(numbers_list) + 1) // 2
    return numbers_list[:half], numbers_list[half:]


# Generate and print a list of 10 random numbers with max value 100
random_list = generate_random_numbers_list(10, 100)
print(f"Random list: {random_list}")


# Calculate and print the average
average = calculate_average(random_list)
print(f"Random list average: {average}")


# Split and print the halves
first_half, second_half = sort_and_split(random_list)
print(f"Random list first half {first_half}")
print(f"Random list second half {second_half}")

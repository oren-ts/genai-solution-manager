"""
Transferaufgabe 7.3.A.01
Task (DE): Entwickle ein Python-Programm, das folgende Funktionalitäten umfasst:
           a) Importiere das Modul random und das Modul math. Verwende aus dem Modul random die Funktion randint
           und aus math die Funktion sqrt.
           b) Erstelle eine Funktion erzeuge_zufallszahlen_liste(n), die eine Liste mit n zufälligen ganzen
           Zahlen zwischen 1 und 100 zurückgibt.
           c) Erstelle eine Funktion berechne_wurzeln(liste), die für jede Zahl in der übergebenen Liste
           die Quadratwurzel berechnet und die Wurzeln in einer neuen Liste speichert. Gib diese Liste zurück.
           d) Erstelle eine Funktion sortiere_und_erzeuge_tupel(liste), die die Liste von Quadratwurzeln aufsteigend
           sortiert und ein Tupel aus (Originalzahl, Quadratwurzel) für jede Zahl in der ursprünglichen Liste erzeugt.
           Speichere diese Tupel in einer Liste und gib sie zurück.
           e) Erstelle eine Funktion erstelle_dictionary(tupel_liste), die ein Dictionary erstellt, wobei der
           Schlüssel die Originalzahl und der Wert die Quadratwurzel ist. Gib dieses Dictionary zurück.
           f) Verwende alle oben erstellten Funktionen in einer Hauptfunktion main(), um eine Liste mit 10
           zufälligen Zahlen zu erzeugen, die Quadratwurzeln zu berechnen, die Liste zu sortieren,
           das Tupel zu erstellen und schließlich das Dictionary zu erstellen und auszugeben.
           g) Gib am Ende des Programms das erstellte Dictionary aus.
Task (EN): Develop a Python program that encompasses the following functionalities:
           a) Import the `random` module and the `math` module. Use the `randint` function from the
           `random` module and the `sqrt` function from `math`.
           b) Create a function `erzeuge_zufallszahlen_liste(n)` that returns a list containing `n` random
           integers between 1 and 100.
           c) Create a function `berechne_wurzeln(liste)` that calculates the square root for each number
           in the provided list and stores the roots in a new list. Return this list.
           d) Create a function `sortiere_und_erzeuge_tupel(liste)` that sorts the list of square roots
           in ascending order and, for each number in the original list, creates a tuple of
           (original number, square root). Store these tuples in a list and return it.
           e) Create a function `erstelle_dictionary(tupel_liste)` that creates a dictionary with the original
           number as the key and the square root as the value. Return this dictionary.
           f) Use all the functions created above in a main function `main()`, to create a list of 10 random numbers,
           calculate their square roots, sort the list, create the tuples, and finally create and output the dictionary.
           g) At the end of the program, output the created dictionary.
"""

from random import randint
from math import sqrt


def generate_random_numbers_list(n):
    """Generates a list of n random integers between 1 and 100."""
    return [randint(1, 100) for _ in range(n)]


def calculate_roots(list):
    """Calculates the square root for each number in the list."""
    return [sqrt(list[i]) for i in range(len(list))]  # Iterate directly over items


def sort_and_create_tuples(list):
    """Creates tuples of (original, square root) and sorts by square root."""
    tuple_list = [(number, sqrt(number)) for number in list]
    return sorted(tuple_list, key=lambda x: x[1])


def create_dictionary(tuple_list):
    """Creates a dictionary with original numbers as keys and roots as values."""
    return {i[0]: i[1] for i in tuple_list}


def main():
    """Main function to run the program and output the dictionary."""
    random_numbers_list = generate_random_numbers_list(10)
    sqrt_numbers_list = calculate_roots(random_numbers_list)
    tuple_list = sort_and_create_tuples(random_numbers_list)
    dictionary = create_dictionary(tuple_list)
    print(dictionary)


main()

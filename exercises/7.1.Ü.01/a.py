"""
Übung 7.1.Ü.01
Task (DE): Entwickele ein Python-Programm, das folgende Aufgaben erfüllt:
           a) Importiere das Modul random und verwende es, um eine Liste von 10 zufälligen Ganzzahlen zwischen 1 und 100 zu erzeugen.
           b) Erstelle eine Funktion namens sortiere_und_zähle, die eine Liste von Zahlen als Argument nimmt. Die Funktion soll die
           Liste aufsteigend sortieren und die Anzahl der Elemente in der Liste zurückgeben.
           c) Erstelle eine weitere Liste, die Tupel aus den ursprünglichen zufälligen Zahlen und dem Quadrat jeder Zahl enthält
           (z.B. [(Zahl, Quadrat der Zahl), ...]).
           d) Verwende eine Schleife, um über die Liste der Tupel zu iterieren, und drucke für jedes Tupel eine formatierte Zeichenkette aus,
           die besagt: "Die Zahl X hat das Quadrat Y".
           e) Schreibe eine Kontrollstruktur, die prüft, ob die Anzahl der Elemente in der sortierten Liste größer als 5 ist. Wenn ja,
           drucke "Mehr als 5 Elemente", ansonsten "5 oder weniger Elemente".
Task (EN): Develop a Python program that fulfills the following tasks:
           a) Import the random module and use it to generate a list of 10 random integers between 1 and 100.
           b) Create a function named sort_and_count that takes a list of numbers as an argument. The function
           should sort the list in ascending order and return the number of elements in the list.
           c) Create another list that contains tuples of the original random numbers and the square of each number
           (e.g. [(number, square of the number), ...]).
           d) Use a loop to iterate over the list of tuples, and print for each tuple a formatted string
           that says: "The number X has the square Y".
           e) Write a control structure that checks if the number of elements in the sorted list is greater than 5.
           If yes, print "More than 5 elements", otherwise "5 or fewer elements".
"""

import random


# a)
original_list = []
for i in range(10):
    random_num = random.randint(1, 100)
    original_list.append(random_num)
# course solution | zufallszahlen = [random.randint(1, 100) for _ in range(10)]


# b)
def sort_and_count(original_list: list) -> int:
    original_list.sort()
    return len(original_list)


elements_number = sort_and_count(original_list)
# course solution
"""
def sortiere_und_zähle(zahlenliste):
    zahlenliste.sort()
    return len(zahlenliste)
anzahl_elemente = sortiere_und_zähle(zufallszahlen)
"""


# c)
tuple_list = []
for number in original_list:
    tuple_list.append((number, number**2))
# course solution | tupel_liste = [(zahl, zahl**2) for zahl in zufallszahlen]


# d)
for i in range(len(tuple_list)):
    print(f"The number {tuple_list[i][0]} has the square {tuple_list[i][1]}")
# course solution
"""
for zahl, quadrat in tupel_liste:
    print(f"Die Zahl {zahl} hat das Quadrat {quadrat}")
"""


# e)
if elements_number > 5:
    print("More than 5 elements")
else:
    print("5 or fewer elements")
# course solution
"""
if anzahl_elemente > 5:
    print("Mehr als 5 Elemente")
else:
    print("5 oder weniger Elemente")
"""

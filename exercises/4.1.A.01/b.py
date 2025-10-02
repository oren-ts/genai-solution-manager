"""
Übung 4.1.A.01/b
Task (DE): Schreibe eine Funktion, die prüft, ob ein bestimmtes Element (Tupel aus Buchstabe und Zahl) in der Liste \n
           vorhanden ist. Gib eine entsprechende Nachricht aus, z.B. "Element gefunden: (Buchstabe, Zahl)" oder \n
           "Element nicht gefunden".
Task (EN): Write a function that checks whether a specific element (a tuple consisting of a letter and a number) \n
           is present in the list. Output an appropriate message, such as "Element found: (letter, number)" or \n 
           "Element not found."
Notes: <what you learned / edge cases>
"""

list1 = [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]
#letter = str(input("Enter a letter a-z: "))
#number = int(input("Enter a number 1-9: "))
#tuple1 = (letter, number)
#if tuple1 in list1:
#    print(f"Element found {tuple1}.")
#else:
#    print("Element not found.")


def existing_element(letter, number):
    if (letter, number) in list1:
        print(f"Element found ({letter}, {number}).")
    else:
        print("Element not found.")
    return(letter, number)

existing_element('a', 1)
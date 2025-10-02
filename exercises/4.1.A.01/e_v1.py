"""
Übung 4.1.A.01/e
Task (DE): Implementiere eine einfache Benutzerschnittstelle in der Konsole, die es dem Benutzer ermöglicht,\n
           die Funktionen zu testen. Die Benutzerschnittstelle sollte mindestens die Möglichkeit bieten, nach\n
           einem Element in der Liste zu suchen und eine Zeichenkette in eine Zahl umzuwandeln.
Task (EN): Implement a simple user interface in the console that allows the user to test the functions.\n
           The user interface should at least provide the ability to search for an element in the list and\n
           convert a string into a number.
Notes: <what you learned / edge cases>
"""
# Define the list of tuples
list1 = [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]

# Ask the user for input
letter = input("Enter a letter a-z: ")
number = input("Enter a number 1-9: ")

# Convert the number string to an integer
def string_to_integer(number):
    integer = int(number)
    print(f"The converted string is: {integer}")
    return integer

# Check if the element exists in the list
def existing_element(letter, number):
    if (letter, number) in list1:
        print(f"Element found ({letter}, {number}).")
    else:
        print("Element not found.")
    return(letter, number)

# Use the functions
converted_number = string_to_integer(number)
existing_element(letter, converted_number)

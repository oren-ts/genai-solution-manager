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

while True:
    action = input("Please select an action: 'Search', 'Convert', 'End': ")
    if action == 'Search':
        letter = input("Enter a letter between a-z: ")
        number = int(input("Enter a number between 1-9: "))
        existing_element(letter, number)
    elif action == 'Convert':
        integer = input("Enter a string, that will be converted to a number: ")
        converted_number = string_to_integer(integer)
    elif action == 'End':
        break
    else:
        print("Invalid input. Please try again")
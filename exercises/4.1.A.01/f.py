"""
Übung 4.1.A.01/f
Task (DE): Füge eine Kontrollstruktur hinzu, die prüft, ob die umgewandelte Zahl positiv,\n
           negativ oder Null ist, und gib eine entsprechende Nachricht aus.
Task (EN): Add a control structure that checks whether the converted number is positive,\n
           negative, or zero, and outputs an appropriate message.
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
        if converted_number is not None:
            if converted_number > 0:
                print("The number is positive.")
            elif converted_number < 0:
                print("The number is negative.")
            else:
                print("The number is zero.")
    elif action == 'End':
        break
    else:
        print("Invalid input. Please try again")
"""
Übung 4.1.A.01/d
Task (DE): Kommentiere dein Skript ausführlich, um die Logik hinter deinem Code zu erklären.
Task (EN): Comment your script thoroughly to explain the logic behind your code.
Notes: <what you learned / edge cases>
"""

def string_to_integer(string):                   # Define a function with one input parameter
    integer = int(string)                        # Convert the input string to an integer and store it
    print(f"The converted string is: {integer}") # Print the converted integer
    return integer                               # Return the integer value

string_to_integer('42')                          # Call the function with the string '42'
"""
Übung 3.6.Ü.01/b
Task (DE): Erstelle ein Python-Skript, das eine Zeichenkette (String) von einem Benutzer einliest und anschließend prüft, ob es sich um eine Ganzzahl (int) oder eine Gleitkommazahl (float) handelt. Gib das Ergebnis aus und erkläre den Prozess in Kommentaren.
Task (EN): Create a Python script that reads a string from a user and then checks whether it is an integer (int) or a floating-point number (float). Output the result and explain the process in comments.
Notes: <what you learned / edge cases>
"""

# Input
user_input = input("Please enter a number: ")                                  # Prompting the user to enter a number

# Process and Output
if user_input.isdigit():                                                       # Checking if the input string consists only of digits
    number = int(user_input)                                                   # Converting the string to an integer
    print(f"The input {number} is an integer")                                 # Outputting that the input is an integer
elif user_input.replace('.', '', 1).isdigit() and user_input.count('.') == 1:  # Checking if the input is a valid float
    number = float(user_input)                                                 # Converting the string to a float
    print(f"The input {number} is a float")                                    # Outputting that the input is a float
else:
    print("The input is neither an integer nor a float")                       # Outputting that the input is neither
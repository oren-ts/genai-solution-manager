"""
Übung 4.5.Ü.01
Task (DE): Entwickle ein Python-Programm, das die folgenden Anforderungen erfüllt:
           a) Das Programm soll zuerst den Benutzer bitten, eine ganze Zahl einzugeben.
           Verwende dafür die Funktion input() und wandle die Eingabe in eine ganze Zahl um.
           b) Überprüfe anschließend, ob die eingegebene Zahl kleiner als 10, gleich 10 oder größer als 10 ist.
           Verwende dafür eine Kombination aus if, elif und else Anweisungen.
           c) Für jede der drei Bedingungen soll das Programm eine entsprechende Nachricht ausgeben:
           Wenn die Zahl kleiner als 10 ist, soll ausgegeben werden: "Die Zahl ist kleiner als 10."
           Wenn die Zahl gleich 10 ist, soll ausgegeben werden: "Die Zahl ist genau 10."
           Wenn die Zahl größer als 10 ist, soll ausgegeben werden: "Die Zahl ist größer als 10."
           d) Am Ende soll das Programm eine Liste von Zahlen von 1 bis zur eingegebenen Zahl (inklusive)
           mithilfe einer for-Schleife ausgeben. Jede Zahl soll in einer neuen Zeile angezeigt werden.
           Verwende Kommentare im Code, um die einzelnen Schritte zu erläutern.
Task (EN): Develop a Python program that meets the following requirements:
           a) The program should first prompt the user to enter an integer. Use the input()
           function and convert the input to an integer.
           b) Then check whether the entered number is less than 10, equal to 10, or greater than 10.
           Use a combination of if, elif, and else statements.
           c) For each of the three conditions, the program should output an appropriate message:
           If the number is less than 10, output: "The number is less than 10."
           If the number is equal to 10, output: "The number is exactly 10."
           If the number is greater than 10, output: "The number is greater than 10."
           d) At the end, the program should output a list of numbers from 1 to the entered number
           (inclusive) using a for loop. Each number should be displayed on a new line.
           Use comments in the code to explain the logic behind each step.
"""
# -------------------------------------------
# Program: Compare an integer to 10 and list numbers up to it
# Purpose: Demonstrates input validation, conditional branching,
#          and iteration with a for-loop.
# -------------------------------------------

# --- Input & validation ---
# Prompt the user until they enter a valid integer within 1–15.
# This prevents errors from non-numeric input and avoids printing
# excessively long lists later.
user_input = 0

while True:
    try:
        # Convert text input to integer; if it fails, re-prompt
        user_input = int(input('Enter a number between 1-15: '))
    except ValueError:
        print('Not a valid number. Try again!')
        continue
    # Accept the number only if it's within the safe range.
    if 1 <= user_input <= 15:
        break
    else:
        print('Must be in the range 1-15')

# --- Conditional logic ---
# Compare the validated number with 10 and print one of
# three mutually exclusive messages.
if user_input < 10:
    print('The number is less than 10.')
elif user_input > 10:
    print('The number is greater than 10.')
else:
    print('The number is exactly 10.')

# --- Iteration (output list) ---
# Print all integers from 1 up to and including the user's number.
# range(1, user_input + 1) ensures the upper bound is included.
for i in range(1, user_input + 1):
    print(i)

# --- Note ---
# The 1–15 limit is an intentional safeguard: it prevents the
# program from printing an extremely long list if the user
# accidentally enters a huge number.
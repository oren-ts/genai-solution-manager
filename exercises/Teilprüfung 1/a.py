"""
Teilprüfung 1
Task (DE): Entwickle ein Python-Programm, das als Taschenrechner für einfache mathematische Operationen\n
           (Addition, Subtraktion, Multiplikation, Division) fungiert. Das Programm soll den Benutzer zuerst fragen,\n
           welche Operation durchgeführt werden soll. Anschließend fragt es nach zwei Zahlen, führt die gewählte\n
           Operation mit diesen Zahlen durch und gibt das Ergebnis aus. Beachte dabei die korrekte Anwendung von Datentypen,\n
           die Implementierung von Kontrollstrukturen sowie die korrekte Verwendung von Kommentaren im Code. 
           
           a) Fordere den Benutzer auf, eine Operation auszuwählen, indem er einen der folgenden Buchstaben eingibt:\n
           A für Addition, S für Subtraktion, M für Multiplikation, D für Division.
           b) Frage den Benutzer nach zwei Zahlen.
           c) Führe die ausgewählte Operation mit diesen Zahlen durch und gib das Ergebnis aus.
           d) Implementiere eine Fehlerbehandlung für den Fall, dass bei der Division durch Null\n
           versucht wird oder ein ungültiger Operator eingegeben wird.
           e) Verwende Kommentare im Code, um die Logik hinter den einzelnen Schritten zu erklären. 
Task (EN): Develop a Python program that functions as a calculator for basic mathematical operations\n
           (addition, subtraction, multiplication, division). The program should first ask the user which operation\n
           they want to perform. Then, it should ask for two numbers, perform the selected operation with those numbers,\n
           and display the result. Make sure to correctly apply data types, implement control structures, and use comments\n
           in the code to explain the logic behind each step.

           a) Prompt the user to select an operation by entering one of the following letters:\n
           A for addition, S for subtraction, M for multiplication, D for division.  
           b) Ask the user for two numbers.  
           c) Perform the selected operation with those numbers and display the result.  
           d) Implement error handling in case of division by zero or an invalid operator input.  
           e) Use comments in the code to explain the logic behind each step.
Notes: <what you learned / edge cases>
"""
# Simple console calculator: asks for an operation (A/S/M/D), reads two numbers, computes the result,\n
# and guards against invalid input/zero division.

# Allowed operations: a=addition, s=subtraction, m=multiplication, d=division (stored in lowercase for easy comparison)
allowed_ops = ['a', 's', 'm', 'd']
# Read the user’s operation choice; normalize to lowercase and trim spaces for reliable comparisons.
operation = input('Select operation A - addition, S - subtraction, M - multiplication, D - division: ').lower().strip()
# Validation loop: keep asking until the user enters one of the allowed operations.
while operation not in allowed_ops:
    print('Wrong operation. Try again!')
    operation = input('Select operation A - addition, S - subtraction, M - multiplication, D - division: ').lower().strip()
# Read two numbers from the user and convert the text input to float so arithmetic works.   
number_1 = float(input('Enter first number: '))
number_2 = float(input('Enter second number: '))
# None means “no result yet”; only print when a real result has been computed.
result = None
# Select and perform the chosen operation using if/elif branches.
if operation == 'a':
    result = number_1 + number_2
elif operation == 's':
    result = number_1 - number_2
elif operation == 'm':
    result = number_1 * number_2
elif operation == 'd':
    # Guard clause: prevent division by zero and show a clear message instead of crashing.
    if number_2 == 0:
        print('The second number is 0. Division cannot proceed')
    else:
        result = number_1 / number_2
# Only print the result when a valid calculation has produced a number.
if result is not None:
    print(f'Your result is {result}')
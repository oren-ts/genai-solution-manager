"""
Übung 5.9.Ü.01
Task (DE): Entwickle ein Python-Programm, das eine Funktion namens berechne_durchschnitt definiert, welche eine Liste von Zahlen
           als Parameter akzeptiert und den Durchschnittswert dieser Zahlen zurückgibt. Dein Programm sollte folgende Anforderungen erfüllen:
           a) Definiere die Funktion berechne_durchschnitt, die eine Liste von Zahlen entgegennimmt. Die Funktion soll den Durchschnitt dieser Zahlen berechnen und das Ergebnis zurückgeben.
           b) Verwende eine for-Schleife innerhalb der Funktion, um durch die Liste zu iterieren und die Summe der Zahlen zu berechnen.
           c) Außerhalb der Funktion, definiere eine Liste von Zahlen und weise sie einer Variablen zu. Verwende dann diese Liste als Argument, um die Funktion berechne_durchschnitt aufzurufen.
           d) Gib das Ergebnis des Funktionsaufrufs mit einer aussagekräftigen Nachricht mithilfe der print()-Funktion aus.
           e) Stelle sicher, dass dein Programm auch mit einer leeren Liste umgehen kann, ohne einen Fehler zu verursachen. In diesem Fall soll die Funktion None zurückgeben.
Task (EN): Develop a Python program that defines a function called calculate_average, which accepts a list of numbers as a parameter
           and returns the average value of those numbers. Your program should meet the following requirements:
           a) Define the function calculate_average, which takes a list of numbers as input. The function should calculate the average of these numbers and return the result.
           b) Use a for loop inside the function to iterate through the list and calculate the sum of the numbers.
           c) Outside the function, define a list of numbers and assign it to a variable. Then use this list as an argument to call the calculate_average function.
           d) Display the result of the function call with a clear message using the print() function.
           e) Ensure that your program can handle an empty list without causing an error. In this case, the function should return None.
"""


def calculate_average(numbers: list) -> float:
    """
    Calculate the average of a list of numbers.

    This function computes the arithmetic mean of the provided list of numbers.
    If the list is empty, it returns None to avoid division by zero.

    Args:
        numbers (list): A list of numeric values (integers or floats).

    Returns:
        float: The average of the numbers, or None if the list is empty.

    Example:
        >>> calculate_average([1, 2, 3])
        2.0
        >>> calculate_average([])
        None
    """
    if not numbers:
        return None

    total_sum = 0  # Initialize sum to zero
    for x in numbers:
        total_sum += x  # Accumulate each number in the list

    average = float(total_sum / len(numbers))  # Compute average as float
    return average


# Sample list of numbers for demonstration
numbers_list = [2, 3, 4, 5, 6, 7, 8, 9]

# Calculate the average using the function
average = calculate_average(numbers_list)

# Check if average was calculated successfully and print the result
if average is not None:
    print(f"The average of the list is: {average:.2f}")
else:
    print("The list is empty.")

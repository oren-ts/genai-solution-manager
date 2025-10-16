"""
Übung 5.12.Ü.01
Task (DE): Entwickle eine Python-Funktion namens filtere_gerade_zahlen, die eine Liste von Zahlen als Argument
           nimmt und mithilfe der filter()-Funktion alle geraden Zahlen aus dieser Liste zurückgibt. Verwende eine
           Lambda-Funktion, um zu bestimmen, ob eine Zahl gerade ist. Die Funktion soll die gefilterten Zahlen als
           Liste zurückgeben. Teste deine Funktion mit einer Liste von Zahlen und gib das Ergebnis mit der print()-Funktion aus.
           Verwende für deine Tests die Liste [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] und stelle sicher, dass deine Funktion korrekt
           implementiert ist, indem du das Ergebnis überprüfst.
Task (EN): Develop a Python function named filter_even_numbers that takes a list of numbers as an argument and, using
           the filter() function, returns all even numbers from this list. Use a lambda function to determine whether a
           number is even. The function should return the filtered numbers as a list. Test your function with a list of
           numbers and output the result using the print() function. Use the list [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] for your
           tests and ensure that your function is correctly implemented by verifying the result.
"""


# Define the function to filter even numbers
def filter_even_numbers(numbers):
    # Use filter() with a lambda function to check if a number is even
    # Lambda function returns True if number % 2 == 0 (i.e., number is even)
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    return even_numbers


# Test the function with the given list
test_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = filter_even_numbers(test_list)

# Print the result to verify
print("Original list:", test_list)
print("Even numbers:", result)

"""
Übung 3.6.Ü.01/a
Task (DE): Schreibe ein Python-Skript, das eine Liste von Ganzzahlen definiert und die Summe sowie den Durchschnitt dieser Zahlen berechnet. Kommentiere jeden Schritt deines Skripts, um zu erklären, was gemacht wird.
Task (EN): Write a Python script that defines a list of integers and calculates the sum and average of these numbers. Comment each step of your script to explain what is being done.
Notes: <what you learned / edge cases>
"""
# Input
numbers = [10, 20, 30, 40, 50]                 # Defining a list of integers

# Process
total_sum = sum(numbers)                       # Calculating the sum of the numbers in the list
average = total_sum / len(numbers)             # Calculating the average by dividing the sum by the count of numbers

# Output
print(f"Sum: {total_sum}\nAverage: {average}") # Printing the sum and average
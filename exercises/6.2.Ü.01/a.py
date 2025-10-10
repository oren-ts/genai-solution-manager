"""
Übung 6.2.Ü.01
Task (DE): a) Gebe an, wie du das Modul math in Python importierst und verwende eine Funktion aus diesem Modul, um die Quadratwurzel von
           256 zu berechnen.
           b) Erstelle eine Variable radius mit dem Wert 7. Berechne den Umfang eines Kreises unter Verwendung der Variable radius
           und der Konstante pi aus dem Modul math. Schreibe das Ergebnis in eine neue Variable umfang und gib sie aus.
           c) Beschreibe, wie du eine eigene Funktion namens fahrenheit_zu_celsius definierst, die eine Temperatur in Fahrenheit
           entgegennimmt und die entsprechende Temperatur in Celsius zurückgibt. Verwende diese Funktion anschließend, um die Temperatur 68°F
           in Celsius umzurechnen und das Ergebnis auszugeben.
           d) Erkläre, wie eine einfache for-Schleife in Python aussieht, die die Zahlen von 1 bis einschließlich 5 ausgibt. Verwende dazu eine
           Schleife und die print-Funktion.
           e) Benenne die zwei grundlegenden Arten, wie Funktionen aus Modulen in Python importiert werden können, und gib für jede Art ein Beispiel an.
Task (EN): a) Specify how you import the math module in Python and use a function from this module to calculate the square root of 256.
           b) Create a variable radius with the value 7. Calculate the circumference of a circle using the variable radius and the constant
           pi from the math module. Write the result into a new variable umfang and print it.
           c) Describe how you define your own function named fahrenheit_zu_celsius that takes a temperature in Fahrenheit and returns
           the corresponding temperature in Celsius. Then use this function to convert the temperature 68°F to Celsius and print the result.
           d) Explain what a simple for loop in Python looks like that prints the numbers from 1 to 5 inclusive. Use a loop and the print function for this.
           e) Name the two basic ways in which functions from modules can be imported in Python, and give an example for each way.
"""

# a) Calculate the square root of a number and display it as a float with two decimal places.
import math

a = 9000
result = math.sqrt(a)
print(f"The square root is: {result:.2f}")


# b) Calculate the circumference of a circle using the radius and pi from the math module.
from math import pi

radius = 7
circum = 2 * pi * radius
print(f"The circumference is: {circum:.2f}")


# c) Convert a temperature from Fahrenheit to Celsius using a custom function.
def fahrenheit_to_celsius(temp_f: float) -> float:
    """
    Convert a temperature from Fahrenheit to Celsius.

    :param temp_f: Temperature in Fahrenheit (float)
    :return: Temperature in Celsius (float)
    """
    temp_c = (temp_f - 32) * 5 / 9
    return temp_c


temp_f = 100
print(f"The converted F temprature is: {fahrenheit_to_celsius(temp_f):.2f}")


# d) Use a for loop to print the integers from 1 to 5 inclusive.
for i in range(1, 6):
    print(i)


# e) Demonstrate two basic ways to import and use functions from modules.
import time  # Option 1: Import the entire module and qualify function calls.

local_time = time.asctime()
print(f"The local time is: {local_time}")

from time import asctime  # Option 2: Import specific functions directly.

local_time = asctime()
print(f"The local time is: {local_time}")

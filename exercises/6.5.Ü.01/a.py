"""
Übung 6.5.Ü.01
Task (DE): Entwickle ein Python-Programm, das folgende Aufgaben erfüllt:
           a) Importiere das Modul random und das Modul time.
           b) Definiere eine Funktion wuerfeln(), die eine zufällige Zahl zwischen 1 und 6 generiert und diese zurückgibt.
           Verwende dafür die Funktion randint() aus dem Modul random.
           c) Definiere eine Funktion aktueller_timestamp(), die den aktuellen Unix-Timestamp zurückgibt. Verwende dafür
           die Funktion time() aus dem Modul time.
           d) Schreibe eine Hauptschleife, die fünfmal läuft. In jedem Durchlauf soll die Funktion wuerfeln() aufgerufen
           und das Ergebnis zusammen mit dem aktuellen Unix-Timestamp ausgegeben werden. Nutze dafür die Funktion aktueller_timestamp().
           e) Sorge dafür, dass zwischen jedem Würfelwurf eine Pause von 2 Sekunden liegt. Verwende dafür die Funktion sleep() aus dem Modul time.
Task (EN): Develop a Python program that fulfills the following tasks:
           a) Import the random module and the time module.
           b) Define a function roll_dice(), which generates a random number between 1 and 6 and returns it.
           Use the randint() function from the random module for this.
           c) Define a function actual_timestamp(), which returns the current Unix timestamp.
           Use the time() function from the time module for this.
           d) Write a main loop that runs five times. In each iteration, the roll_dice() function should be
           called and the result output together with the current Unix timestamp. Use the actual_timestamp() function for this.
           e) Ensure that there is a pause of 2 seconds between each dice roll. Use the sleep() function from the time module for this.
"""

import random
import time


# Function to simulate a single die roll, returning a random number between 1 and 6
def roll_dice():
    return random.randint(1, 6)


# Function to get the current Unix timestamp in seconds since epoch
def actual_timestamp():
    return time.time()


# Main loop to roll the die 5 times with a 2-second delay between rolls
for i in range(5):
    dice_res = roll_dice()  # Store the result of the die roll
    timestamp = actual_timestamp()  # Capture the current timestamp
    print(f"{i+1} Roll - Dice result {dice_res}, time {timestamp} ")
    time.sleep(2)  # Pause for 2 seconds to space out the rolls

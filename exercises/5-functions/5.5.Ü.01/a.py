"""
Übung 5.5.Ü.01
Task (DE): Entwickle ein Python-Programm, das die folgenden Anforderungen erfüllt:
           a) Definiere eine Funktion namens temperatur_umrechner, die zwei Parameter akzeptiert:
           temperatur und einheit. Der Parameter einheit soll optional sein und standardmäßig den
           Wert 'C' für Celsius haben. Die Funktion soll die Temperatur von Celsius in Fahrenheit
           umrechnen, wenn einheit den Wert 'C' hat, und von Fahrenheit in Celsius, wenn einheit den
           Wert 'F' hat. Die Umrechnungsformeln lauten: (C = (F - 32) * 5/9) und (F = C * 9/5 + 32).
           b) Verwende eine while-Schleife, um vom Benutzer wiederholt Temperaturen und optional die
           Einheiten einzulesen, bis der Benutzer entscheidet, das Programm zu beenden. Gib für jede
           Eingabe die umgerechnete Temperatur aus. Implementiere eine Möglichkeit für den Benutzer,
           das Programm durch Eingabe eines bestimmten Wortes, zum Beispiel "ende", zu beenden.
           c) Stelle sicher, dass dein Programm Fehleingaben (wie z.B. nicht-numerische Temperaturwerte
           oder falsche Einheitsangaben) elegant behandelt, indem du entsprechende Fehlermeldungen ausgibst
           und den Benutzer zur erneuten Eingabe aufforderst.
Task (EN): Develop a Python program that meets the following requirements:
           a) Define a function called temperature_converter that accepts two parameters:
           temperature and unit. The unit parameter should be optional and default to 'C' for Celsius.
           The function should convert the temperature from Celsius to Fahrenheit when unit is 'C', and
           from Fahrenheit to Celsius when unit is 'F'. Use the formulas: (C = (F - 32) * 5/9) and (F = C * 9/5 + 32).
           b) Use a while loop to repeatedly read temperatures—and optionally the units—from the user until the user
           decides to exit the program. For each input, print the converted temperature. Implement a way for the user
           to end the program by entering a specific word, for example, “end”.
           c) Ensure that your program gracefully handles invalid inputs (e.g., non-numeric temperature values
           or incorrect unit entries) by displaying appropriate error messages and prompting the user to try again.
"""


def temperature_converter(temp: float, unit: str = "C"):
    if unit.upper() == "F":
        temp_celzius = round(float((temp - 32) * (5 / 9)), 2)
        return temp_celzius
    else:
        temp_fahrenheit = round(float(temp * (9 / 5) + 32), 2)
        return temp_fahrenheit


entered_temp = 0
entered_unit = 0
user_exit = True

while user_exit != "Q":
    try:
        entered_temp = float(input("Enter Temprature to convert: "))
    except ValueError:
        print("Enter a valid number. Try again!")
        continue
    else:
        entered_unit = input(
            "Enter temprature unit (C Celzius (Default if no unit entered), F Fahrenheit): "
        )
    print(f"The temprature is {temperature_converter(entered_temp, entered_unit)}")
    user_exit = input("Press Q to end the program: ").upper()

"""
# course solution
def temperatur_umrechner(temperatur, einheit='C'):
    if einheit == 'C':
        return temperatur * 9/5 + 32
    elif einheit == 'F':
        return (temperatur - 32) * 5/9
    else:
        return None
while True:
    eingabe = input("Gib eine Temperatur mit Einheit ein (z.B. '35 C' oder '95 F'), oder 'ende' zum Beenden: ")
    if eingabe.lower() == 'ende':
        break
    try:
        teile = eingabe.split()
        temp = float(teile[0])
        if len(teile) == 2:
            einheit = teile[1].upper()
        else:
            einheit = 'C'  # Standardwert, wenn keine Einheit angegeben ist
        umgerechnet = temperatur_umrechner(temp, einheit)
        if umgerechnet is not None:
            if einheit == 'C':
                print(f"{temp} °C entspricht {umgerechnet} °F")
            else:
                print(f"{temp} °F entspricht {umgerechnet} °C")
        else:
            print("Bitte gib eine gültige Einheit ('C' oder 'F') ein.")
    except ValueError:
        print("Bitte gib eine gültige Zahl für die Temperatur ein.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
"""

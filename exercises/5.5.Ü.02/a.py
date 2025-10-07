"""
Übung 5.5.Ü.01
Task (DE): Entwickle ein Python-Programm, das eine Funktion namens umrechner enthält, welche zwei Parameter
           akzeptiert: betrag und waehrung, wobei waehrung einen optionalen Parameter darstellt, der standardmäßig
           auf "USD" gesetzt ist. Die Funktion soll den betrag von Euro in die angegebene Währung umrechnen. Verwende
           für die Umrechnung folgende fiktive Wechselkurse: 1 Euro = 1,1 USD und 1 Euro = 0,9 GBP. Das Programm soll
           den Benutzer auffordern, einen Betrag und eine Währung einzugeben, und dann das Ergebnis der Umrechnung ausgeben.
           Implementiere zusätzlich eine Kontrollstruktur, die überprüft, ob die eingegebene Währung unterstützt wird,
           und eine entsprechende Nachricht ausgibt, falls dies nicht der Fall ist. Verwende Schleifen, um den Benutzer
           die Möglichkeit zu geben, mehrere Umrechnungen durchzuführen, bis er das Programm explizit beendet.
Task (EN): Develop a Python program that contains a function named converter which accepts two parameters: amount and currency,
           where currency is an optional parameter that defaults to "USD". The function should convert the amount from euros into the specified currency.
           Use the following fictitious exchange rates:
           - 1 Euro = 1.1 USD
           - 1 Euro = 0.9 GBP
           The program should prompt the user to enter an amount and a currency, and then display the result of the conversion.
           Additionally, implement a control structure that checks whether the entered currency is supported and outputs a corresponding message if it is not.
           Use loops to allow the user to perform multiple conversions until they explicitly choose to end the program.
"""


def converter(amount, currency="USD"):
    if currency == "USD":
        return amount * 1.1
    elif currency == "GBP":
        return amount * 0.9
    else:
        return None


while True:
    user_input = input(
        "Enter amount and currency to convert e.g. 100 USD, 50 GBP, or type 'end' to exit the program: "
    )
    if user_input.lower() == "end":
        break
    try:
        user_list = user_input.split()
        temp_amount = float(user_list[0])
        if len(user_list) == 2:
            currency = user_list[1].upper()
        else:
            currency = "USD"
        converted_amount = converter(temp_amount, currency)
        if converted_amount is not None:
            if currency == "USD":
                print(f"You converted {temp_amount} EUR to {converted_amount} USD")
            else:
                print(f"You converted {temp_amount} EUR to {converted_amount} GBP")
        else:
            print('Not a valid currency. Enter "USD" or "GBP"')
    except ValueError:
        print("Not a valid amount. Enter a number")

"""
# course solution
ef umrechner(betrag, waehrung="USD"):
    if waehrung == "USD":
        return betrag * 1.1
    elif waehrung == "GBP":
        return betrag * 0.9
    else:
        return None
while True:
    print("Währungsumrechner: EUR zu USD oder GBP")
    betrag = float(input("Bitte geben Sie den Betrag in EUR ein, den Sie umrechnen möchten: "))
    waehrung = input("Bitte geben Sie die Währung ein, in die Sie umrechnen möchten (USD/GBP). Drücken Sie Enter für USD: ").upper()
    
    if waehrung not in ["USD", "GBP", ""]:
        print("Die angegebene Währung wird nicht unterstützt.")
    else:
        ergebnis = umrechner(betrag, waehrung)
        if ergebnis is not None:
            print(f"Umrechnungsergebnis: {ergebnis:.2f} {waehrung}")
        else:
            print("Es gab ein Problem mit der Währungsumrechnung.")
    
    weiter = input("Möchten Sie eine weitere Umrechnung durchführen? (ja/nein): ").lower()
    if weiter != "ja":
        print("Programm beendet.")
        break
"""

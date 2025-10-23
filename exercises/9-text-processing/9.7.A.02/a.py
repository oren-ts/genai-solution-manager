"""
Transferaufgabe 9.7.A.02
Task (DE): Entwickle ein Python-Programm, das eine Textdatei mit einer Liste von Produkten und deren Preisen verarbeitet.
           Die Datei soll in folgendem Format vorliegen:
           Produkt,Preis
           Milch,1.29
           Brot,2.49
           Äpfel,3.19
           a) Lese die Datei ein und speichere die Daten in einer geeigneten Datenstruktur. Verwende dabei die
           with-Anweisung und stelle sicher, dass Fehler beim Lesen der Datei ordnungsgemäß behandelt werden.
           b) Füge eine Funktion hinzu, die die Mehrwertsteuer für jedes Produkt berechnet. Die Mehrwertsteuer
           beträgt 19%. Speichere die Ergebnisse in einer neuen Datenstruktur, die sowohl den Originalpreis als
           auch den Preis inklusive Mehrwertsteuer enthält.
           c) Erweitere das Programm, sodass es eine neue Datei erstellt, die neben dem Produktnamen und dem Originalpreis
           auch den Preis inklusive Mehrwertsteuer enthält. Das Format soll wie folgt sein:
           Produkt,Preis,MwSt
           Milch,1.29,1.54
           Brot,2.49,2.96
           Äpfel,3.19,3.80
           d) Implementiere eine Fehlerbehandlung für den Fall, dass die Eingabedatei Produkte mit ungültigen
           Preisen enthält (z.B. nicht-numerische Werte). In solchen Fällen soll eine Warnmeldung ausgegeben und das
           betroffene Produkt übersprungen werden.
           e) Verwende reguläre Ausdrücke, um zu überprüfen, ob die Produktbezeichnungen gültig sind
           (bestehend aus Buchstaben, Zahlen und ggf. Leerzeichen). Ungültige Produktbezeichnungen sollen ähnlich
           wie bei d) behandelt werden.
Task (EN): Develop a Python program that processes a text file with a list of products and their prices.
           The file should be in the following format:
           Product,Price
           Milk,1.29
           Bread,2.49
           Apples,3.19
           a) Read the file and store the data in a suitable data structure. Use the with statement and make sure that
           errors when reading the file are handled properly.
           b) Add a function that calculates the value-added tax (VAT) for each product. The VAT rate is 19%. Store the
           results in a new data structure that contains both the original price and the price including VAT.
           c) Extend the program so that it creates a new file that contains, in addition to the product name and the
           original price, also the price including VAT.The format should look as follows:
           Product,Price,VAT
           Milk,1.29,1.54
           Bread,2.49,2.96
           Apples,3.19,3.80
           d) Implement error handling for the case that the input file contains products with invalid prices
           (e.g., non-numeric values). In such cases, a warning message should be output and the affected product skipped.
           e) Use regular expressions to check whether the product names are valid (consisting of letters,
           numbers, and, if applicable, spaces). Invalid product names should be handled in the same way as in d).
"""

import re

FILE_ORG = "prices.txt"
FILE_MOD = "prices_vat.txt"


def calculate_vat(vat_rate, price_list):
    """Calculate price including VAT for each product."""
    vat_list = []
    for product, price in price_list:
        price_with_vat = round(price * (1 + vat_rate / 100), 2)
        vat_list.append(
            {"Product": product, "Price": price, "Price VAT": price_with_vat}
        )
    return vat_list


def main():
    try:
        with open(FILE_ORG, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]  # skip header
            price_list = []
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) != 2 or not parts[0]:
                    continue  # skip malformed line

                product = parts[0]

                # Use re.findall() to check for invalid characters
                # It returns a list of all *invalid* characters (not allowed)
                invalid_chars = re.findall(r"[^A-Za-z0-9 ]", product)

                if invalid_chars:
                    print(f"Invalid product name: {product}")
                    continue  # skip invalid names

                try:
                    price = float(parts[1])
                except ValueError:
                    print(
                        f"Invalid price on line: {line.strip()}"
                    )  # skip if not a valid number
                    continue

                price_list.append((product, price))

        # Calculate VAT
        vat_data = calculate_vat(19, price_list)

        # Write to new file
        with open(FILE_MOD, "w", encoding="utf-8") as file:
            file.write("Product,Price,VAT\n")
            for item in vat_data:
                file.write(f"{item['Product']},{item['Price']},{item['Price VAT']}\n")

        print(f"File '{FILE_MOD}' created successfully!")

    except FileNotFoundError:
        print(f"File {FILE_ORG} not found.")


main()

"""
Case Study 5.12.C.01
Task (DE): Entwickle ein Python-Programm, das eine Datenanalyse für ein fiktives Unternehmen durchführt, welches
           verschiedene Produkte verkauft. Deine Aufgabe besteht darin, eine Reihe von Funktionen zu erstellen,
           die verschiedene Analysen ermöglichen. Das Programm soll folgende Funktionen beinhalten:
           Liste an Produkten: Laptop, 999,00€; Smartphone, 599,00€; Kopfhörer, 149,00€; Smartwatch, 249,00€;
           Tablet, 399,00€; E-Book-Reader, 129,00€; Fitness-Tracker, 79,00€; Bluetoothlautsprecher, 89,00€; Powerbank, 39,00€;
           Webcam, 59,00€
           a) Eine Funktion durchschnittspreis, die den Durchschnittspreis aus einer Liste von Produkt-Preisen berechnet.
           Die Funktion nimmt eine Liste von Preisen als Argument und gibt den Durchschnittspreis zurück.
           b) Eine Funktion produkt_filter, die eine Liste von Produktnamen und einen Buchstaben als Argumente nimmt und
           alle Produkte zurückgibt, die mit diesem Buchstaben beginnen, unter Verwendung der filter()-Funktion.
           c) Eine rekursive Funktion max_preis, die den höchsten Preis in einer Liste von Preisen findet. Wenn die Liste
           leer ist, soll die Funktion None zurückgeben.
           d) Eine Funktion preis_mit_steuer, die den Preis eines Produkts inklusive Mehrwertsteuer berechnet. Die Funktion
           nimmt zwei Argumente: den Preis ohne Steuer und den Steuersatz (als optionalen Parameter mit einem Default-Wert von 19%).
           e) Eine Lambda-Funktion, die zusammen mit der map()-Funktion verwendet wird, um die Preise einer Liste von Produkten um
           einen bestimmten Prozentsatz zu erhöhen. Die Prozentsatzerhöhung soll als Argument übergeben werden.
           f) Eine Funktion drucke_produktliste, die eine Liste von Produktnamen schön formatiert auf der Konsole ausgibt.
           Verwende die print()-Funktion, um jedes Produkt in einer neuen Zeile auszugeben.
Task (EN): Develop a Python program that performs data analysis for a fictional company that sells various products.
           Your task is to create a set of functions that enable different analyses. The program should include the following
           functions based on this product list: Laptop, €999.00; Smartphone, €599.00; Headphones, €149.00; Smartwatch, €249.00; Tablet,
           €399.00; E-Book Reader, €129.00; Fitness Tracker, €79.00; Bluetooth Speaker, €89.00; Powerbank, €39.00; Webcam, €59.00.
           a) A function `average_price` that calculates the average price from a list of product prices. The function takes a list of
           prices as an argument and returns the average price.
           b) A function `product_filter` that takes a list of product names and a letter as arguments and returns all products
           that start with that letter, using the `filter()` function.
           c) A recursive function `max_price` that finds the highest price in a list of prices. If the list is empty,
           the function should return `None`.
           d) A function `price_with_tax` that calculates the price of a product including value-added tax. The function takes
           two arguments: the price without tax and the tax rate (as an optional parameter with a default value of 19%).
           e) A lambda function used with the `map()` function to increase the prices of a list of products by a certain percentage.
           The percentage increase should be passed as an argument.
           f) A function `print_product_list` that prints a list of product names in a nicely formatted way to the console.
           Use the `print()` function to output each product on a new line.
"""

# Product data: nested list of names and prices
items = [
    [
        "Laptop",
        "Smartphone",
        "Headphones",
        "Smartwatch",
        "Tablet",
        "E-Book Reader",
        "Fitness Tracker",
        "Bluetooth Speaker",
        "Powerbank",
        "Webcam",
    ],
    [999.00, 599.00, 149.00, 249.00, 399.00, 129.00, 79.00, 89.00, 39.00, 59.00],
]

# Extract prices for calculations
prices = items[1]


def average_price(prices_list: list[float]) -> float:
    """Calculate the average price from a list of floats, returning 0.0 if empty."""
    if not prices_list:
        return 0.0
    total = 0.0  # Float for decimal precision
    for price in prices_list:
        total += price
    return total / len(prices_list)


# Extract names for filtering
names = items[0]


def product_filter(names: list[str], letter: str) -> list[str]:
    """Filter product names starting with the given letter (case-insensitive)."""
    result = list(filter(lambda name: name.lower().startswith(letter.lower()), names))
    return result


def max_price(prices: list[float]) -> float:
    # Handle empty list
    if not prices:
        return None
    # Base case: single item is the max
    if len(prices) == 1:
        return prices[0]
    else:
        # Recursively find max of remaining items
        prices_rest = max_price(prices[1:])
        # Compare first item with max of the rest
    return prices[0] if prices[0] > prices_rest else prices_rest


def price_with_tax(price: float, tax_rate: float = 0.19) -> float:
    """Calculate price including VAT (default tax rate 19%)."""
    return price * (1 + tax_rate)


def increase_prices_by_percentage(
    prices_list: list[float], percentage: float
) -> list[float]:
    """Increase all prices by a given percentage using map() and lambda."""
    return list(map(lambda p: p * (1 + percentage / 100), prices_list))


def print_product_list(products: list[str]) -> None:
    """Print product names."""
    for product in products:
        print(f"{product}")


# Test with formatted output (2 decimal places)
print(f"Average Price: €{average_price(prices):.2f}")
# Test with dynamic letter
letter = "S"
print(f"Products starting with {letter}: {product_filter(names, letter)}")
# Test with extracted prices for claculations
print(f"The maximum price in the list is: {max_price(prices)}")
# Test with Laptop price and default tax rate
print(f"{names[1]} with tax: €{price_with_tax(prices[1]):.2f}")
# Test with 10% increase, show first three prices
percentage = 10
increased = increase_prices_by_percentage(prices, percentage)
print(
    f"First three prices +{percentage}%: €{increased[0]:.2f}, €{increased[1]:.2f}, €{increased[2]:.2f}"
)
# Test by printing all product names
print_product_list(names)

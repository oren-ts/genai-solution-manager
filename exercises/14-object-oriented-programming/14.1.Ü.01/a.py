"""
Übung 14.1.Ü.01
Task (DE):
Task (EN): Develop a Python class Auto that has several attributes such as brand, model, year of manufacture, and mileage.
           The class should include the following methods:
           a) An initialization method that allows the brand, model, and year of manufacture to be specified when creating
           an Auto object, while the mileage is set to 0 by default.
           b) A method fahren (drive) that increases the mileage by the number of kilometers passed as a parameter.
           c) A method anzeigen (display) that outputs the details of the car (brand, model, year of manufacture, mileage)
           in a readable format.
           Make sure you correctly apply object-oriented programming concepts, especially defining classes, initializing
           objects, and calling methods. Test your class by creating at least two Auto objects, changing their mileage
           using the fahren method, and finally displaying the details of each car with the anzeigen method.
"""


class Auto:
    def __init__(self, brand, model, year):
        """Initialize a new Auto instance with brand, model, year, and default mileage of 0."""
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = 0  # Default mileage set to 0 as per requirements

    def increase_mileage(self, kilometer):
        """Increase the car's mileage by the specified number of kilometers."""
        self.mileage += kilometer

    def display_details(self):
        """Display all car details in a readable format."""
        print(
            f"Brand: {self.brand}\nModel: {self.model}\nYear: {self.year}\nMileage: {self.mileage}"
        )


if __name__ == "__main__":
    # Create two Auto instances
    a = Auto("Toyota", "Corola", 2020)
    b = Auto("BMW", "A1", 2022)

    # Simulate driving by increasing mileage
    a.increase_mileage(100)
    b.increase_mileage(50)

    # Display details of both cars
    a.display_details()
    b.display_details()

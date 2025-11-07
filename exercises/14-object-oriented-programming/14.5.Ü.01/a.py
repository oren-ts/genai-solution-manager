"""
Übung 14.5.Ü.01
Task (EN): Create a class Car with the following attributes:
           brand (string)
           model (string)
           mileage (integer)
           fuel_level (as a percentage, integer)
           The class should have two methods: drive(kilometers) and refuel(percent).
           The method drive(kilometers) should increase the mileage by the driven kilometers and reduce the fuel
           level based on the assumption that the car consumes 5% of the tank per 100 kilometers.
           The method refuel(percent) should increase the fuel level by the given percentage but must not exceed 100%.
"""


class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.mileage = 0
        self.fuel_level = 100

    def drive(self, kilometer):
        fuel_consumption = 5
        if self.fuel_level >= (round((fuel_consumption / 100) * kilometer)):
            self.fuel_level = self.fuel_level - (
                round((fuel_consumption / 100) * kilometer)
            )
            self.mileage += kilometer
        else:
            raise ValueError("Not enough fuel.")

    def refuel(self, fuel):
        if fuel < 0:
            raise ValueError("Fuel amount cannot be negative.")
        if fuel > 100:
            raise ValueError("Fuel amount cannot exceed 100%.")
        self.fuel_level = min(100, (self.fuel_level + fuel))


def main():
    print("=== Car Testing Program ===\n")

    # Test 1: Create a car and check initial values
    print("Test 1: Creating a new car")
    my_car = Car("BMW", "320i")
    print(f"Brand: {my_car.brand}")
    print(f"Model: {my_car.model}")
    print(f"Initial mileage: {my_car.mileage} km")
    print(f"Initial fuel level: {my_car.fuel_level}%\n")

    # Test 2: Drive a short distance
    print("Test 2: Driving 100 km")
    my_car.drive(100)
    print(f"Mileage after driving: {my_car.mileage} km")
    print(f"Fuel level after driving: {my_car.fuel_level}%\n")

    # Test 3: Drive another distance
    print("Test 3: Driving 500 km")
    my_car.drive(500)
    print(f"Mileage after driving: {my_car.mileage} km")
    print(f"Fuel level after driving: {my_car.fuel_level}%\n")

    # Test 4: Refuel the car
    print("Test 4: Refueling by 30%")
    my_car.refuel(30)
    print(f"Fuel level after refueling: {my_car.fuel_level}%\n")

    # Test 5: Try to overfill the tank
    print("Test 5: Trying to refuel by 80% (should cap at 100%)")
    my_car.refuel(80)
    print(f"Fuel level after refueling: {my_car.fuel_level}%\n")

    # Test 6: Drive until low fuel
    print("Test 6: Driving 1500 km")
    my_car.drive(1500)
    print(f"Mileage after driving: {my_car.mileage} km")
    print(f"Fuel level after driving: {my_car.fuel_level}%\n")

    # Test 7: Try to drive without enough fuel (should raise error)
    print("Test 7: Trying to drive 500 km with low fuel")
    try:
        my_car.drive(500)
        print("Drive successful")
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Current mileage: {my_car.mileage} km")
        print(f"Current fuel level: {my_car.fuel_level}%\n")

    # Test 8: Try to refuel with negative value (should raise error)
    print("Test 8: Trying to refuel with -20% (invalid)")
    try:
        my_car.refuel(-20)
        print("Refuel successful")
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Current fuel level: {my_car.fuel_level}%\n")

    # Test 9: Try to refuel with value over 100% (should raise error)
    print("Test 9: Trying to refuel with 150% (invalid)")
    try:
        my_car.refuel(150)
        print("Refuel successful")
    except ValueError as e:
        print(f"Error: {e}")
        print(f"Current fuel level: {my_car.fuel_level}%\n")

    # Test 10: Refuel and continue driving
    print("Test 10: Refueling by 50% and driving 200 km")
    my_car.refuel(50)
    print(f"Fuel level after refueling: {my_car.fuel_level}%")
    my_car.drive(200)
    print(f"Mileage after driving: {my_car.mileage} km")
    print(f"Fuel level after driving: {my_car.fuel_level}%\n")

    # Test 11: Create a second car to verify independence
    print("Test 11: Creating a second car")
    second_car = Car("Audi", "A4")
    print(f"Second car - Brand: {second_car.brand}, Model: {second_car.model}")
    print(
        f"Second car - Mileage: {second_car.mileage} km, Fuel: {second_car.fuel_level}%"
    )
    print(f"First car - Mileage: {my_car.mileage} km, Fuel: {my_car.fuel_level}%\n")

    print("=== Testing Complete ===")


if __name__ == "__main__":
    main()

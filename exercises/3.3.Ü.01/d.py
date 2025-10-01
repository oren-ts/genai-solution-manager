# A tuple is ordered but immutable (cannot be changed)
# A list is ordered and mutable (can be changed)

fruits = ('apple', 'banana', 'cherry')    # Tuple
print(f"Tuple: {fruits}")
# fruits [1] = 'orange'                   # Uncommenting this line would raise a TypeError

prime_numbers = [2, 3, 5, 7, 11, 13, 17]  # List
print(f"Original list: {prime_numbers}")
prime_numbers [3] = 19                   # Change element at index 3
print(f"Modified list: {prime_numbers}")
"""
Übung 13.3.Ü.01
Task (DE):
Task (EN): a) Define a function filter_even_numbers that takes a list of numbers as an argument
           and returns a new list containing only the even numbers. Use a loop to iterate through the list.
           b) Add an assertion at the beginning of the function to ensure that the passed argument is indeed a list.
           If the argument is not a list, the program should terminate with an AssertionError.
           c) Write a second function sort_list that takes a list of numbers and sorts it using the
           quicksort algorithm. You may choose your own implementation of the quicksort algorithm, but make sure it is
           implemented correctly.
           d) Use the filter_even_numbers function to filter a list of numbers, and then use the sort_list function
           to sort the filtered list. Print the result.
           e) At the end of the script, include a test routine that tests your functions with a predefined list of numbers.
           The list should include both positive and negative numbers as well as zero.
"""


def filter_even_numbers(s: list) -> list:
    """Filter and return only even numbers from the input list."""
    # Ensure input is a list, raise AssertionError otherwise
    assert isinstance(s, list), "AssertionError: Not a valid list"

    filtered = []
    # Iterate through each number in the list
    for num in s:
        # Check if number is even (remainder 0 when divided by 2)
        if num % 2 == 0:
            filtered.append(num)
    return filtered


def sort_list(s: list) -> list:
    """Sort a list of numbers using the quicksort algorithm."""
    # Base case: list with 0 or 1 element is already sorted
    if len(s) <= 1:
        return s
    else:
        # Select first element as pivot
        pivot = s[0]

        # Partition: elements less than pivot
        s1 = [x for x in s if x < pivot]
        # Partition: elements equal to pivot
        s2 = [x for x in s if x == pivot]
        # Partition: elements greater than pivot
        s3 = [x for x in s if x > pivot]

        # Recursively sort partitions and combine: left + middle + right
        return sort_list(s1) + s2 + sort_list(s3)


def test_functions():
    """Test the filter and sort functions with positive, negative, and zero values."""
    test_list = [3, -1, 4, 1, -5, 9, 2, -6, -5, 3, 0]

    print(f"Original list: {test_list}")

    # Filter out only even numbers
    result = filter_even_numbers(test_list)
    print(f"Filtered (even numbers): {result}")

    # Sort the filtered list using quicksort
    sorted_result = sort_list(result)
    print(f"Sorted result: {sorted_result}")


# Run tests when script is executed directly
if __name__ == "__main__":
    test_functions()

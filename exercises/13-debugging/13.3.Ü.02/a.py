"""
Übung 13.3.Ü.02
Task (DE):
Task (EN): You are to write a Python function named improve_quicksort that implements the Quicksort
           algorithm and includes an improvement: before the actual sorting begins, the function should
           check whether the list is already sorted. If this is the case, the function should return
           the list directly without performing the Quicksort algorithm.
           This check should be implemented using an assertion (assert), which ensures that the function
           only executes the Quicksort algorithm when the list is not already sorted.
           Additionally, implement a simple debugging output that prints the state of the list before
           and after sorting to the console, provided the environment variable DEBUG is set to True.
"""

import os


def is_sorted(lst):
    """Check if a list is sorted in ascending order."""
    for j in range(len(lst) - 1):
        if lst[j] > lst[j + 1]:
            return False
    return True


def improve_quicksort(lst):
    """
    Sort a list using Quicksort with early-exit optimization for sorted lists.

    Prints debug information if DEBUG environment variable is 'True'.
    """
    if os.environ.get("DEBUG") == "True":
        print("Before sorting:", lst)

    # Early return if already sorted
    for j in range(len(lst) - 1):
        if lst[j] > lst[j + 1]:
            break
    else:
        if os.environ.get("DEBUG") == "True":
            print("After sorting:", lst)
        return lst

    # Verify list actually needs sorting (per requirement)
    assert not is_sorted(lst), "List should not be sorted at this point"

    result = quicksort(lst)

    if os.environ.get("DEBUG") == "True":
        print("After sorting:", result)

    return result


def quicksort(s: list) -> list:
    """Sort a list of numbers using the quicksort algorithm."""
    if len(s) <= 1:
        return s

    pivot = s[0]
    s1 = [x for x in s if x < pivot]
    s2 = [x for x in s if x == pivot]
    s3 = [x for x in s if x > pivot]

    return quicksort(s1) + s2 + quicksort(s3)


def test_functions():
    """Test the sorting function with various input values."""
    test_list = [-5, 3, -1, 0, 2]
    print(f"Original list: {test_list}")
    sorted_result = improve_quicksort(test_list)
    print(f"Sorted result: {sorted_result}")


if __name__ == "__main__":
    test_functions()

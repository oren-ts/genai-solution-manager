'''
CHANGELOG
v1: Hardcoded list with different data types and print their types
v2: Loop over elements in the list to print their types
v3: Loop over elements in the list to print their types with f-string
'''

'''
# v1: Create a list and show the type of each element in the list
my_list = [1, "Zwei", 3.0, True]
print(f"My list: {type(my_list[0]), type(my_list[1]), type(my_list[2]), type(my_list[3])}")
'''

'''
# v2: Create a list and show the type of each element in the list
my_list = [1, "Zwei", 3.0, True]
for element in my_list:
    print(type(element))
'''

# v3: Create a list and show the type of each element in the list with f-string
my_list = [1, "Zwei", 3.0, True]
for element in my_list:
    print(f"{element!r} -> {type(element).__name__}")
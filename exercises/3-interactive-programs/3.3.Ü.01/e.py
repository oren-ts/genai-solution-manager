'''
CHANGELOG
v1: Functional script. no comments per line
v2: Show IPO with clear per-line comments and a straightforward concat example
'''

'''
# Convert an integer to a string and concatenate it with another string
# Input
my_str = input("Please enter a number between 1 and 100: ")
my_int = int(input("Please enter a number between 1 and 100: "))
# Processing
converted_str = str(my_int)
# Output
print("Your input as string: " + my_str + converted_str)
'''

# INPUT (Eingabe)
my_str = input("Please enter some text: ")        # read a string from the user
my_int = int(input("Please enter an integer: "))  # read input and convert it to int

# PROCESSING (Verarbeitung)
converted_str = str(my_int)                       # convert the integer to a string
result = my_str + " " + converted_str             # concatenate the two strings

# OUTPUT (Ausgabe)
print(result)                                       # print the result
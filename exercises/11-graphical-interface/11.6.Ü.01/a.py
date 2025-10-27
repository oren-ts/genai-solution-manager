"""
Übung 11.6.Ü.01
Task (DE):
Task (EN): a) A Label widget that displays "Hello World!" using a font of your choice with a size of 14 points.
           b) An Entry widget where users can enter text.
           c) Two Button widgets: the first button should clear the text in the Entry widget when clicked,
           and the second button should close the application window.
           d) Use loops to create a list of tuples, each containing the button text and the corresponding function
           (for clearing the text and closing the window). Add the buttons to the application window based on this list.
           e) Design the application window so that the Label appears at the top, the Entry widget below it,
           and the Buttons are arranged at the bottom of the window.
           f) Use the pack() method for the layout management of all widgets.
           g) Write comments in your code to explain the functionality of the different parts.
           h) Ensure that the program runs error-free and that all widgets behave as described.
"""

from tkinter import Tk, Label, Entry, Button


# Function to clear text from entry widget
def clear_text():
    entry.delete(0, "end")


# Function to close the application window
def close_window():
    window.destroy()


# Create main application window
window = Tk()
window.title("My Tkinter Program")  # Add window title

# Create label widget displaying "Hello World!" with 14-point font
label = Label(master=window, text="Hello World!", font=("Verdana", 14))
label.pack()

# Create entry widget for user text input
entry = Entry(master=window, font=("Verdana", 14))
entry.pack()

# List of tuples containing button text and corresponding functions
buttons_list = [("Clear Text", clear_text), ("Close", close_window)]

# Create buttons using a loop and add them to the window
for text, command in buttons_list:
    button = Button(master=window, text=text, command=command)
    button.pack(side="bottom", pady=5)  # spacing and positioning

# Start the application main loop
window.mainloop()

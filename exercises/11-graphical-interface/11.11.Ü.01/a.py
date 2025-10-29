"""
Übung 11.11.Ü.01
Task (DE):
Task (EN): Your program should have a main window with the title "My First GUI Program".
           In this window, the following widgets should be placed and configured:
           a) A Label widget that displays the greeting “Welcome to my program!”.
           Make sure the text is centered and has a font size of 14 points.
           The background color of the label should be yellow ('yellow') and the text color should be blue ('blue').
           b) An Entry widget for text input that is at least 20 characters wide.
           c) Two Button widgets:
           The first button should be labeled "OK", and the second "Cancel".
           When the OK button is pressed, the program should output the text entered in the Entry widget to the console.
           When the Cancel button is pressed, the program should terminate.
           d) Arrange the widgets using a grid layout so that:
           – The Label widget is in the first row (row 0)
           – The Entry widget is in the second row (row 1)
           – Both Button widgets are next to each other in the third row (row 2).
"""

from tkinter import Tk, Label, Button, Entry


# Event handler for OK button: prints the text from the Entry widget
def print_text():
    text = entry.get()
    print(text)  # Output exactly the entered text, no extra message


# Event handler for Cancel button: closes the program
def terminate_program():
    app.destroy()


# Create the main window
app = Tk()
app.title("My First GUI Program")

# Configure the grid to expand and center widgets
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)  # For the second button

# Label: centered text, yellow background, blue text, font size 14
label = Label(
    app,
    text="Welcome to my program!",
    font=("Verdana", 14),
    bg="yellow",
    fg="blue",
    anchor="center",  # Centers the text inside the label
)
label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Entry: at least 20 characters wide
entry = Entry(app, width=25)
entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# OK Button
ok_button = Button(app, text="OK", command=print_text)
ok_button.grid(row=2, column=0, padx=(10, 5), pady=10, sticky="ew")

# Cancel Button – next to OK button
cancel_button = Button(app, text="Cancel", command=terminate_program)
cancel_button.grid(row=2, column=1, padx=(5, 10), pady=10, sticky="ew")

# Start the GUI event loop
app.mainloop()

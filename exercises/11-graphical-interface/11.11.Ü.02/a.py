"""
Übung 11.11.Ü.02
Task (DE):
Task (EN): Develop a Python script that creates a simple GUI (Graphical User Interface) with Tkinter.
           Your application should display a small quiz in which the user can choose between three options
           (A, B, C) using radiobuttons. Each option should represent a different color (Red, Green, Blue).
           After the selection and a click on a button "Confirm", the background color of the application
           window should change according to the selection. Use the control variable of the radiobuttons to
           determine the selection and adjust the background color accordingly. Also implement a function
           that performs the color change. The GUI should also contain a button "Reset" which resets the
           background color to the default color and clears the selection of the radiobuttons.
           a) Define the GUI elements and the necessary variables.
           b) Implement the function to change the background color based on the selection.
           c) Add event handlers for the buttons "Confirm" and "Reset".
           d) Organize the widgets in the window using the grid layout.
"""

from tkinter import Tk, Button, Radiobutton, StringVar


def change_background():
    """change window background based on selected color"""
    app.config(bg=COLORS.get(selection.get(), bg_color))


def reset_background():
    """reset window background and clear selection"""
    app.config(bg=bg_color)
    selection.set(None)


# map color choices to corresponding background colors
COLORS = {"A": "red", "B": "green", "C": "blue"}

# initialize main window
app = Tk()
app.title("Color Quiz")
app.geometry("450x300")

# store system default background color for reset
bg_color = app.cget("bg")

# variable to track selected radio button
selection = StringVar(value=None)

# create radio buttons for color choices
red = Radiobutton(app, text="A", value="A", variable=selection)
red.grid(row=1, column=0, sticky="w", padx=10)

green = Radiobutton(app, text="B", value="B", variable=selection)
green.grid(row=2, column=0, sticky="w", padx=10)

blue = Radiobutton(app, text="C", value="C", variable=selection)
blue.grid(row=3, column=0, sticky="w", padx=10)

# create control buttons for actions
confirm = Button(app, text="Confirm", command=change_background)
confirm.grid(row=4, column=0, sticky="w", padx=10)

reset = Button(app, text="Reset", command=reset_background)
reset.grid(row=4, column=1, sticky="w", padx=10)

# start application loop
app.mainloop()

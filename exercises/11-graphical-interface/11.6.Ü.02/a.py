"""
Übung 11.6.Ü.02
Task (DE):
Task (EN): a) Import the Tkinter module correctly and initialize the main window of the application.
           Name the window “My GUI”.
           b) Add a label widget that displays the text “Welcome to your GUI!” in the font “Arial”, size 16,
           with blue text on a yellow background. Position the label in the center of the window.
           c) Create a button labeled “Click me!”. When the button is clicked, the text of the label should
           change to “Button was clicked!”. Make sure that the button and the label are clearly visible and
           not overlapping.
           d) Implement a function that is called when the button is clicked and that changes the text of the label.
           Use the config method of the label widget to update the text.
           e) Make sure that the window has a fixed size and cannot be resized by the user.
           f) The program should run in an infinite loop so that the window remains open until the user
           closes it manually.
"""

# a) Import the Tkinter module
from tkinter import Tk, Label, Button

# Initialize the main window
window = Tk()
window.title("My GUI")  # Set window title
window.resizable(False, False)  # e) Prevent resizing
window.geometry("400x200")  # Optional fixed window size


# d) Define function to change the label text
def change_text():
    label.config(text="Button was clicked!")


# b) Create a label widget (blue text on yellow background)
label = Label(
    master=window,
    text="Welcome to your GUI!",
    font=("Arial", 16),
    fg="yellow",  # Text color
    bg="blue",  # Background color
    justify="center",  # Text alignment
)
label.pack(expand=True)  # Center the label in the window

# c) Create a button that changes the label text
button = Button(master=window, text="Click me!", command=change_text)
button.pack(side="bottom", pady=10)  # Place the button at the bottom

# f) Keep the window open until manually closed
window.mainloop()

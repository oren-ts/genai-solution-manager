"""
Übung 12.3.Ü.01
Task (DE):
Task (EN): Create a simple Python program using Tkinter that contains the following elements:
           a) A main window with the title "My GUI Program".
           b) In the main window, display a label with the text "Hello World!".
           c) Below the label, place a button that, when clicked, changes the label text to "Button was clicked!".
           d) Add a radiobutton that allows switching between two background colors for the label: red and blue.
           Selecting a radiobutton should immediately change the label’s background color according to the selection.
           e) Use a Canvas widget to draw a simple line and a circle.
"""

import tkinter as tk


def on_button_click():
    """Change the label text when button is clicked"""
    label.config(text="Button was clicked!")


def change_background_color():
    """Change label background color based on radiobutton selection"""
    color = color_var.get()
    label.config(bg=color)


# Create the main window
root = tk.Tk()
root.title("My GUI Program")
root.geometry("400x500")

# a) & b) Create a label with "Hello World!"
label = tk.Label(
    root, text="Hello World!", font=("Arial", 16), bg="lightgray", width=20, height=2
)
label.pack(pady=20)

# c) Create a button that changes the label text
button = tk.Button(root, text="Click Me!", command=on_button_click, font=("Arial", 12))
button.pack(pady=10)

# d) Create radiobuttons for background color selection
color_var = tk.StringVar(value="lightgray")

tk.Label(root, text="Select Label Background Color:", font=("Arial", 11)).pack(pady=5)

radio_red = tk.Radiobutton(
    root,
    text="Red",
    variable=color_var,
    value="red",
    command=change_background_color,
    font=("Arial", 10),
)
radio_red.pack()

radio_blue = tk.Radiobutton(
    root,
    text="Blue",
    variable=color_var,
    value="blue",
    command=change_background_color,
    font=("Arial", 10),
)
radio_blue.pack()

# e) Create a Canvas widget with a line and a circle
canvas = tk.Canvas(root, width=350, height=200, bg="white")
canvas.pack(pady=20)

# Draw a line
canvas.create_line(50, 50, 300, 50, fill="black", width=3)

# Draw a circle (oval with equal width and height)
canvas.create_oval(125, 80, 225, 180, fill="yellow", outline="black", width=2)

# Start the GUI event loop
root.mainloop()

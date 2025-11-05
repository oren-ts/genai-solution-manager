"""
Übung 12.3.Ü.02
Task (DE):
Task (EN): Create a Python script that contains a Tkinter window with the following widgets and functionalities:
           a) A label that displays “Choose your favorite color:”.
           b) Three radio buttons to choose between “Red”, “Green”, and “Blue”.
           c) A button labeled “Confirm” that, when clicked, executes a function displaying the name of the
           selected color in a separate label.
           d) A canvas widget that, when a color is selected and the “Confirm” button is clicked, changes its
           background color according to the selected color.
           e) Use a common control variable for the radio buttons.
           f) Ensure that the window uses a grid layout to organize the widgets.
"""

import tkinter as tk

# Create main application window
app = tk.Tk()
app.title("Color Selection")
app.geometry("450x450")

# Create and place the question label at the top (row 0, spanning 2 columns)
question_label = tk.Label(app, text="Choose your favorite color").grid(
    row=0, column=0, columnspan=2, pady=10
)

# Create a StringVar to hold the selected color value (shared by all radio buttons)
selection = tk.StringVar()

# Define radio button options: (display_text, value)
radio_buttons = [("Red", "red"), ("Green", "green"), ("Blue", "blue")]

# Create radio buttons in a loop, positioning them vertically
i = 1
for key, val in radio_buttons:
    rb = tk.Radiobutton(app, text=key, value=val, variable=selection).grid(
        row=i, column=0, pady=5, sticky="w"
    )
    i += 1

# Create label to display the selected color name (initially empty)
color_label = tk.Label(app, text="")
color_label.grid(row=5, column=0, columnspan=2, pady=10)

# Create canvas widget to display the color visually
color_canvas = tk.Canvas(app, width=200, height=200)
color_canvas.grid(row=6, column=0, columnspan=2)


# Define function to update label and canvas when Confirm is clicked
def show_color():
    # Get the currently selected color value
    selected_color = selection.get()
    # Only update if a color is actually selected
    if selected_color:
        # Update label with capitalized color name
        color_label.config(text=selected_color.title())
        # Change canvas background to the selected color
        color_canvas.config(bg=selected_color)


# Create Confirm button that triggers the show_color function
confirm_button = tk.Button(app, text="Confirm", command=show_color)
confirm_button.grid(row=4, column=0, sticky="w")

# Start the Tkinter event loop
app.mainloop()

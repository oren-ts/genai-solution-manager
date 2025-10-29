"""
Übung 11.11.A.01
Task (DE):
Task (EN): Develop a Python program that creates a graphical user interface (GUI) using Tkinter.
           Your program should include an application window with the following widgets and functionalities:
           a) An input field (Entry widget) where users can enter their name.
           b) A button (Button widget) that, when clicked, displays a greeting message along with the entered
           name in a Label widget.
           c) A Radiobutton widget that allows users to select their preferred greeting time:
           “Good morning”, “Good afternoon”, or “Good evening”. The selection should influence the greeting message.
           d) A Text widget that serves as a log, where every performed greeting is saved with a timestamp.
           e) Use the grid layout to arrange the widgets within the application window.
           f) Implement a function that returns the current time and date as a string and use it to generate the timestamp in the log.
           g) Design the application window and widgets attractively by adjusting sizes, colors, and fonts.
"""

from tkinter import *
import datetime

# Dictionary: Maps radio values to full English greetings
D = {
    "Morning": "Good Morning",
    "Afternoon": "Good Afternoon",
    "Evening": "Good Evening",
}


# Returns current time as formatted string (e.g., "2025-10-29 12:45:00")
def calculate_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Builds greeting, updates label, and logs full entry
def concatenate_name():
    name = name_entry.get().strip()
    if not name:
        name = "there"  # Fallback if empty
    greeting = D[greetings.get()] + ", " + name + "!"
    greeting_label.config(text=greeting)

    time_str = calculate_current_time()
    log_line = f"{time_str}: {greeting}\n"
    timestamp_text.insert("end", log_line)
    timestamp_text.see("end")  # Scroll to bottom


# ========================================
# MAIN WINDOW SETUP (Clean & Course-Like)
# ========================================
window = Tk()
window.title("Greeting App")

# --- Row 0: Name Entry + Button ---
name_entry = Entry(window, width=20)
name_entry.grid(row=0, column=1, padx=10, pady=10)

name_button = Button(window, text="Greet", command=concatenate_name)
name_button.grid(row=0, column=2, padx=10, pady=10)

# --- Row 1: Big Greeting Label ---
greeting_label = Label(window, text="", font=("Arial", 16))
greeting_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# --- Row 2: Radio Buttons (one per column) ---
greetings = StringVar()
greetings.set("Morning")  # Default selection

morning = Radiobutton(window, text="Good Morning", variable=greetings, value="Morning")
morning.grid(row=2, column=0, sticky="w", padx=10)

afternoon = Radiobutton(
    window, text="Good Afternoon", variable=greetings, value="Afternoon"
)
afternoon.grid(row=2, column=1, sticky="w", padx=10)

evening = Radiobutton(window, text="Good Evening", variable=greetings, value="Evening")
evening.grid(row=2, column=2, sticky="w", padx=10)

# --- Row 3: Log Area (Text Widget) ---
timestamp_text = Text(window, height=10, width=60)
timestamp_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Start the app
window.mainloop()

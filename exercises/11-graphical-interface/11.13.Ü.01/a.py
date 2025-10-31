"""
Übung 11.13.Ü.01
Task (DE):
Task (EN): Develop a Python program that creates a Tkinter application window. In this window, users should
           be able to choose between three different types of fruit (apples, bananas, oranges) using
           radiobuttons. After making a selection and clicking a "Confirm" button, the selected value should
           be displayed in a label. Additionally, a function should be implemented that allows opening a
           text file via a dialog box, with its content displayed in a text widget. The application should
           also include a button to close the window. Consider using threads to ensure that the GUI remains
           responsive while the file is being loaded.
"""

from tkinter import *
from tkinter import filedialog
from _thread import start_new_thread


def load():
    start_new_thread(load_file(), ())


def load_file():
    file_path = filedialog.askopenfilename()
    stream = open(file_path, encoding="utf-8")
    text.delete(1.0, "end")
    text.insert(1.0, stream.read())
    stream.close


def display_fruit():
    text = selection.get()
    label.config(text=text)


def close_app():
    app.destroy()


app = Tk()
app.title("Fruit Selection")
app.geometry("450x300")

label = Label(app, text="", bg="grey", fg="black", width=60)
label.grid(row=0, column=0, columnspan=2)

selection = StringVar(value=None)

apples = Radiobutton(app, text="apples", value="apples", variable=selection)
apples.grid(row=1, column=0, sticky="w", padx=10)

bananas = Radiobutton(app, text="bananas", value="bananas", variable=selection)
bananas.grid(row=2, column=0, sticky="w", padx=10)

oranges = Radiobutton(app, text="oranges", value="oranges", variable=selection)
oranges.grid(row=3, column=0, sticky="w", padx=10)

confirm = Button(app, text="Confirm", command=display_fruit)
confirm.grid(row=4, column=0, sticky="w", padx=10)

close = Button(app, text="Close", command=close_app)
close.grid(row=4, column=1, sticky="w", padx=10)

upload = Button(app, text="Upload file", command=load_file)
upload.grid(row=5, column=1, sticky="w", padx=10)

text = Text(app, width=60, height=20, wrap=WORD, font=("Arial", 10))
text.grid(row=6, column=0, columnspan=2)

app.mainloop()

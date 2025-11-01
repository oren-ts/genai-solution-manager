"""
Teilprüfung 5
Task (DE): Entwickle eine Python-Anwendung mit Tkinter für ein einfaches Quiz mit Fragen und mehreren
           Antwortmöglichkeiten über Radiobuttons. Die Anwendung soll Ergebnisse in einer Datei speichern
           und frühere Ergebnisse laden sowie Threads für Timer nutzen, um die GUI reaktionsfähig zu halten.
           a) Erstelle ein Python-Skript quiz_app.py, das die GUI aufbaut. Das Hauptfenster soll einen Titel,
           einen Bereich für die Frage, Radiobuttons für die Antwortmöglichkeiten, ein Timer-Label, einen
           "Nächste Frage"-Button und einen "Ergebnisse speichern"-Button enthalten.
           b) Implementiere Funktionen, um Fragen und Antwortmöglichkeiten anzuzeigen. Speichere jede Frage
           als Dictionary mit den folgenden Elementen: die Frage selbst, eine Liste der Antwortmöglichkeiten
           und die richtige Antwort.
           c) Füge einen Timer hinzu, der für jede Frage 30 Sekunden läuft. Verwende Threads, damit der Timer
           parallel zur GUI läuft und die Anwendung reaktionsfähig bleibt.
           d) Implementiere Eventhandler-Funktionen für die Buttons "Nächste Frage" und "Ergebnisse speichern".
           Der "Nächste Frage"-Button soll die nächste Frage laden und den Timer zurücksetzen. Der "Ergebnisse
           speichern"-Button soll die Antworten in einer Datei speichern und die Möglichkeit bieten, diese später zu laden.
           e) Verwende Dialogboxen, um den Pfad für das Speichern und Laden der Ergebnisse auszuwählen.
Task (EN): Develop a Python application using Tkinter for a simple quiz with questions and multiple answer options
           via radio buttons. The application should save results to a file and load previous results, as well as use
           threads for timers to keep the GUI responsive.
           a) Create a Python script quiz_app.py that builds the GUI. The main window should include a title, an area
           for the question, radio buttons for the answer options, a timer label, a "Next Question" button, and a
           "Save Results" button.
           b) Implement functions to display questions and answer options. Store each question as a dictionary with the
           following elements: the question itself, a list of answer options, and the correct answer.
           c) Add a timer that runs for 30 seconds per question. Use threads so that the timer runs in parallel with
           the GUI and keeps the application responsive.
           d) Implement event handler functions for the "Next Question" and "Save Results" buttons. The "Next Question"
           button should load the next question and reset the timer. The "Save Results" button should save the answers
           to a file and allow loading them later.
           e) Use dialog boxes to select the path for saving and loading results.
"""

# Import necessary modules
from tkinter import *
from tkinter import filedialog
from _thread import start_new_thread
from time import sleep

# -----------------------------
# Quiz Questions
# -----------------------------
quiz_questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Madrid", "Rome"],
        "correct_answer": "Paris",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Mercury"],
        "correct_answer": "Mars",
    },
    {
        "question": 'Who wrote the play "Romeo and Juliet"?',
        "options": [
            "Charles Dickens",
            "William Shakespeare",
            "Mark Twain",
            "Leo Tolstoy",
        ],
        "correct_answer": "William Shakespeare",
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct_answer": "Pacific Ocean",
    },
    {
        "question": "Which element has the chemical symbol O?",
        "options": ["Oxygen", "Gold", "Silver", "Iron"],
        "correct_answer": "Oxygen",
    },
    {
        "question": "How many continents are there on Earth?",
        "options": ["Five", "Six", "Seven", "Eight"],
        "correct_answer": "Seven",
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": [
            "Vincent van Gogh",
            "Leonardo da Vinci",
            "Pablo Picasso",
            "Claude Monet",
        ],
        "correct_answer": "Leonardo da Vinci",
    },
    {
        "question": "What is the capital of Japan?",
        "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"],
        "correct_answer": "Tokyo",
    },
    {
        "question": "Which gas do humans exhale during breathing?",
        "options": ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"],
        "correct_answer": "Carbon dioxide",
    },
    {
        "question": "In which year did the Titanic sink?",
        "options": ["1905", "1912", "1920", "1931"],
        "correct_answer": "1912",
    },
]

# -----------------------------
# Global Variables
# -----------------------------
current_question = 0  # Track which question we're on
user_results = []  # Store all user answers
quiz_result = ""  # Store formatted results for saving

# Timer variables
current_timer_number = 0  # Used to stop old timers when starting new ones
start_count = 30  # Seconds per question


# -----------------------------
# Functions
# -----------------------------
def show_question(index):
    """Display a question and its answer options."""
    global selection
    selection.set(None)  # Clear previous selection
    question_label.config(text=quiz_questions[index]["question"])
    options = quiz_questions[index]["options"]
    # Update all radio buttons with new options
    for i in range(4):
        radio_buttons[i].config(text=options[i], value=options[i])


def next_question():
    """Move to the next question or end the quiz."""
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question(current_question)
    else:
        # Quiz is finished
        question_label.config(text="Quiz completed!")
        for rb in radio_buttons:
            rb.config(text="", value="")
        countdown_label.config(text="")
        compare_answers()


def countdown(count, my_number):
    """Run a countdown timer in a separate thread."""
    while count >= 0:
        # Stop if a new timer has started
        if current_timer_number != my_number:
            return

        countdown_label.config(text=f"Time left: {count}s")
        sleep(1)
        count -= 1

    # Show time's up message
    if current_timer_number == my_number:
        countdown_label.config(text="Time's up!")


def compare_answers():
    """Compare user answers with correct answers and format results."""
    global quiz_result
    quiz_result = ""
    counter = 0

    # Check each answer
    for result in user_results:
        question = result["question"]
        correct_answer = result["correct_answer"]
        user_answer = result["user_answer"]

        # Determine if answer is correct, wrong, or not answered
        if user_answer == "":
            status = "Not answered"
        elif user_answer == correct_answer:
            status = "Correct"
            counter += 1
        else:
            status = "Wrong"

        # Build result text
        line = question + " | " + status
        quiz_result += line + "\n"

    # Add total score
    quiz_result += f"Total Score: {counter}/10"


def next_question_and_countdown():
    """Save current answer, move to next question, and start new timer."""
    global current_timer_number

    # Save the current answer
    part = {
        "question": quiz_questions[current_question]["question"],
        "correct_answer": quiz_questions[current_question]["correct_answer"],
        "user_answer": selection.get(),
    }
    user_results.append(part)

    # Stop old timer and start new one
    current_timer_number += 1
    next_question()

    if current_question < len(quiz_questions):
        start_new_thread(countdown, (start_count, current_timer_number))


def save_results():
    """Save quiz results to a file chosen by the user."""
    global quiz_result

    # Open save dialog
    file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")

    if file is None:
        return  # User cancelled

    # Write results and close file
    file.write(quiz_result)
    file.close()


# -----------------------------
# GUI Setup
# -----------------------------
app = Tk()
app.title("Quiz App")

# Load previous results if user wants to
filename = filedialog.askopenfilename(defaultextension=".txt")

if filename != "":
    # Read and display previous results
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    results_text = Text(app, height=15, width=80)
    results_text.pack(pady=10)
    results_text.insert("1.0", content)
    results_text.config(state="disabled")

# Question display area
question_label = Label(app, text="", font=("Arial", 12))
question_label.pack(pady=10)

# Timer display
countdown_label = Label(app, text="", font=("Arial", 10), fg="blue")
countdown_label.pack(pady=10)

# Answer options (radio buttons)
selection = StringVar()
radio_buttons = []
for i in range(4):
    rb = Radiobutton(app, text="", variable=selection, value="")
    rb.pack(anchor="w")
    radio_buttons.append(rb)

# Control buttons
next_button = Button(app, text="Next Question", command=next_question_and_countdown)
next_button.pack(pady=10)

save_button = Button(app, text="Save Results", command=save_results)
save_button.pack(pady=10)

# -----------------------------
# Start Quiz
# -----------------------------
show_question(0)
start_new_thread(countdown, (start_count, current_timer_number))

app.mainloop()

"""
Transferaufgabe 03.4.A.01
Task (EN): Develop a simple chatbot in Python that uses both rule-based and AI-based elements.
           The chatbot should be able to recognize and respond to simple greetings and answer a simple question
           about the current weather in a city by giving a fixed answer. Use a simple form of intent recognition for the AI-based
           elements to determine whether the user is saying a greeting or asking about the weather.
           a) Implement the basic structure of the chatbot, including a class for the chatbot that contains methods for processing input (input processing),
           recognizing intent (intent recognition) and generating responses (response generation).
           b) Add a method to the class that reacts rule-based to greetings such as "Hello" or "Good day" with a defined response, e.g. "Hello! How can I help you?".
           c) Integrate simple AI-based intent detection that checks whether a user input is a question about the weather. Use a simple query to check whether
           the string "weather" and the name of a city are included in the input. If yes, the chatbot should respond with a predefined answer, e.g. "It's sunny in
           Berlin today."
           d) Test your chatbot with different inputs to check whether it responds correctly to greetings and weather questions.
"""


class SimpleChatbot:
    def __init__(self):
        # Liste der erkannten Begrüßungen
        self.greetings = ["hallo", "guten tag", "hi"]
        # Liste der Städte für Wetterabfragen
        self.weather_cities = ["berlin", "münchen", "hamburg"]

    def process_input(self, user_input):
        """
        Verarbeitet die Benutzereingabe und erkennt die Absicht (Intent).
        Gibt die passende Antwort zurück.
        """
        user_input_lower = user_input.lower()

        # Regel-basiert: Prüfe auf Begrüßungen
        if any(greeting in user_input_lower for greeting in self.greetings):
            return self.generate_response("greeting")

        # KI-basiert: Prüfe auf Wetterfragen (einfache Intent-Erkennung)
        elif "wetter" in user_input_lower and any(
            city in user_input_lower for city in self.weather_cities
        ):
            return self.generate_response("weather", user_input_lower)

        else:
            return "Entschuldigung, ich habe das nicht verstanden."

    def generate_response(self, intent, user_input=None):
        """
        Generiert die Antwort basierend auf der erkannten Absicht.
        """
        if intent == "greeting":
            return "Hallo! Wie kann ich Ihnen helfen?"

        elif intent == "weather":
            # Finde die Stadt in der Benutzereingabe
            city = next(city for city in self.weather_cities if city in user_input)
            # Hier könnte eine echte Wetter-API integriert werden, um dynamische
            # Antworten zu generieren.
            return f"In {city.capitalize()} ist es heute sonnig."

        else:
            return "Entschuldigung, ich kann darauf nicht antworten."


# Beispiel für die Verwendung des Chatbots
bot = SimpleChatbot()

# Test 1: Einfache Begrüßung
print("Test 1:", bot.process_input("Hallo"))

# Test 2: Wetterabfrage
print("Test 2:", bot.process_input("Wie ist das Wetter in Berlin?"))

# Test 3: Andere Begrüßung
print("Test 3:", bot.process_input("Guten Tag"))

# Test 4: Wetterabfrage für München
print("Test 4:", bot.process_input("Wie ist das Wetter in München?"))

# Test 5: Wetterabfrage für Hamburg
print("Test 5:", bot.process_input("Wie ist das Wetter in Hamburg?"))

# Test 6: Begrüßung mit Großbuchstaben
print("Test 6:", bot.process_input("HI"))

# Test 7: Ungültige Eingabe
print("Test 7:", bot.process_input("Was ist 2 + 2?"))

# Test 8: Stadt ohne "wetter" im Satz
print("Test 8:", bot.process_input("Berlin"))

# Test 9: "Wetter" ohne Stadt
print("Test 9:", bot.process_input("Wie ist das Wetter?"))

# Test 10: Unbekannte Stadt
print("Test 10:", bot.process_input("Wie ist das Wetter in Paris?"))

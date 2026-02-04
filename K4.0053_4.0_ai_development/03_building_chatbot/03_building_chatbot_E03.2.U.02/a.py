"""
Ubung 3.2.U.02
Task (EN): Develop a simple, rule-based chatbot in Python that responds to specific keywords in user input.
           Your chatbot should be able to answer simple questions about the opening hours of a fictitious restaurant and the menu.
           Use the following steps for the development:
           a) Define a Python class called SimpleRestaurantBot In this class, you should implement a respond_to_user_input method
           that takes a user input as an argument.
           b) Within the respond_to_user_input method Implement a simple logic that checks for the keywords "opening hours" and "menu".
           If the user asks for the opening hours, the bot should respond with "Our restaurant is open daily from 12:00 to 23:00".
           If the user asks about the menu, the bot should reply: "You can find our menu on our website
           at www.beispielrestaurant.de/speisekarte."
           c) Test your implementation by calling the respond_to_user_input method with various user inputs containing the
           keywords "opening hours" and "menu" and check whether the bot's responses are correct.
"""


# Define a simple rule-based chatbot class for a restaurant
class SimpleRestaurantBot:  # Note: Fixed typo from "Bit" to "Bot"
    def __init__(self):
        # Initialize the chatbot with a dictionary of keywords and their responses
        # Keys are the keywords to search for in user input
        # Values are the responses the bot should return
        self.rules = {
            "opening hours": "Our restaurant is open daily from 12:00 to 23:00",
            "menu": "You can find our menu on our website at www.beispielrestaurant.de/speisekarte.",
        }

    def respond_to_user_input(self, user_input):
        # Convert user input to lowercase for case-insensitive matching
        input_lower = user_input.lower()

        # Iterate through each keyword in the rules dictionary
        for keyword in self.rules:
            # Get the response associated with this keyword
            response = self.rules[keyword]

            # Check if the keyword appears in the user's input
            if keyword in input_lower:
                # Return the matching response immediately (first match wins)
                return response

        # If no keywords matched, return a default response
        return "I'm sorry, I don't understand the question."


# Test the bot (this code only runs when the file is executed directly)
if __name__ == "__main__":
    # Create an instance of the chatbot
    bot = SimpleRestaurantBot()

    # Define test cases to verify the bot's behavior
    test_inputs = [
        "What are your opening hours?",  # Should match "opening hours"
        "OPENING HOURS",  # Test case insensitivity
        "Show me the menue please",  # Should match "menu" (despite typo in "menue")
        "What's on the menu",  # Should match "menu"
        "Do you have parking",  # Should return default response
        "Tell me your opening hours and menu",  # Should match first keyword found
    ]

    print("Testing SimpleRestaurantBot:\n")

    # Test each input and display the bot's response
    for test in test_inputs:
        response = bot.respond_to_user_input(test)
        print(f"User: {test}")
        print(f"Bot: {response}\n")

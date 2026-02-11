"""
Pizza Ordering Chatbot - Main Loop
Exercise 04.3.A.01 - Integration

This module integrates the three core components (intent recognition,
entity extraction, context management) into a functional chatbot with
an interactive conversation loop.
"""

from chatbot_components import recognize_intent, extract_entities, ContextManager


def main():
    """
    Main chatbot loop with debug mode.

    This function runs the interactive chatbot, processing user inputs
    through the three-component pipeline and maintaining conversation
    state across multiple turns.
    """
    # Configuration
    DEBUG_MODE = True  # Set to False to hide debug information

    # Initialize context manager
    context = ContextManager()

    # Welcome message
    print("=" * 60)
    print("PIZZA ORDERING CHATBOT")
    print("=" * 60)
    print("\nWelcome! I can help you order a pizza.")
    print("\nCommands:")
    print("  - Type 'quit' or 'exit' to end the conversation")
    print("  - Type 'debug' to toggle debug mode ON/OFF")
    print("  - Type 'reset' to start over")
    print("=" * 60)
    print(f"\nBot: {context.get_next_prompt()}")

    # Main conversation loop
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        # Handle empty input
        if not user_input:
            print("Bot: Please say something!")
            continue

        # Handle special commands
        if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            print("\nBot: Thank you for using the Pizza Ordering Chatbot! Goodbye!")
            break

        if user_input.lower() == "debug":
            DEBUG_MODE = not DEBUG_MODE
            status = "ON" if DEBUG_MODE else "OFF"
            print(f"\n[System] Debug mode is now {status}")
            continue

        if user_input.lower() == "reset":
            context.clear()
            print("\n[System] Conversation reset!")
            print(f"Bot: {context.get_next_prompt()}")
            continue

        # Process user input through the pipeline
        # Stage 1: Intent Recognition
        intent = recognize_intent(user_input, context.to_dict())

        # Stage 2: Entity Extraction
        entities = extract_entities(user_input)

        # Debug output - before context update
        if DEBUG_MODE:
            print("\n" + "-" * 60)
            print("[DEBUG] Processing Pipeline:")
            print(f"  Input: '{user_input}'")
            print(f"  Intent detected: {intent}")
            print(f"  Entities extracted: {entities}")
            print(f"  State BEFORE update: {context.get_state()}")
            print(f"  Entities BEFORE update: {context.get_entities()}")

        # Stage 3: Context Update
        context.update(intent, entities)

        # Debug output - after context update
        if DEBUG_MODE:
            print(f"  State AFTER update: {context.get_state()}")
            print(f"  Entities AFTER update: {context.get_entities()}")
            print(f"  Full context: {context.to_dict()}")
            print("-" * 60)

        # Stage 4: Response Generation
        # Handle special responses for certain intents
        if intent == "cancel_order":
            if context.get_state() == "idle":
                response = "Order cancelled! " + context.get_next_prompt()
            else:
                response = context.get_next_prompt()

        elif intent == "greeting":
            if context.get_state() == "idle":
                response = "Hello! " + context.get_next_prompt()
            else:
                response = f"Hi! You're currently ordering a pizza. {context.get_next_prompt()}"

        elif intent == "unknown":
            if context.get_state() == "idle":
                response = "I didn't understand that. " + context.get_next_prompt()
            else:
                response = f"I didn't understand that. {context.get_next_prompt()}"

        else:
            response = context.get_next_prompt()

        # Display bot response
        print(f"\nBot: {response}")


def run_demo_conversation():
    """
    Run a pre-scripted demo conversation for demonstration purposes.

    This function simulates a complete pizza ordering conversation,
    useful for testing and demonstration without manual input.
    """
    print("=" * 60)
    print("DEMO CONVERSATION")
    print("=" * 60)

    # Demo conversation script
    demo_script = [
        "Hello!",
        "I want to order a pizza",
        "Large",
        "Pepperoni and mushrooms",
        "yes",
    ]

    context = ContextManager()
    print(f"\nBot: {context.get_next_prompt()}")

    for user_input in demo_script:
        print(f"\nYou: {user_input}")

        # Process input
        intent = recognize_intent(user_input, context.to_dict())
        entities = extract_entities(user_input)

        print(f"  [Intent: {intent}, Entities: {entities}]")

        context.update(intent, entities)

        # Generate response
        if intent == "greeting":
            response = "Hello! " + context.get_next_prompt()
        else:
            response = context.get_next_prompt()

        print(f"Bot: {response}")
        print(
            f"  [State: {context.get_state()}, All entities: {context.get_entities()}]"
        )


if __name__ == "__main__":
    """
    Entry point when script is run directly.

    Uncomment the function you want to run:
    - main() for interactive chatbot
    - run_demo_conversation() for automated demo
    """
    # Run interactive chatbot
    # main()

    # OR run demo conversation (comment out main() above)
    run_demo_conversation()

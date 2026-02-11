"""
Pizza Ordering Chatbot - Core Components
Exercise 04.3.A.01 - Parts (b), (c), (d)

This module implements the three core components of the chatbot:
- Intent Recognition (Part b)
- Entity Extraction (Part c)
- Context Management (Part d)
"""

# ============================================================================
# PART (b): INTENT RECOGNITION
# ============================================================================

# Intent keywords mapping
INTENT_KEYWORDS = {
    "cancel_order": ["cancel", "stop", "nevermind", "never mind", "forget it"],
    "greeting": ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"],
    "order_pizza": ["pizza", "order", "want", "get", "buy"],
    "specify_size": ["small", "medium", "large"],
    "specify_toppings": ["pepperoni", "mushrooms", "cheese", "olives", "onions"],
}

# Intent priority order (highest to lowest)
INTENT_PRIORITY = [
    "cancel_order",  # Priority 1: Critical - must always work
    "greeting",  # Priority 2: Meta - conversation management
    "order_pizza",  # Priority 3: Primary - main action
    "specify_size",  # Priority 4: Contextual - depends on state
    "specify_toppings",  # Priority 5: Contextual - depends on state
]


def recognize_intent(user_input, context=None):
    """
    Recognize user intent from input text with context awareness.

    This function uses keyword-based matching with priority ordering.
    Low-priority intents (specify_size, specify_toppings) are validated
    against conversation context to handle ambiguous inputs.

    Args:
        user_input (str): Raw user input text
        context (dict, optional): Current conversation context with 'state' key

    Returns:
        str: Detected intent label or "unknown" if no match found

    Examples:
        >>> recognize_intent("I want to order a pizza")
        'order_pizza'
        >>> recognize_intent("Large", {"state": "awaiting_size"})
        'specify_size'
        >>> recognize_intent("Large", {"state": "idle"})
        'order_pizza'
    """
    # Normalize input: lowercase and strip whitespace
    normalized_input = user_input.lower().strip()

    # Check each intent in priority order
    for intent in INTENT_PRIORITY:
        keywords = INTENT_KEYWORDS[intent]

        # Check if any keyword is present in the input
        for keyword in keywords:
            if keyword in normalized_input:
                # For contextual intents, validate against context
                if intent in ["specify_size", "specify_toppings"]:
                    return _validate_contextual_intent(intent, context)
                else:
                    # Non-contextual intents return immediately
                    return intent

    # No intent matched
    return "unknown"


def _validate_contextual_intent(intent, context):
    """
    Validate contextual intents against conversation state.

    Helper function that determines if a contextual intent (specify_size,
    specify_toppings) is appropriate given the current conversation state.

    Args:
        intent (str): The contextual intent to validate
        context (dict): Current conversation context

    Returns:
        str: Validated intent (may return 'order_pizza' instead)
    """
    # If no context provided, treat as starting order with details
    if not context:
        return "order_pizza"

    current_state = context.get("state", "idle")

    # Validate specify_size intent
    if intent == "specify_size":
        if current_state == "awaiting_size":
            return "specify_size"  # Expected - we're asking for size
        elif current_state == "idle":
            return "order_pizza"  # User starting order with size
        else:
            return "specify_size"  # Allow modification (e.g., changing size)

    # Validate specify_toppings intent
    if intent == "specify_toppings":
        if current_state == "awaiting_toppings":
            return "specify_toppings"  # Expected - we're asking for toppings
        elif current_state == "idle":
            return "order_pizza"  # User starting order with toppings
        else:
            return "specify_toppings"  # Allow modification

    return intent


# ============================================================================
# PART (c): ENTITY EXTRACTION
# ============================================================================

# Entity keywords mapping
ENTITY_KEYWORDS = {
    "size": ["small", "medium", "large"],
    "toppings": ["pepperoni", "mushrooms", "cheese", "olives", "onions"],
}


def extract_entities(user_input):
    """
    Extract entities from user input text.

    This function uses rule-based pattern matching to identify and extract
    structured information (size and toppings) from user input. It operates
    independently of intent recognition.

    Args:
        user_input (str): Raw user input text

    Returns:
        dict: Dictionary of extracted entities with structure:
              - "size": str (e.g., "large") - only one size allowed
              - "toppings": list of str (e.g., ["pepperoni", "mushrooms"])
              Empty dict {} if no entities found

    Examples:
        >>> extract_entities("I want a large pizza")
        {'size': 'large'}
        >>> extract_entities("Pepperoni and mushrooms")
        {'toppings': ['pepperoni', 'mushrooms']}
        >>> extract_entities("Large with pepperoni")
        {'size': 'large', 'toppings': ['pepperoni']}
    """
    # Initialize empty entities dictionary
    entities = {}

    # Normalize input: lowercase
    normalized_input = user_input.lower().strip()

    # Extract size entity (only one size allowed, last match wins)
    size_keywords = ENTITY_KEYWORDS["size"]
    for size_keyword in size_keywords:
        if size_keyword in normalized_input:
            entities["size"] = size_keyword  # Overwrite if multiple found

    # Extract toppings entities (multiple toppings allowed)
    toppings_keywords = ENTITY_KEYWORDS["toppings"]
    found_toppings = []
    for topping_keyword in toppings_keywords:
        if topping_keyword in normalized_input:
            found_toppings.append(topping_keyword)

    # Only add toppings to entities if at least one was found
    if found_toppings:
        entities["toppings"] = found_toppings

    return entities


# ============================================================================
# PART (d): CONTEXT MANAGEMENT
# ============================================================================


class ContextManager:
    """
    Manages conversation state and context for the chatbot.

    This class implements a finite state machine (FSM) for conversation flow,
    storing the current intent, dialogue state, and collected entities.
    It handles state transitions based on user intents and extracted entities.

    States:
        - idle: No active conversation
        - awaiting_size: Order started, waiting for pizza size
        - awaiting_toppings: Size received, waiting for toppings
        - ready_to_confirm: All info collected, ready to confirm order
    """

    def __init__(self):
        """
        Initialize empty context.

        Sets up initial state with no active intent, idle state,
        and empty entities dictionary.
        """
        self.current_intent = None
        self.state = "idle"
        self.entities = {}

    def update(self, intent, entities):
        """
        Update context with new intent and entities.

        This method implements the state transition logic based on the
        detected intent and extracted entities. It handles:
        - Critical intents (cancel_order)
        - Order flow progression
        - Entity storage
        - Skip-ahead logic (when multiple entities provided at once)

        Args:
            intent (str): Detected intent from intent recognition
            entities (dict): Extracted entities from entity extraction
        """
        # Handle critical intents first
        if intent == "cancel_order":
            self.clear()
            return

        # Handle greeting (acknowledge but don't change state)
        if intent == "greeting":
            # Greeting doesn't change state, just acknowledged
            return

        # Handle unknown intent
        if intent == "unknown":
            # Don't change state for unknown inputs
            return

        # Handle order flow based on current state
        if self.state == "idle":
            self._handle_idle_state(intent, entities)

        elif self.state == "awaiting_size":
            self._handle_awaiting_size_state(intent, entities)

        elif self.state == "awaiting_toppings":
            self._handle_awaiting_toppings_state(intent, entities)

        elif self.state == "ready_to_confirm":
            self._handle_ready_to_confirm_state(intent, entities)

    def _handle_idle_state(self, intent, entities):
        """Handle updates when in idle state."""
        if intent == "order_pizza" or intent in ["specify_size", "specify_toppings"]:
            # Start order
            self.current_intent = "order_pizza"
            self.state = "awaiting_size"

            # Check if size already provided (skip-ahead)
            if "size" in entities:
                self.entities["size"] = entities["size"]
                self.state = "awaiting_toppings"

                # Check if toppings also provided (double skip-ahead)
                if "toppings" in entities:
                    self.entities["toppings"] = entities["toppings"]
                    self.state = "ready_to_confirm"

    def _handle_awaiting_size_state(self, intent, entities):
        """Handle updates when awaiting size."""
        # Store size if provided
        if "size" in entities:
            self.entities["size"] = entities["size"]
            self.state = "awaiting_toppings"

            # Check if toppings also provided (skip-ahead)
            if "toppings" in entities:
                self.entities["toppings"] = entities["toppings"]
                self.state = "ready_to_confirm"

    def _handle_awaiting_toppings_state(self, intent, entities):
        """Handle updates when awaiting toppings."""
        # Store toppings if provided
        if "toppings" in entities:
            # If toppings already exist, append new ones
            if "toppings" in self.entities:
                existing_toppings = self.entities["toppings"]
                new_toppings = entities["toppings"]
                # Combine and remove duplicates
                combined = list(set(existing_toppings + new_toppings))
                self.entities["toppings"] = combined
            else:
                self.entities["toppings"] = entities["toppings"]

            self.state = "ready_to_confirm"

        # Allow size modification
        if "size" in entities:
            self.entities["size"] = entities["size"]
            # Stay in awaiting_toppings state

    def _handle_ready_to_confirm_state(self, intent, entities):
        """Handle updates when ready to confirm."""
        # Allow modifications
        if "size" in entities:
            self.entities["size"] = entities["size"]

        if "toppings" in entities:
            # Replace toppings with new selection
            self.entities["toppings"] = entities["toppings"]

        # Stay in ready_to_confirm state
        # (Actual confirmation would be handled by checking for confirmation keywords)

    def get_state(self):
        """
        Return current dialogue state.

        Returns:
            str: Current state (idle, awaiting_size, awaiting_toppings, ready_to_confirm)
        """
        return self.state

    def get_entities(self):
        """
        Return collected entities.

        Returns:
            dict: Dictionary of collected entities
        """
        return self.entities.copy()

    def clear(self):
        """
        Reset context to initial state.

        Clears all stored information and returns to idle state.
        Used when order is cancelled or completed.
        """
        self.current_intent = None
        self.state = "idle"
        self.entities = {}

    def get_next_prompt(self):
        """
        Generate appropriate bot response based on current state.

        This method determines what the bot should say next based on
        the current dialogue state and collected entities.

        Returns:
            str: Bot response text appropriate for current state
        """
        if self.state == "idle":
            return "How can I help you? Say 'order pizza' to start an order!"

        elif self.state == "awaiting_size":
            return "What size pizza would you like? We have small, medium, and large."

        elif self.state == "awaiting_toppings":
            return "What toppings would you like? We have pepperoni, mushrooms, cheese, olives, and onions."

        elif self.state == "ready_to_confirm":
            size = self.entities.get("size", "unknown size")
            toppings = self.entities.get("toppings", [])

            if toppings:
                toppings_str = ", ".join(toppings)
                return f"Perfect! I have a {size} pizza with {toppings_str}. Say 'yes' to confirm or 'cancel' to cancel."
            else:
                return f"I have a {size} pizza with no toppings. Say 'yes' to confirm or 'cancel' to cancel."

        return "I'm not sure what to say next."

    def to_dict(self):
        """
        Return context as dictionary for inspection/debugging.

        Returns:
            dict: Complete context state including intent, state, and entities
        """
        return {
            "current_intent": self.current_intent,
            "state": self.state,
            "entities": self.entities.copy(),
        }


# ============================================================================
# TEST FUNCTIONS
# ============================================================================


def test_intent_recognition():
    """Test intent recognition with various inputs."""
    print("=" * 60)
    print("TESTING INTENT RECOGNITION")
    print("=" * 60)

    test_cases = [
        # (input, context, expected_intent)
        ("I want to order a pizza", None, "order_pizza"),
        ("Cancel my order", {"state": "awaiting_size"}, "cancel_order"),
        ("Hello", None, "greeting"),
        ("Hi there", None, "greeting"),
        ("Large", {"state": "awaiting_size"}, "specify_size"),
        ("Large", {"state": "idle"}, "order_pizza"),
        ("Large pizza please", None, "order_pizza"),
        ("Pepperoni", {"state": "awaiting_toppings"}, "specify_toppings"),
        ("Pepperoni pizza", {"state": "idle"}, "order_pizza"),
        ("Random text xyz", None, "unknown"),
        ("Stop", {"state": "awaiting_toppings"}, "cancel_order"),
    ]

    for i, (input_text, context, expected) in enumerate(test_cases, 1):
        result = recognize_intent(input_text, context)
        status = "✓" if result == expected else "✗"
        print(f"{status} Test {i}: '{input_text}'")
        print(f"   Context: {context}")
        print(f"   Expected: {expected}, Got: {result}")
        print()


def test_entity_extraction():
    """Test entity extraction with various inputs."""
    print("=" * 60)
    print("TESTING ENTITY EXTRACTION")
    print("=" * 60)

    test_cases = [
        # (input, expected_entities)
        ("I want a large pizza", {"size": "large"}),
        ("Pepperoni and mushrooms", {"toppings": ["pepperoni", "mushrooms"]}),
        ("Large with pepperoni", {"size": "large", "toppings": ["pepperoni"]}),
        ("Hello", {}),
        ("Small no wait medium pizza", {"size": "medium"}),  # Last wins
        (
            "Cheese pepperoni and olives",
            {"toppings": ["cheese", "pepperoni", "olives"]},
        ),
        (
            "Medium pizza with cheese, mushrooms, and onions",
            {"size": "medium", "toppings": ["cheese", "mushrooms", "onions"]},
        ),
    ]

    for i, (input_text, expected) in enumerate(test_cases, 1):
        result = extract_entities(input_text)
        status = "✓" if result == expected else "✗"
        print(f"{status} Test {i}: '{input_text}'")
        print(f"   Expected: {expected}")
        print(f"   Got: {result}")
        print()


def test_context_management():
    """Test context management with conversation flows."""
    print("=" * 60)
    print("TESTING CONTEXT MANAGEMENT")
    print("=" * 60)

    # Test 1: Normal flow
    print("\nTest 1: Normal conversation flow")
    print("-" * 40)
    context = ContextManager()
    print(f"Initial state: {context.get_state()}")

    context.update("order_pizza", {})
    print(f"After 'order pizza': {context.get_state()}")

    context.update("specify_size", {"size": "large"})
    print(f"After 'large': {context.get_state()}, entities: {context.get_entities()}")

    context.update("specify_toppings", {"toppings": ["pepperoni"]})
    print(
        f"After 'pepperoni': {context.get_state()}, entities: {context.get_entities()}"
    )

    # Test 2: Skip-ahead
    print("\n\nTest 2: Skip-ahead (provide all info at once)")
    print("-" * 40)
    context2 = ContextManager()
    context2.update(
        "order_pizza", {"size": "medium", "toppings": ["cheese", "mushrooms"]}
    )
    print(f"State: {context2.get_state()}, entities: {context2.get_entities()}")

    # Test 3: Cancel
    print("\n\nTest 3: Cancel order")
    print("-" * 40)
    context3 = ContextManager()
    context3.update("order_pizza", {"size": "large"})
    print(f"Before cancel: {context3.get_state()}")
    context3.update("cancel_order", {})
    print(f"After cancel: {context3.get_state()}, entities: {context3.get_entities()}")

    # Test 4: Modification
    print("\n\nTest 4: Modify size while awaiting toppings")
    print("-" * 40)
    context4 = ContextManager()
    context4.update("order_pizza", {"size": "small"})
    print(
        f"After ordering small: {context4.get_state()}, size: {context4.get_entities()}"
    )
    context4.update("specify_size", {"size": "large"})
    print(
        f"After changing to large: {context4.get_state()}, size: {context4.get_entities()}"
    )


if __name__ == "__main__":
    """Run all tests when module is executed directly."""
    test_intent_recognition()
    print("\n")
    test_entity_extraction()
    print("\n")
    test_context_management()

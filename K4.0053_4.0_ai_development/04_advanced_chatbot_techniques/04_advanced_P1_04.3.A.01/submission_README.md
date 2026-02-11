# Exercise 04.3.A.01 - Simple AI-Based Chatbot (Partial Exam 1)

---

## Overview

This exercise implements a simple AI-based pizza ordering chatbot with three core components: **intent recognition**, **entity extraction**, and **context management**. The chatbot demonstrates fundamental NLU (Natural Language Understanding) principles using keyword-based pattern matching and finite state machine architecture.

---

## Part (a): Architecture Design

### System Components

The chatbot architecture consists of three tightly integrated components:

#### 1. Intent Recognition
**Purpose:** Identifies user's goal from their message using priority-based keyword matching.

**Key Features:**
- 6 predefined intents with priority ordering (cancel_order → greeting → order_pizza → specify_size → specify_toppings → unknown)
- Context-aware validation for ambiguous inputs
- Dual-role keywords (serve as both intent triggers and entity values)

**Example:**
```
Input: "Large" 
Context: awaiting_size → Intent: specify_size
Context: idle → Intent: order_pizza (user starting with details)
```

#### 2. Entity Extraction
**Purpose:** Extracts structured information (size, toppings) from user input.

**Key Features:**
- Rule-based pattern matching with predefined keyword lists
- Operates independently of intent recognition
- Supports multiple entities per input (e.g., "large with pepperoni and mushrooms")

**Supported Entities:**
- `size`: small, medium, large (single value, last match wins)
- `toppings`: pepperoni, mushrooms, cheese, olives, onions (multiple values allowed)

#### 3. Context Management
**Purpose:** Maintains conversation state across multiple turns using finite state machine (FSM).

**States:**
- `idle` - No active conversation
- `awaiting_size` - Order started, needs size
- `awaiting_toppings` - Size received, needs toppings  
- `ready_to_confirm` - All info collected, ready to confirm

**Key Features:**
- Skip-ahead logic (advance multiple states if user provides multiple entities)
- Modification support (allows changing previously provided information)
- Critical intent priority (cancel_order overrides normal flow)

### Component Interaction Flow

```
User Input → Intent Recognition → Entity Extraction → Context Update → Response Generation
```

**Example Conversation:**
1. User: "I want to order a pizza" → Intent: order_pizza, State: idle → awaiting_size
2. User: "Large" → Intent: specify_size, Entity: {size: "large"}, State: awaiting_size → awaiting_toppings
3. User: "Pepperoni and mushrooms" → Intent: specify_toppings, Entities: {toppings: ["pepperoni", "mushrooms"]}, State: awaiting_toppings → ready_to_confirm

### State Transition Table (Key Transitions)

| Current State      | Intent + Entities           | Next State         |
|--------------------|-----------------------------|---------------------|
| idle               | order_pizza                 | awaiting_size      |
| awaiting_size      | specify_size + size entity  | awaiting_toppings  |
| awaiting_toppings  | specify_toppings + toppings | ready_to_confirm   |
| any state          | cancel_order                | idle               |

### Design Principles

**Priority-Based Intent Resolution:**
- Critical intents (cancel) checked first, then meta (greeting), then primary (order_pizza), then contextual (size/toppings)
- Context validation prevents misinterpretation of ambiguous inputs

**Dual-Role Keywords:**
- Keywords like "large" serve as both intent triggers and entity values
- Both components process input independently, results combined in context update
- Mirrors production NLU systems (Dialogflow, Rasa)

**Skip-Ahead Capability:**
- User can provide multiple details at once: "Large pepperoni pizza"
- System extracts all entities and advances directly to appropriate state
- Enables natural, efficient conversations

---

## Part (b): Intent Recognition Implementation

### Data Structures
```python
INTENT_KEYWORDS = {
    "cancel_order": ["cancel", "stop", "nevermind"],
    "greeting": ["hi", "hello", "hey"],
    "order_pizza": ["pizza", "order", "want", "get"],
    "specify_size": ["small", "medium", "large"],
    "specify_toppings": ["pepperoni", "mushrooms", "cheese", "olives", "onions"],
}

INTENT_PRIORITY = [
    "cancel_order", "greeting", "order_pizza", 
    "specify_size", "specify_toppings"
]
```

### Function Signature
```python
def recognize_intent(user_input, context=None) -> str:
    """
    Recognize intent with context-aware validation.
    Returns: intent label or "unknown"
    """
```

### Algorithm
1. Normalize input (lowercase, strip whitespace)
2. Check each intent in priority order
3. For contextual intents (specify_size, specify_toppings):
   - Validate against conversation state
   - Return order_pizza if user starting with details
4. Return first matching intent or "unknown"

### Key Implementation Detail: Context Validation
```python
def _validate_contextual_intent(intent, context):
    """Validate contextual intents against state."""
    if intent == "specify_size":
        if context.state == "awaiting_size":
            return "specify_size"  # Expected
        elif context.state == "idle":
            return "order_pizza"  # Starting with size
        else:
            return "specify_size"  # Modification
```

---

## Part (c): Entity Extraction Implementation

### Data Structures
```python
ENTITY_KEYWORDS = {
    "size": ["small", "medium", "large"],
    "toppings": ["pepperoni", "mushrooms", "cheese", "olives", "onions"],
}
```

### Function Signature
```python
def extract_entities(user_input) -> dict:
    """
    Extract entities using rule-based pattern matching.
    Returns: {"size": str, "toppings": list} or empty dict
    """
```

### Algorithm
1. Normalize input (lowercase)
2. Scan for size keywords (store last match if multiple)
3. Scan for toppings keywords (collect all matches in list)
4. Return dictionary with found entities

### Key Features
- **Independence:** Operates separately from intent recognition
- **Multiple toppings:** Collected in list, duplicates allowed
- **Single size:** Last mentioned value used if multiple provided
- **Exact matches only:** "large" matches, "extra-large" does not

---

## Part (d): Context Management Implementation

### Class Structure
```python
class ContextManager:
    def __init__(self):
        """Initialize: state="idle", entities={}"""
    
    def update(self, intent, entities):
        """Update context based on intent and entities"""
    
    def get_state(self) -> str:
        """Return current dialogue state"""
    
    def get_next_prompt(self) -> str:
        """Generate bot response for current state"""
    
    def clear(self):
        """Reset to idle state"""
```

### State Transition Logic

**Idle State:**
```python
if intent == "order_pizza":
    state = "awaiting_size"
    if "size" in entities:
        state = "awaiting_toppings"
        if "toppings" in entities:
            state = "ready_to_confirm"  # Skip-ahead
```

**Awaiting Size:**
```python
if "size" in entities:
    store_size()
    state = "awaiting_toppings"
    if "toppings" in entities:
        state = "ready_to_confirm"  # Skip-ahead
```

**Awaiting Toppings:**
```python
if "toppings" in entities:
    store_toppings()
    state = "ready_to_confirm"
if "size" in entities:
    update_size()  # Allow modification
```

### Response Generation
```python
def get_next_prompt(self):
    if state == "awaiting_size":
        return "What size? (small, medium, large)"
    elif state == "awaiting_toppings":
        return "What toppings? (pepperoni, mushrooms, cheese, olives, onions)"
    elif state == "ready_to_confirm":
        return f"I have {size} with {toppings}. Confirm? (yes/cancel)"
```

---

## Implementation Files

### `chatbot_components.py`
Contains all three components:
- Intent recognition function with context validation
- Entity extraction function with dual-role keyword support
- ContextManager class with FSM implementation
- Comprehensive test functions for each component

### `chatbot_main.py`
Integration and main loop:
- Interactive chatbot with debug mode
- Four-stage processing pipeline
- Special command handling (quit, debug, reset)
- Demo conversation function

---

## Testing Results

### Intent Recognition Tests
✓ All priority-based matches working correctly  
✓ Context validation prevents ambiguous interpretations  
✓ Dual-role keywords handled properly  

### Entity Extraction Tests
✓ Single and multiple entity extraction working  
✓ Multiple toppings collected correctly  
✓ Last-value-wins for size conflicts  

### Context Management Tests
✓ State transitions follow FSM rules  
✓ Skip-ahead logic advances multiple states  
✓ Modifications update context correctly  
✓ Cancel clears context properly  

### Integration Tests
✓ Normal conversation flow: idle → awaiting_size → awaiting_toppings → ready_to_confirm  
✓ Skip-ahead: "Large pepperoni pizza" → ready_to_confirm directly  
✓ Modifications: Changing size while awaiting toppings  
✓ Cancel at any state returns to idle  

---

## Files Submitted

1. **chatbot_components.py** - Core components implementation (Parts b, c, d)
2. **chatbot_main.py** - Integration and interactive loop
3. **README.md** - This documentation

---

## How to Run

```bash
# Test individual components
python chatbot_components.py

# Run interactive chatbot
python chatbot_main.py

# Commands in chatbot:
# - 'debug' - Toggle debug mode
# - 'reset' - Start new conversation
# - 'quit' - Exit
```

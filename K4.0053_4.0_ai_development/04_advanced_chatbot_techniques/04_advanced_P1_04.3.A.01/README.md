# Exercise 04.3.A.01 – Part (a): Chatbot Architecture

## Overview

This document describes the architecture of a simple AI-based chatbot designed for pizza ordering. The chatbot consists of three core components working together to enable natural, multi-turn conversations: **intent recognition**, **entity extraction**, and **context management**. These components process user input, maintain conversation state, and generate appropriate responses.

**Key Design Principles:**
- Beginner-friendly implementation using keyword-based rules
- Context-aware intent resolution for handling ambiguous inputs
- Finite state machine for conversation flow management
- Modular architecture allowing independent component testing

---

## 1. Intent Recognition

### Purpose
The intent recognition component identifies the **user's goal or intention** from their message. This determines what action the chatbot should take.

### How It Works
Intent recognition uses a **keyword-based approach with priority ordering**. User input is normalized (lowercased, punctuation removed) and scanned for keywords associated with predefined intents.

**Key Features:**
- **Priority-based matching:** Intents are evaluated in a fixed priority order to resolve conflicts when multiple intents match
- **Context-aware resolution:** Low-priority intents (specify_size, specify_toppings) are validated against conversation context
- **Dual-role keywords:** Some keywords serve both as intent triggers and entity values (e.g., "large" triggers specify_size and represents a size entity)

### Supported Intents

The chatbot recognizes six intents with the following priority order:

| Priority | Intent           | Purpose                              | Example Keywords          |
|----------|------------------|--------------------------------------|---------------------------|
| 1        | cancel_order     | Cancel current order (critical)      | cancel, stop, nevermind   |
| 2        | greeting         | Start/acknowledge conversation       | hi, hello, hey            |
| 3        | order_pizza      | Initiate pizza order                 | pizza, order, want, get   |
| 4        | specify_size     | Provide pizza size (context-dependent)| small, medium, large      |
| 5        | specify_toppings | Provide toppings (context-dependent) | pepperoni, mushrooms, cheese |
| 6        | unknown          | Fallback for unrecognized input      | (no keywords match)       |

### Intent Priority Rationale

**Tier 1: Critical Intents** (cancel_order)
- Must work at any time in the conversation
- User safety and control priority
- Overrides all other intents

**Tier 2: Meta Intents** (greeting)
- Conversation management
- Can occur at any point without disrupting order flow
- Acknowledged but doesn't change conversation state

**Tier 3: Primary Intent** (order_pizza)
- Main action trigger
- Higher priority than detail-specification intents

**Tier 4: Contextual Intents** (specify_size, specify_toppings)
- Lowest priority in keyword matching
- **Context-aware validation:** Only accepted when context expects them
- If detected outside expected context, may indicate user starting order with details

**Tier 5: Fallback** (unknown)
- Default when no keywords match
- Prompts user for clarification based on current conversation state

### Context-Aware Intent Resolution

When low-priority intents (specify_size, specify_toppings) are detected, the chatbot validates them against conversation context:

**Example 1: Expected Context**
```
Context state: awaiting_size
User input: "Large"
Keywords match: specify_size
Validation: Context expects size → ACCEPT specify_size intent
```

**Example 2: Unexpected Context**
```
Context state: idle
User input: "Large pepperoni pizza"
Keywords match: order_pizza (pizza), specify_size (large), specify_toppings (pepperoni)
Priority order: order_pizza wins
Result: Intent = order_pizza, but entities (size, toppings) still extracted
```

**Example 3: Conflict Resolution**
```
Context state: awaiting_toppings
User input: "Actually, make it large"
Keywords match: specify_size (large)
Validation: Context expects toppings, not size → Interpret as modification request
Result: Intent = specify_size, update size entity, maintain conversation flow
```

### Input / Output

**Input:**
- Raw user text (string)
- Current conversation context (for validation)

**Output:**
- Single intent label (string)

---

## 2. Entity Extraction

### Purpose
The entity extraction component identifies and extracts **structured information** from user input that is required to fulfill their request.

### How It Works
Entity extraction uses **rule-based pattern matching** with predefined keyword lists. It operates **independently** of intent recognition, scanning every user input for known entity values regardless of detected intent. This allows the chatbot to capture information even from ambiguous or unexpected inputs.

**Key Features:**
- **Intent-independent operation:** Extracts entities from all inputs
- **Multiple entity support:** Single message can contain multiple entity types
- **Dual-role keywords:** Entity keywords may also serve as intent triggers
- **List aggregation:** Multiple values of same entity type collected in lists

### Supported Entities

The chatbot extracts two entity types:

| Entity Type | Possible Values                              | Example Extraction               |
|-------------|----------------------------------------------|----------------------------------|
| size        | small, medium, large                         | "large" → {size: "large"}        |
| toppings    | pepperoni, mushrooms, cheese, olives, onions | "pepperoni and mushrooms" → {toppings: ["pepperoni", "mushrooms"]} |

### Entity Validation Rules

- **Exact matches only:** "large" matches, "extra-large" does not
- **Case-insensitive:** "Large", "LARGE", "large" all match
- **Invalid values ignored:** Unknown entity values not stored
- **Multiple toppings allowed:** Collected in a list
- **Single size only:** Last mentioned size value used if multiple provided

### Relationship with Intent Recognition

Entity extraction and intent recognition work **in parallel**, both processing the same user input:

**Dual-Role Keywords:**
- Some keywords serve both as **intent triggers** (for intent recognition) and **entity values** (for entity extraction)
- Example: "large" triggers `specify_size` intent AND represents `size: "large"` entity

**Example Flow:**
```
User: "I want a large pepperoni pizza"

Intent Recognition:
- Keywords found: "want" (order_pizza), "large" (specify_size), "pepperoni" (specify_toppings), "pizza" (order_pizza)
- Priority order: order_pizza (highest match)
- Result: Intent = order_pizza

Entity Extraction:
- Keywords found: "large" (size entity), "pepperoni" (toppings entity)
- Result: Entities = {size: "large", toppings: ["pepperoni"]}

Both components succeed independently, results combined in context update.
```

### Handling Multiple Entities

The chatbot can extract multiple entities from a single user message:

**Example 1: Size and Toppings Together**
```
User: "Large with pepperoni and mushrooms"
Extracted: {size: "large", toppings: ["pepperoni", "mushrooms"]}
```

**Example 2: Multiple Toppings Only**
```
User: "Pepperoni, mushrooms, and cheese"
Extracted: {toppings: ["pepperoni", "mushrooms", "cheese"]}
```

**Example 3: No Entities**
```
User: "Hello"
Extracted: {} (empty dictionary)
```

### Input / Output

**Input:**
- Raw user text (string)

**Output:**
- Dictionary of extracted entities (e.g., `{size: "large", toppings: ["pepperoni"]}`)
- Empty dictionary `{}` if no entities found

---

## 3. Context Management

### Purpose
The context management component maintains **conversation state** across multiple turns, allowing the chatbot to remember previous inputs, track dialogue progress, and interpret short or ambiguous user messages correctly.

### Definition of Context

Context represents the **current state of the conversation**, not the full chat history. It is a lightweight data structure that stores:
- What the user is trying to do (current intent)
- Where we are in the conversation flow (dialogue state)
- What information has been collected so far (entities)

**Context is NOT:**
- A full transcript of the conversation
- A database of all user interactions
- Permanent storage (context is cleared when conversation ends)

### Context Structure

The context object uses a **flat dictionary structure** for simplicity:
```python
context = {
    "current_intent": "order_pizza",           # Active intent
    "state": "awaiting_toppings",              # Dialogue state
    "entities": {                               # Collected information
        "size": "large",
        "toppings": ["pepperoni"]
    }
}
```

**Field Descriptions:**

| Field          | Type   | Purpose                                           | Example Values                    |
|----------------|--------|---------------------------------------------------|-----------------------------------|
| current_intent | string | The active user intent                            | "order_pizza", "cancel_order"     |
| state          | string | Current position in conversation flow             | "idle", "awaiting_size", "ready_to_confirm" |
| entities       | dict   | All entities collected during current conversation| {size: "large", toppings: [...]}  |

### Dialogue States

The chatbot uses a **finite state machine (FSM)** with four states:

| State              | Meaning                                      | Next Action                    |
|--------------------|----------------------------------------------|--------------------------------|
| idle               | No active conversation                       | Wait for order_pizza intent    |
| awaiting_size      | Order started, need pizza size               | Prompt for size                |
| awaiting_toppings  | Size received, need toppings                 | Prompt for toppings            |
| ready_to_confirm   | All info collected, awaiting confirmation    | Show order summary, ask confirm|

### State Transition Table

This table defines **all valid transitions** between states based on user inputs:

| Current State      | Event (Intent + Entities)        | Actions Taken                     | Next State         |
|--------------------|----------------------------------|-----------------------------------|--------------------|
| **idle**           |                                  |                                   |                    |
| idle               | order_pizza                      | Initialize order context          | awaiting_size      |
| idle               | order_pizza + size entity        | Store size, initialize order      | awaiting_toppings  |
| idle               | order_pizza + size + toppings    | Store all, initialize order       | ready_to_confirm   |
| idle               | greeting                         | Respond with greeting             | idle               |
| idle               | cancel_order                     | "No active order to cancel"       | idle               |
| idle               | unknown                          | "How can I help you?"             | idle               |
| **awaiting_size**  |                                  |                                   |                    |
| awaiting_size      | specify_size + size entity       | Store size                        | awaiting_toppings  |
| awaiting_size      | order_pizza + size entity        | Store size                        | awaiting_toppings  |
| awaiting_size      | cancel_order                     | Clear context, "Order cancelled"  | idle               |
| awaiting_size      | greeting                         | "Hi! What size pizza?"            | awaiting_size      |
| awaiting_size      | unknown                          | "Please specify: small, medium, or large" | awaiting_size |
| **awaiting_toppings** |                               |                                   |                    |
| awaiting_toppings  | specify_toppings + toppings      | Store toppings                    | ready_to_confirm   |
| awaiting_toppings  | order_pizza + toppings           | Store toppings                    | ready_to_confirm   |
| awaiting_toppings  | specify_size + size entity       | Update size (modification)        | awaiting_toppings  |
| awaiting_toppings  | cancel_order                     | Clear context, "Order cancelled"  | idle               |
| awaiting_toppings  | unknown                          | "What toppings would you like?"   | awaiting_toppings  |
| **ready_to_confirm** |                                |                                   |                    |
| ready_to_confirm   | confirm (yes/ok/confirm)         | Place order, "Order confirmed!"   | idle               |
| ready_to_confirm   | cancel_order                     | Clear context, "Order cancelled"  | idle               |
| ready_to_confirm   | specify_size + size entity       | Update size, back to confirm      | ready_to_confirm   |
| ready_to_confirm   | specify_toppings + toppings      | Update toppings, back to confirm  | ready_to_confirm   |
| ready_to_confirm   | unknown                          | "Say 'yes' to confirm or 'cancel' to cancel" | ready_to_confirm |

### Context Update Strategy

Context updates follow these rules:

1. **Immediate entity storage:** When entities are extracted, add them to context immediately
2. **State progression:** When required information is collected, advance to next state
3. **Allow skip-ahead:** If multiple entities provided at once, skip intermediate states
4. **Modification support:** Allow users to change previously provided information
5. **Critical intent priority:** cancel_order and greeting override normal flow

**Example: Skip-Ahead Logic**
```
State: awaiting_size
User: "Large with pepperoni and mushrooms"
Entities: {size: "large", toppings: ["pepperoni", "mushrooms"]}

Context Update:
1. Store size entity → would advance to awaiting_toppings
2. Detect toppings also provided → skip awaiting_toppings
3. Advance directly to ready_to_confirm

Result: Single input completes multiple steps
```

### Role in Conversation Flow

Context enables the chatbot to:

1. **Interpret ambiguous inputs**
   - "Large" → Context knows we're awaiting size → Interpret as size specification

2. **Track conversation progress**
   - Context state determines what to ask next

3. **Handle modifications**
   - User changes size after already providing it → Context updates, maintains flow

4. **Maintain conversation coherence**
   - Context prevents asking for information already provided

5. **Enable natural multi-turn dialogue**
   - Users don't need to repeat information across turns

### Input / Output

**Input:**
- Detected intent (from intent recognition)
- Extracted entities (from entity extraction)
- Current context state

**Output:**
- Updated context object
- Determination of next bot action (prompt, confirm, cancel, etc.)

---

## 4. Component Interaction (End-to-End Flow)

### Processing Pipeline

When a user sends a message, the chatbot processes it through four stages:
```
User Input → [1. Intent Recognition] → [2. Entity Extraction] → [3. Context Update] → [4. Response Generation]
                      ↓                         ↓                         ↓                    ↓
                  Intent label            Entities dict             Updated context      Bot response
```

### Detailed Flow

**Stage 1: Intent Recognition**
- Input: Raw user text + current context
- Process: Scan for intent keywords with priority ordering
- Validate: Check if low-priority intents match context expectations
- Output: Single intent label

**Stage 2: Entity Extraction**
- Input: Raw user text (same input, processed independently)
- Process: Scan for entity keywords using predefined lists
- Extract: Collect all matching entities (multiple allowed)
- Output: Entities dictionary (may be empty)

**Stage 3: Context Update**
- Input: Intent label + entities dict + current context
- Process: 
  - Update entities in context
  - Determine next dialogue state based on state transition table
  - Handle special cases (cancel, modifications)
- Output: Updated context object

**Stage 4: Response Generation**
- Input: Updated context
- Process: Generate appropriate response based on:
  - Current dialogue state
  - Missing vs. collected information
  - Detected intent
- Output: Bot response text

### Error Handling

**Unknown Intent:**
- Intent recognition returns "unknown"
- Entity extraction still attempted (may capture useful info)
- Context NOT cleared (preserve conversation state)
- Response: Ask for clarification based on current state

**Invalid Entities:**
- Entity values not in predefined lists are ignored
- Context remains unchanged for invalid values
- Response: Prompt for valid options

**Context Conflicts:**
- Example: specify_size detected while awaiting_toppings
- Interpretation: User modifying previous choice
- Action: Update size entity, maintain conversation state
- Response: Acknowledge modification, continue flow

### Example End-to-End Execution

**Turn 1:**
```
User: "I want to order a pizza"

Stage 1 - Intent Recognition:
- Keywords: "want" (order_pizza), "order" (order_pizza), "pizza" (order_pizza)
- Priority: order_pizza (rank 3)
- Output: Intent = "order_pizza"

Stage 2 - Entity Extraction:
- Scan for size: none found
- Scan for toppings: none found
- Output: Entities = {}

Stage 3 - Context Update:
- Current state: idle
- Transition: idle + order_pizza → awaiting_size
- Update context: {current_intent: "order_pizza", state: "awaiting_size", entities: {}}

Stage 4 - Response Generation:
- State: awaiting_size
- Missing: size entity
- Response: "What size pizza would you like? We have small, medium, and large."
```

**Turn 2:**
```
User: "Large"
Context: {current_intent: "order_pizza", state: "awaiting_size", entities: {}}

Stage 1 - Intent Recognition:
- Keywords: "large" (specify_size)
- Context validation: state = awaiting_size → specify_size expected
- Output: Intent = "specify_size"

Stage 2 - Entity Extraction:
- Scan for size: "large" found
- Output: Entities = {size: "large"}

Stage 3 - Context Update:
- Current state: awaiting_size
- Received: size entity
- Transition: awaiting_size + size → awaiting_toppings
- Update context: {current_intent: "order_pizza", state: "awaiting_toppings", entities: {size: "large"}}

Stage 4 - Response Generation:
- State: awaiting_toppings
- Missing: toppings entity
- Response: "Great! What toppings would you like? We have pepperoni, mushrooms, cheese, olives, and onions."
```

**Turn 3:**
```
User: "Pepperoni and mushrooms"
Context: {current_intent: "order_pizza", state: "awaiting_toppings", entities: {size: "large"}}

Stage 1 - Intent Recognition:
- Keywords: "pepperoni" (specify_toppings), "mushrooms" (specify_toppings)
- Output: Intent = "specify_toppings"

Stage 2 - Entity Extraction:
- Scan for toppings: "pepperoni", "mushrooms" found
- Output: Entities = {toppings: ["pepperoni", "mushrooms"]}

Stage 3 - Context Update:
- Current state: awaiting_toppings
- Received: toppings entity
- Transition: awaiting_toppings + toppings → ready_to_confirm
- Update context: {current_intent: "order_pizza", state: "ready_to_confirm", entities: {size: "large", toppings: ["pepperoni", "mushrooms"]}}

Stage 4 - Response Generation:
- State: ready_to_confirm
- All info collected
- Response: "Perfect! I have a large pizza with pepperoni and mushrooms. Should I place this order? (Say 'yes' to confirm or 'cancel' to cancel)"
```

### Component Independence

While components work together, they are **designed to be independent**:

- **Intent recognition** doesn't know about entity extraction
- **Entity extraction** doesn't know about intent recognition
- **Context management** receives results from both and orchestrates the conversation

This modular design allows:
- Independent testing of each component
- Easy debugging (isolate which component has issues)
- Future enhancements without affecting other components
- Clear separation of concerns

---

## Summary

The chatbot architecture consists of three tightly integrated components:

1. **Intent Recognition** identifies user goals using priority-based keyword matching with context validation
2. **Entity Extraction** captures structured information using rule-based pattern matching operating independently
3. **Context Management** maintains conversation state using a finite state machine with defined transitions

These components work together through a clear processing pipeline, enabling the chatbot to:
- Handle natural, multi-turn conversations
- Interpret ambiguous user inputs using context
- Skip conversation steps when users provide multiple details at once
- Allow modifications to previously provided information
- Maintain conversation coherence across turns

The architecture balances **simplicity** (keyword-based, rule-based) with **sophistication** (context-awareness, state management), making it suitable for beginner implementation while demonstrating real-world chatbot design principles.

---

## Implementation Roadmap

The following sections implement each component as Python code:

**Part (b)** implements intent recognition:
- Function: `recognize_intent(user_input, context) → intent_label`
- Method: Keyword matching with priority ordering and context validation
- Returns: String intent label

**Part (c)** implements entity extraction:
- Function: `extract_entities(user_input) → entities_dict`
- Method: Rule-based pattern matching with predefined keyword lists
- Returns: Dictionary of extracted entities

**Part (d)** implements context management:
- Class: `ContextManager` with methods for initialization, update, and state transitions
- Maintains: Current intent, dialogue state, collected entities
- Determines: Next bot action based on state machine

These components will be integrated into a main chatbot loop that orchestrates the complete conversation flow.

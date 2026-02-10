# Exercise 04.3.A.01 – Part (a): Chatbot Architecture

## Overview

This section describes the basic architecture of a simple AI-based chatbot for a pizza ordering scenario. The chatbot consists of three main components: **intent recognition**, **entity extraction**, and **context management**. Together, these components enable the chatbot to understand user input, maintain a coherent conversation over multiple turns, and generate appropriate responses.

---

## 1. Intent Recognition

**Purpose:**
The intent recognition component identifies the **goal or intention** of the user’s message.

**How it works:**
In this chatbot, intent recognition is implemented using a simple keyword-based approach. The user’s input text is analyzed for specific keywords or phrases that are associated with predefined intents (for example: `order_pizza`, `specify_size`, `specify_toppings`, `cancel_order`, `greeting`).

**Input:**

* Raw user text (e.g. “I want to order a pizza”)

**Output:**

* A single intent label representing the user’s goal (e.g. `order_pizza`)

---

## 2. Entity Extraction

**Purpose:**
The entity extraction component identifies and extracts **specific pieces of information** from the user’s input that are relevant to fulfilling the intent.

**How it works:**
Entity extraction is performed using simple rule-based logic and predefined keyword lists. For the pizza chatbot, this includes detecting entities such as pizza size (small, medium, large) and toppings (e.g. pepperoni, mushrooms). The component scans the user’s message for known entity values and collects them in a structured form.

**Input:**

* Raw user text

**Output:**

* Structured entity data (e.g. `size = large`, `toppings = [pepperoni, mushrooms]`)

---

## 3. Context Management

**Purpose:**
The context management component stores and updates the **conversation state** across multiple turns, allowing the chatbot to remember previous inputs and respond appropriately.

**How it works:**
The chatbot maintains a context object that represents the current state of the conversation. This context may include the current intent, the current step in the dialogue (e.g. awaiting size or awaiting toppings), and any entities that have already been collected. Context management ensures that short or ambiguous inputs (such as “Large”) can be correctly interpreted based on what has already happened in the conversation.

**Stored information may include:**

* Current intent (e.g. `order_pizza`)
* Conversation state (e.g. `awaiting_size`, `awaiting_toppings`)
* Collected entities (size, toppings)

---

## 4. Component Interaction (End-to-End Flow)

When a user sends a message, the chatbot processes it in the following order:

1. **Intent recognition** analyzes the user input to determine the user’s goal.
2. **Entity extraction** identifies and extracts relevant information from the same input.
3. **Context management** updates the stored conversation state using the detected intent and entities.
4. Based on the updated context, the chatbot generates a response that either asks for missing information or confirms the current order.

By combining these components, the chatbot can handle multi-turn interactions, remember user choices across messages, and maintain a coherent and structured conversation.

---

## Part (b): Intent Recognition – Planning

### Goal

Design a simple intent recognition mechanism that identifies the user’s intent from a predefined list using keyword-based rules.

### Predefined Intents

The chatbot supports the following intents:

* `greeting`
* `order_pizza`
* `specify_size`
* `specify_toppings`
* `cancel_order`
* `unknown`

### Strategy

* User input is normalized (e.g. converted to lowercase, punctuation ignored).
* Each intent is associated with a set of keywords.
* The input text is checked for the presence of these keywords.
* Intents are evaluated in a **fixed priority order** to avoid conflicts.
* The first matching intent is returned.
* If no keywords match, the intent `unknown` is returned.

### Intent–Keyword Mapping (Conceptual)

| Intent           | Example Keywords             |
| ---------------- | ---------------------------- |
| greeting         | hi, hello, hey               |
| cancel_order     | cancel, stop, never mind     |
| order_pizza      | pizza, order, get            |
| specify_size     | small, medium, large         |
| specify_toppings | pepperoni, mushrooms, cheese |

### Input / Output Definition

* **Input:** Raw user text (string)
* **Output:** One intent label (string)

---

## Part (c): Entity Extraction – Planning

### Goal

Extract structured information (entities) from the user’s input that is required to complete a pizza order.

### Supported Entities

* `size` (e.g. small, medium, large)
* `toppings` (one or more values, e.g. pepperoni, mushrooms)

### Strategy

* Use predefined keyword lists for each entity type.
* Scan the normalized user input for known entity values.
* Allow extraction of multiple entities from a single message.
* Store extracted entities in a structured format.

### Handling Multiple Entities

* A single user message may contain more than one entity (e.g. size and toppings).
* For toppings, multiple matches are allowed and collected in a list.

### Input / Output Definition

* **Input:** Raw user text (string)
* **Output:** Dictionary of extracted entities (e.g. `{size: "large", toppings: ["pepperoni"]}`)

---

## Part (d): Context Management – Planning

### Goal

Maintain conversation state across multiple turns so the chatbot can handle short, incremental user inputs and multi-step ordering.

### Definition of Context

Context represents the **current state of the conversation**, not the full chat history. It allows the chatbot to remember what information has already been provided and what is still missing.

### Context Structure (Conceptual)

The context is represented as a simple data object containing:

* `current_intent` (e.g. `order_pizza`)
* `state` (e.g. `idle`, `awaiting_size`, `awaiting_toppings`, `confirming`)
* `size` (if provided)
* `toppings` (if provided)

### Context Update Rules

* **Order starts:** Initialize context, set state to `awaiting_size`.
* **Size provided:** Store size, update state to `awaiting_toppings`.
* **Toppings provided:** Store toppings, move toward confirmation.
* **Order canceled:** Clear context and return to `idle` state.

### Role in Response Generation

The current context determines:

* how user input is interpreted (e.g. what a single word like “Large” means), and
* what the chatbot should ask or say next.

---

## Summary

Parts (b), (c), and (d) are designed to work together in a clear sequence:

1. Intent recognition determines the user’s goal.
2. Entity extraction retrieves relevant information from the input.
3. Context management stores and updates the conversation state.

This planning phase ensures that the subsequent Python implementation is simple, structured, and aligned with the exercise requirements.

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

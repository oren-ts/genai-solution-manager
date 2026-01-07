# 🛒 Exercise 04.Ü.01: Prompt Engineering Iteration Log

## 🎯 Project Objective
To create a robust, unambiguous Chain-of-Thought (CoT) prompt for a volume discount calculator that explains its reasoning and handles errors correctly.

---

## 🏗️ Iteration 1: The Zero-Shot Foundation

**Original Prompt:**
> "Think step by step, calculate the unit price for a product given the following scenarios: 1 - 9 units, price is 25€ per unit, 10-19, there's a price discount of 10% per unit, 20+ there's a discount of 20% per unit. create a table showing the quantity, discount, and price per unit"

**Original Comments:**
> "Great start! Using the phrase 'Think step by step' is the classic way to trigger Zero-Shot Chain-of-Thought (CoT)... Modern best practices suggest that giving the model 'room to think' significantly improves accuracy in logic-heavy tasks."

**Key Takeaways:**
1. 🧠 **CoT Trigger:** The phrase "Think step by step" encourages the model to lay out logic before the final answer.
2. 🧮 **Logic Gaps:** Initial prompts often focus on the rules but miss the specific "Task" (calculating a total).
3. 📉 **Accuracy:** Forcing a step-by-step process prevents the model from "jumping" to an incorrect calculation.

---

## 🏗️ Iteration 2: Testing & Instruction Conflict

**Original Prompt:**
> "Think step by step, calculate the unit price for a product given the following scenarios: 1 - 9 units... Calculate these specific quantinites and use these steps to find the final total, [8], [14], [32]"

**Original Comments:**
> "Solid step forward! You’ve added specific test cases... However, there are a few 'pro-tips'... avoid conflicting instructions. You started with 'Think step by step' but ended with 'Enough thinking.'"

**Key Takeaways:**
1. 🧪 **Test Cases:** Using specific numbers ([8], [14], [32]) allows you to verify if the AI understands every logic tier.
2. 🚫 **Instruction Conflict:** Using "Enough thinking" at the end can counteract "Think step by step," leading to truncated logic.
3. 🧱 **Structural Clarity:** Long paragraphs are harder for AIs to parse than segmented instructions.

---

## 🏗️ Iteration 3: Structural Anchors

**Original Prompt:**
> "Discount Rules: 1 - 9 units... Task: Think step by step... Reasoning Format: Show results in a table"

**Original Comments:**
> "Much cleaner structure! By using clear headers like Discount Rules, Task, and Reasoning Format, you are providing the model with 'structural anchors' that help it parse your instructions more accurately."

**Key Takeaways:**
1. ⚓ **Headers:** Using clear labels helps the AI distinguish between rules and the current task.
2. 📏 **Precision:** Clearly defining "Unit Price" (original vs. discounted) removes ambiguity.
3. 📊 **Output Control:** Specifying a format (like a table) organizes the AI's final answer.

---

## 🏗️ Iteration 4: Thinking Blocks & Generalization

**Original Prompt:**
> "Discount Rules: ... Task: Step 1: calculate the unit price... step 2: find the final total... Reasoning Format: output your reasoning before providing final answer"

**Original Comments:**
> "Significantly stronger... clarifying the math and thinking blocks... This aligns with Anthropic’s recommendation to use a 'thought block' to prevent the model from committing to a wrong answer too early."

**Key Takeaways:**
1. 🧠 **Reasoning Placement:** Asking for reasoning *before* the answer forces the AI to process the math correctly first.
2. 🏷️ **Variables:** Moving away from hard-coded numbers toward `[Quantity]` markers makes the prompt reusable.
3. 🕰️ **Recency Bias:** Instructions at the very end of a prompt carry the most weight.

---

## 🏗️ Iteration 5: The "Master" Prompt (Guardrails & Examples)

**Original Prompt:**
> "###Role### You are a precise billing assistant... ###Thinking Process### ... ###Examples### Input: 14 units ... Output: ... Final Total Price: €315.00"

**Original Comments:**
> "This prompt is excellent and demonstrates a high level of mastery! ... Logical Guardrails (Step 1) prevent the model from wasting processing power on invalid data."

**Key Takeaways:**
1. 🛡️ **Guardrails:** Explicitly checking for a "positive integer" prevents errors from invalid user inputs.
2. 🛑 **Output Control:** Defining exact error messages (e.g., `{"You've entered wrong input"}`) ensures professional behavior.
3. 🌟 **Few-Shot Prompting:** Including examples (Success/Error) provides a pattern for the AI to follow, dramatically increasing reliability.

# 🛒 Prompt Engineering Iteration Log: Exercise 04.Ü.01

## 🎯 Project Goal
Create a robust, unambiguous **Chain-of-Thought (CoT)** prompt for a volume discount calculator that explains its reasoning step-by-step and handles input errors gracefully.

---

## 🏗️ Iteration 1: Zero-Shot Foundation

### 💬 Original Learner Prompt
> "Think step by step, calculate the unit price for a product given the following scenarios: 1 - 9 units, price is 25€ per unit, 10-19, there's a price discount of 10% per unit, 20+ there's a discount of 20% per unit. create a table showing the quantity, discount, and price per unit"

### 💡 Original Tutor Comment
> "That is a great start! 🛠️ Using the phrase 'Think step by step' is the classic way to trigger Zero-Shot Chain-of-Thought (CoT), which encourages the model to lay out its logic before giving a final answer."

### 🧠 Key Takeaways
1. **CoT Trigger:** Using "Think step by step" is the standard way to activate the model's reasoning capabilities.
2. **Task Definition:** Initial prompts often focus on the "Rules" but forget the specific "Task" (calculating for a specific input).
3. **Logic Gaps:** Without specific quantities to solve for, the model simply describes the rules rather than applying them.

---

## 🏗️ Iteration 2: Inputs and Conflicting Signals

### 💬 Original Learner Prompt
> "Think step by step, calculate the unit price for a product given the following scenarios: 1 - 9 units, price is 25€ per unit, 10-19, there's a price discount of 10% per unit, 20+ there's a discount of 20% per unit. create a table showing the quantity, discount, and price per unit. Calculate these specific quantinites and use these steps to find the final total, [8], [14], [32]"

### 💡 Original Tutor Comment
> "That second iteration is a solid step forward! 🎯 You’ve added specific test cases ([8], [14], [32]), which is excellent for verifying that the AI understands each discount tier... Avoid Conflicting Instructions: You started with 'Think step by step' but ended with 'Enough thinking.'"

### 🧠 Key Takeaways
1. **Test Cases:** Hard-coding specific numbers ([8], [14], [32]) allows for immediate verification of logic across all tiers.
2. **Instruction Conflict:** Avoid giving expansion signals (Think more) and compression signals (Enough thinking) in the same prompt.
3. **Variable Markers:** Using brackets `[ ]` helps the AI identify where specific data inputs are located.

---

## 🏗️ Iteration 3: Structural Anchors and Precision

### 💬 Original Learner Prompt
> "Discount Rules: 1 - 9 units, price is 25€ per unit, 10-19, there's a price discount of 10% per unit, 20+ there's a discount of 20% per unit
> Task: Think step by step, step 1: calculate the unit price for given the discount rules step 2: find the final total price for these quantities [8], [14], [32]
> Reasoning Format: Show results in a table"

### 💡 Original Tutor Comment
> "This is a much cleaner structure! 🏗️ By using clear headers like Discount Rules, Task, and Reasoning Format, you are providing the model with 'structural anchors' that help it parse your instructions more accurately."

### 🧠 Key Takeaways
1. **Markdown Headers:** Headers act as visual and logical delimiters, helping the AI focus its attention on different sections.
2. **Semantic Precision:** Defining exactly what math to perform (e.g., "calculate from the original unit price") removes ambiguity.
3. **Reasoning-First:** Modern models perform significantly better when required to output reasoning *before* the final numerical answer.

---

## 🏗️ Iteration 4: Guardrails and Output Control

### 💬 Original Learner Prompt
> "###Role###
> You are a precise billing assistant. Your goal is to calculate order totals accurateley based on volume discount rules.
> ###Discount Rules###
> 1 - 9 units: 0% discount ...
> ###Thinking Process###
> 1. Check for input accuracy: must be a positive integer. If the input is not a positive integer, stop immediately, show the user the following message {"You've entered wrong input"} and explain why the calculation cannot proceed."

### 💡 Original Tutor Comment
> "This is a sophisticated prompt! 🛠️ You have successfully integrated Role prompting, Structured Data, and Chain-of-Thought (CoT) reasoning with explicit Guardrails. By adding the specific error message... you are exercising a technique called Output Control."

### 🧠 Key Takeaways
1. **Guardrails:** Explicit validation (e.g., checking for positive integers) prevents the model from processing logically invalid data.
2. **Dynamic Scaling:** Using percentage rules instead of fixed numbers allows the prompt to stay valid even if the base price changes.
3. **Role Prompting:** Assigning a specific professional persona (Billing Assistant) sets the tone and increases focus on accuracy.

---

## 🏗️ Iteration 5: Few-Shot Mastery (Final Tool)

### 💬 Original Learner Prompt
> "###Examples###
> Input: 14 units
> Output: Step 1: Check for input accuracy. 14 is a positive integer.
> ...
> Final Total Price: €315.00"

### 💡 Original Tutor Comment
> "This prompt is excellent and demonstrates a high level of mastery! ... you are teaching the AI how to double-check its work, which reduces 'calculator errors.' ... moving the Base Price to its own line... turned this into a professional template."

### 🧠 Key Takeaways
1. **Few-Shot Prompting:** Providing examples of success and failure creates a "template" that the AI follows with near 100% reliability.
2. **Logic Decomposition:** Showing the AI *how* to verify math (e.g., 14 x 20 + 14 x 2.5) prevents common multiplication errors.
3. **Template Design:** Isolating variables like "Base Price" makes the prompt reusable for different products without editing the core logic.

---

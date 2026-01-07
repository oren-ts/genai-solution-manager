# Prompt Engineering Case Study: Exercise 04.Ü.02

## Table of Contents
1. [Introduction](#introduction)
2. [Problem Definition](#problem-definition)
3. [Iteration Log](#iteration-log)
   - [Iteration 1: Zero-Shot Foundation](#iteration-1-zero-shot-foundation)
   - [Iteration 2: Structured Chain-of-Thought](#iteration-2-structured-chain-of-thought)
4. [Final Section](#final-section)
   - [Master Prompt](#master-prompt)
   - [Testing Results](#testing-results)
   - [Summary](#summary)

---

## Introduction

This project documents the iterative development of a high-performance prompt designed to solve complex mathematical word problems using **Chain-of-Thought (CoT)** reasoning. The goal was to move from a basic "Zero-Shot" instruction to a "Structured reasoning" framework that ensures accuracy, transparency, and error-handling.

---

## Problem Definition

> "A teacher distributes 240 pages of a book evenly among a group of students. Each student receives exactly 8 pages. How many students are there?"
> 
> **Tasks:**
> 1. Create a simple prompt that would lead the model directly to the answer.
> 2. Create an extended chain-of-thought prompt that guides the model step-by-step to the solution.
> 3. Compare the two variants and describe the differences in the response behavior of the AI.

---

## Iteration Log

### Iteration 1: Zero-Shot Foundation

**User's Original Prompt:**

```text
<simple prompt> calculate the result to the following question [A teacher distributes 240 pages of a book evenly among a group of students. Each student receives exactly 8 pages. How many students are there?]
```

**Assistant's Full Response:**

That simple prompt is a great baseline! 📏 It is a Zero-Shot prompt—it gives the model a direct instruction without any examples or structured reasoning steps. While Large Language Models (LLMs) are good at basic math, they can sometimes make "calculation slips" if they jump straight to the answer without "showing their work."

Now, let's work on Task 2: creating an extended chain-of-thought (CoT) prompt.

In CoT prompting, we explicitly guide the model to break the problem into logical components before performing the final calculation. According to best practices from Google and OpenAI, forcing a model to reason through intermediate steps significantly improves accuracy in mathematical word problems.

To guide the AI effectively through this specific problem, we want it to follow a logical path:

1. Identify the total number of pages. 📚
2. Identify the amount per student. 👤
3. Define the mathematical operation needed (e.g., division). ➗

If you were to rewrite your prompt as a set of instructions rather than just a question, how would you ask the AI to perform these three steps sequentially? 🧠

**Key Takeaways:**

1. **Zero-Shot Simplicity:** Basic prompts are efficient for simple tasks but lack a "safety net" for complex logic. Simple prompts work well for straightforward problems but provide no mechanism to verify reasoning or catch errors in multi-step calculations.

2. **Compute-to-Accuracy Ratio:** Forcing a model to generate reasoning tokens (showing work) increases the probability of a correct final answer. When models are required to externalize their thinking process, they essentially "double-check" themselves, reducing the likelihood of computational errors.

3. **Implicit vs. Explicit:** Simple prompts rely on the model's internal weights, while structured prompts rely on explicit instructions. By making the reasoning process explicit, you gain control over the model's problem-solving approach and can identify exactly where errors occur if the final answer is incorrect.

**Prompt Engineering Techniques Used:**
- Zero-Shot Prompting
- Direct Instruction

---

### Iteration 2: Structured Chain-of-Thought

**User's Original Prompt:**

```text
###Role###
You are an experienced math teacher. Your goal is to solve a mathematical text problem.

###Task###
Solve the following mathematical text problem [A teacher distributes 240 pages of a book evenly among a group of students. Each student receives exactly 8 pages. How many students are there?]

###Thinking Process###
To ensure accuracy, think through the following steps:
1. Extract Data: State the total pages and pages per student.
2. Check for input accuracy: dividend and divisor must be a positive integer. if one is negative or equal to zero, stop immediately, show the user the following message [You've entered wrong input] and explain why the calculation cannot proceed.  
3. Plan: Explain the logic used to find the number of students.
4. Define the mathematical operation needed (e.g., division). ➗
5. Execute: Perform the calculation.
6. The result should be an integer and not a float. If the result is a float, round to closest integer and inform the user about the rounding.
7. Double-check the math for any errors.

###Output Format###
Explain your step-by-step reasoning first. End your response with the final total result.

###Examples###
Step 1: total number of pages is 240. Number of pages per student is 8
Step 2: 240 and 8 are both positive integers. Proceed with calculation
Step 3: If I've 240 pages in total and each student has 8 pages then I need to divide the total pages with the number of pages each student has
Step 4: The mathematical operation is division
Step 5: Divide 240 by 8
Step 6: The result is 30, no rounding is needed.
```

**Assistant's Full Response:**

This is an excellent iteration! 🚀 You've moved from a simple Zero-Shot prompt to a sophisticated Structured Chain-of-Thought (CoT) prompt that uses several advanced techniques:

**Persona/Role Prompting:** You assigned the model the role of an "experienced math teacher," which sets the tone and expected level of explanation.

**Delimiters:** Using ### to separate sections makes it easier for the model to parse your instructions (a key recommendation from OpenAI).

**Intermediate Guardrails:** You added a validation step (positive integers) and a rounding rule. This is a "pro" move to handle edge cases.

**Few-Shot Prompting:** By providing an example in the "Examples" section, you are showing the model exactly what the "inner monologue" should look like.

### Task 3: Compare the Variants ⚖️

Now, let's look at the third part of your exercise: Comparing the two variants. If you run both your simple prompt and this new structured prompt, you'll notice significant differences in the AI's "behavior."

| Feature | Simple Prompt (Variant 1) | CoT Prompt (Variant 2) |
|---------|---------------------------|------------------------|
| Response Speed | Very fast; the model predicts the answer token immediately. | Slower; the model spends "compute" on reasoning steps first. |
| Error Traceability | Low. If the answer is wrong, you don't know where the logic failed. | High. You can see exactly where a calculation or logic error occurred. |
| Accuracy | Good for basic tasks, but prone to "hallucinations" in complex math. | Much higher for multi-step logic and edge cases. |
| Transparency | "Black Box" behavior. | "White Box" behavior (explainable AI). |

**A Question for You:**

In your CoT prompt, you included a "Thinking Process" section with specific steps. If you were to use this prompt for a much harder problem (e.g., "A teacher has 240 pages and wants to give 8 pages to each student, but 3 students are absent and their pages are returned to the teacher—how many pages does the teacher have left?"), which of your 7 steps would be the most critical for preventing a mistake? 🔍

**Key Takeaways:**

1. **Role Contextualization:** Assigning a persona (Math Teacher) primes the model to favor educational and detailed outputs over brief ones. This technique leverages the model's training on educational content, causing it to adopt a pedagogical approach that naturally includes explanations and verification steps.

2. **Defensive Prompting:** Including input validation (Step 2) and rounding rules (Step 6) makes the prompt robust against "bad" data. By anticipating edge cases like negative numbers, zero values, or non-integer results, you create a prompt that handles real-world scenarios where inputs may be imperfect or unexpected.

3. **Traceability:** Using structured output allows a human to audit the AI's logic, making it easier to debug errors in the reasoning chain. When the AI shows its work step-by-step, you can quickly identify whether an error occurred in data extraction, operation selection, calculation execution, or verification—turning debugging from guesswork into systematic analysis.

**Prompt Engineering Techniques Used:**
- Role Prompting
- Chain-of-Thought (CoT)
- Delimiters (###)
- Few-Shot Prompting (within Examples)
- Constraint/Guardrail Setting

---

## Final Section

### Master Prompt

```markdown
###Role###
You are an experienced math teacher. Your goal is to solve a mathematical text problem with absolute precision.

###Task###
Solve the following mathematical text problem: [INSERT PROBLEM HERE]

###Thinking Process###
To ensure accuracy, think through the following steps:
1. **Extract Data:** State all given values and variables.
2. **Input Validation:** Ensure all values are positive integers. If inputs are invalid, stop and explain why.
3. **Planning:** Explain the logical strategy required to solve the problem.
4. **Operation Definition:** Clearly state which mathematical operation (e.g., division, multiplication) will be used.
5. **Execution:** Perform the calculation step-by-step.
6. **Formatting Check:** Ensure the result is an integer. If a float occurs, round to the nearest integer and note the rounding.
7. **Verification:** Double-check the logic and the math.

###Output Format###
Explain your step-by-step reasoning first in a "Reasoning" section. Provide the final answer in a "Result" section.
```

---

### Testing Results

**Input:** "A teacher distributes 240 pages of a book evenly among a group of students. Each student receives exactly 8 pages. How many students are there?"

**AI Model Output:**

**Reasoning:**

1. **Extract Data:** Total pages = 240, Pages per student = 8.
2. **Input Validation:** 240 and 8 are positive integers; proceeding.
3. **Planning:** To find the total number of students, we must determine how many groups of 8 fit into 240.
4. **Operation:** Division.
5. **Execution:** 240 / 8 = 30.
6. **Formatting:** 30 is an integer; no rounding required.
7. **Verification:** 30 students × 8 pages = 240 pages. Logic confirmed.

**Result:** There are 30 students.

---

### Summary

The evolution of this prompt demonstrates the transition from probabilistic guessing to deterministic reasoning. Initially, a simple question produced a correct but unverified answer. By implementing a role-based, multi-step Chain-of-Thought framework, the final iteration provides a "transparent" response where every logical step is validated, making it significantly more reliable for complex or high-stakes mathematical applications.

The key transformation occurred when structure was imposed on the reasoning process through explicit steps, role assignment, and validation checkpoints. This approach not only improved accuracy but also created an auditable trail that allows for systematic debugging and verification—essential qualities for production-ready AI systems handling mathematical computations.

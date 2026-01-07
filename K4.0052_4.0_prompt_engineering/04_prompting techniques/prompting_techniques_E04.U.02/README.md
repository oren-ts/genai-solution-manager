# Exercise 04.Ü.02: Mastering Chain-of-Thought Prompting

## Introduction
The objective of this exercise is to transition from simple "Zero-Shot" prompting to "Chain-of-Thought" (CoT) prompting. CoT is a critical technique for complex reasoning and mathematical tasks, as it encourages the model to process problems in logical, intermediate steps, thereby increasing accuracy and transparency.

## Problem Definition
> "A teacher distributes 240 pages of a book evenly among a group of students. Each student receives exactly 8 pages. How many students are there?"

## Table of Contents
1. [Iteration 1: Zero-Shot Foundation](#iteration-1-zero-shot-foundation)
2. [Iteration 2: Transition to Structured Reasoning](#iteration-2-transition-to-structured-reasoning)
3. [Master Prompt](#master-prompt)
4. [Testing Results](#testing-results)
5. [Summary of Evolution](#summary-of-evolution)

---

## Iteration 1: Zero-Shot Foundation

### User's Original Prompt
> `<simple prompt> calculate the result to the following question [A teacher distributes 240 pages of a book evenly among a group of students. Each student receives exactly 8 pages. How many students are there?]`

### Assistant's Full Response
> That simple prompt is a great baseline! 📏 It is a **Zero-Shot prompt**—it gives the model a direct instruction without any examples or structured reasoning steps. While Large Language Models (LLMs) are good at basic math, they can sometimes make "calculation slips" if they jump straight to the answer without "showing their work."
>
> Now, let's work on **Task 2**: creating an **extended chain-of-thought (CoT) prompt**.
>
> In CoT prompting, we explicitly guide the model to break the problem into logical components before performing the final calculation. According to best practices from Google and OpenAI, forcing a model to reason through intermediate steps significantly improves accuracy in mathematical word problems.
>
> 
>
> To guide the AI effectively through this specific problem, we want it to follow a logical path:
> 1. Identify the **total** number of pages. 📚
> 2. Identify the **amount per student**. 👤
> 3. Define the **mathematical operation** needed (e.g., division). ➗
>
> If you were to rewrite your prompt as a set of instructions rather than just a question, how would you ask the AI to perform these three steps sequentially? 🧠

### Key Takeaways
1. **Zero-Shot Limitations:** Simple prompts are efficient but provide no "audit trail" for the AI's logic, making them prone to calculation errors in more complex scenarios.
2. **Instruction vs. Question:** Transitioning from asking a question to providing a set of instructions gives the user more control over the model's output quality.
3. **Step-by-Step Logic:** Breaking a problem into "Identify," "Plan," and "Execute" phases is a core best practice for mathematical reasoning.

### Prompt Engineering Techniques Used
* Zero-Shot Prompting
* Instructional Scaffoldin

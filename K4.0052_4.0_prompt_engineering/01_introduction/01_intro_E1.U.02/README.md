# Exercise 01.Ü.02: Intentional Optimization & Comparative Analysis

## 📋 Exercise Overview
This exercise focuses on "Reverse Engineering" prompts. By intentionally creating an imprecise prompt and then optimizing it, we demonstrate how linguistic precision directly controls the AI's probabilistic output.

### 🎯 Objective
* Identify the pitfalls of "open" and "unstructured" prompts.
* Apply **Persona**, **Context**, and **Success Metrics** to narrow the AI's focus.
* Analyze the technical reasons why specific formulations yield superior results.

---

## 🏗️ Task 1: Prompt Comparison

### 🔴 The Imprecise Prompt
> **"Can I vibecode a mobile app?"**
* **Topic:** Software Development / AI Tools.
* **Status:** Unclear and highly ambiguous.

### 🟢 The Optimized Prompt
> **"I'm a product manager with no coding experience and my target is to build and deploy a simple habit tracking app to Google Play and App Store. I want to reach an MRR of 10,000€ within 6 months since the app is launched. Come up with a clear roadmap and the technology stack to achieve my goal."**
* **Status:** High Precision, Clear Persona, Defined Constraints.

---

## 🔍 Task 2: Analysis of Differences

### What changes were made?
1. **Introduction of a Persona:** Added "Product Manager with no coding experience." This sets the technical level for the response.
2. **Defined the Goal:** Changed a binary question ("Can I?") into a request for a "Roadmap and Technology Stack."
3. **Added Success Metrics:** Specified the target platforms (Google Play/App Store) and a financial goal (10,000€ MRR within 6 months).

### Why does the optimized prompt achieve better output?
According to **Chapter 1.1** of the course script, AI models operate on **probabilities**. 
* **The Imprecise Prompt** has a wide "probability field." The AI might guess you want a definition of a slang term, a pep talk, or a list of websites.
* **The Optimized Prompt** "narrows" the field. By using keywords like "Product Manager," "MRR," and "Deployment," you force the AI to retrieve patterns related to **business strategy** and **software architecture** rather than generic conversational fillers.

---

## 🧪 Task 3: AI Testing & Results

### 🤖 Result of Prompt 1 (Imprecise)
* **AI Response:** *"Yes, you definitely can! 'Vibecoding' is a term for using AI tools like Cursor or Replit to build apps with natural language. Do you want some tool suggestions?"*
* **Observation:** The response is a "generic answer" (Ch 1.2). It is polite but lacks any actionable depth for a professional project.

### 🤖 Result of Prompt 2 (Optimized)
* **AI Response:** Provides a **comprehensive roadmap**:
    * **Stack:** FlutterFlow (Frontend), Firebase (Backend), RevenueCat (Subscription management).
    * **Roadmap:** Month 1 (MVP/Core Loops), Month 2 (Integration), Month 3 (Deployment), Months 4-6 (Scaling & Monetization).
* **Observation:** The response is **Consultative**. It addresses the user as a peer and provides a strategy tailored to the specific financial constraint (10k MRR).

---

## 🏁 Comparison Summary

| Feature | Imprecise Prompt | Optimized Prompt |
| :--- | :--- | :--- |
| **Clarity** | Low (uses slang "vibecode") | High (defined role and app type) |
| **Precision** | Low (binary question) | High (specific roadmap request) |
| **Context** | None | Strong (target platforms & MRR goals) |
| **Value** | Educational/Definitions | Strategic/Actionable |

## 💡 Key Learning
"Vague prompts lead to vague results." To get professional-grade output from an LLM, you must provide the **constraints** that define success. As noted in **Chapter 1.4**, the biggest challenge in prompting is ambiguity—precision is the only cure.

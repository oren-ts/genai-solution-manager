# Exercise 02.Ü.01: Open vs. Closed Prompts — Iterative Logic Log

## 📋 Exercise Overview

This exercise focuses on **Chapter 2.2** (Difference between open and closed prompts) and **Chapter 2.3** (The role of context and clarity). The goal is to analyze specific prompts, categorize them based on textbook criteria, and reformulate them to change their framework from **Open** to **Closed** (or vice versa).

---

## 🏗️ The Iteration Logs

### **Task (a): "Explain the benefits of renewable energy."**

* **Original Prompt:** "Explain the benefits of renewable energy."
* **User Analysis:** *this prompt is an open one. it leaves to much room for the ai model to provide a vague, superficial answer. this prompts leaves room for interpretation. there are no specific restrictions. It misses both clarity - what is expected from the model and context - who is the audience, how long the text should be*
* **Senior Feedback:** *You are absolutely correct. Your analysis aligns perfectly with Section 2.2 and 2.3 of the course material. Because the prompt is "open," the AI's probabilistic nature might lead it to talk about anything from global politics to home solar panels without a specific goal.*
* **Final Reformulated Prompt (Closed):** *"As an environmental consultant, list the top 3 economic benefits of switching to wind energy for a small manufacturing business. Format the answer as a bulleted list and keep the total length under 100 words."*

---

### **Task (b): "Name three main causes of climate change."**

* **Original Prompt:** "Name three main causes of climate change."
* **User Analysis:** *this is a an open prompt, the word three doesn not act as a real constraint because the model still have room for interpertation e.g. is it men made reasons vs. natural climate change.*
* **Senior Feedback:** *Actually a **Closed Prompt**. The script states that closed prompts "provide a clear framework for the answer." By specifying the number "three," you are creating a narrow framework. The AI is no longer free to write a long, rambling essay; it is forced to provide exactly three items. Reformulate it into an Open Prompt.*
* **User 1st Iteration (Open):** *why climate is happening?*
* **Senior Feedback:** *The phrasing "climate is happening" is scientifically ambiguous. As the textbook notes, “unclear or ambiguous prompts often lead to unusable results.” Your prompt falls into the category of being "too broad."*
* **User 2nd Iteration (Open):** *Tell me about climate change and how it affects humans in their everyday life*
* **Senior Feedback:** *Better. But Section 2.3 says: "AI models often perform better when they are assigned a specific perspective." Currently, you haven't told the AI who it is. Section 2.1 says: "Should the model provide a formal, creative, technical or factual answer? This can be explicitly defined."*
* **User 3rd Iteration (Open):** *As a concerned activist, tell me about climate change and how it affects humans in their everyday life, be fact based as well as empathetic. use everyday terminology*
* **Final Master Version (Open):** *"Act as a concerned climate activist. Explain how climate change is currently impacting the everyday lives of ordinary people, from food prices to local weather. Be deeply empathetic to the human struggle but remain strictly fact-based. Use accessible, everyday language and conclude with a message of community resilience."*

---

### **Task (c): "What could a city of the future look like?"**

* **Original Prompt:** "What could a city of the future look like?"
* **User Analysis:** *this is an open prompt. the ai model could interpret that in many ways: future cities on the moon/mars, deep in the ocean. it is not limited by the future horizon: in 100, 200, 1000 years*
* **Senior Feedback:** *Categorization is correct. High risk of a "Broadness" pitfall (Section 2.5). Reformulate to a Closed Prompt.*
* **User 1st Iteration (Closed):** *as a futuristic expert, describe how city of New York will look like 500 hundreds years from now. Your description should cover transportation, accommodation, leisure and work styles. Comeup with engaging tone*
* **Senior Feedback:** *Section 2.2 says closed prompts aim for "precise, fact-based or structured answers." By asking for an "engaging tone," you invite creativity. You wrote "500 hundreds years" (50,000 years). A Senior Engineer ensures the input is unambiguous.*
* **User 2nd Iteration (Closed):** *as a futuristic expert, describe how city of New York will look like 500 hundred years from now. For each of the following categories list 5 specific technological predictions: 1. transportation 2. accommodation 3. leisure 3. work. Max of 300 words. each category is a sub-header with bullet points below*
* **Final Master Version (Closed):** *"Act as a professional Futurist. Provide a structured vision of New York City in the year 2525. For each of the following four categories, provide exactly 3 concise, high-impact technological predictions: 1. Transportation, 2. Accommodation, 3. Leisure, 4. Work. Format using sub-headers and bullet points. Constraint: Max 250 words total."*

---

### **Task (d): "What steps are required to train a neural network?"**

* **Original Prompt:** "What steps are required to train a neural network?"
* **User Analysis:** *closed prompt as this asks for a specific checklist. The prompt does not have a "narrow framework" because it doesnt specify the number of steps*
* **Senior Feedback:** *Actually **Open**. The script defines a closed prompt as one that provides a "narrow framework" (e.g., "Name three characteristics"). Because it leaves "a great deal of room for interpretation" regarding depth and length, it is technically Open. Reformulate to Closed.*
* **User 1st Iteration (Closed):** *as a machine learning scientist, list the 5 must have steps to train a neural network for the latest Gemini model. for each step explain the input, processing and outputs. Use technical terms with explnations for non technical product manager who wants to find their next role in AI companies. combine visual aids e.g. workflows*
* **Senior Feedback:** *Conflict: "Scientist" vs "Non-technical." Hallucination Trap: Asking for "latest Gemini" (proprietary). Feasibility: Most LLMs cannot "combine visual aids" in text output.*
* **User 2nd Iteration (Closed):** *as a machine learning scientist, list the 5 must have steps to train a neural network for a standard code generator. for each step explain the input, processing and outputs. Your audience are non technical product managers who want to find their next role in AI companies. Max 600 words and use Markdown Table for the IPO steps.*
* **Final Master Version (Closed):** *"Role: Senior AI Technical Recruiter. Task: Explain the 5 essential steps to train a standard code-generation neural network for non-technical PMs. Format: Strictly a Markdown Table with columns for Step Name, Input, Processing, and Output. Constraint: Use accessible analogies; Max 500 words; focus on industry standards."*

---

## 📊 Summary of Key Learnings

### **Task (a): Renewable Energy**

* **What went well:** Accurate identification of "Open" ambiguity and lack of target audience.
* **Improvement:** Learned that a closed prompt needs an "Economic" or "Technical" angle to stay precise.

### **Task (b): Climate Change**

* **What went well:** Successful layering of Persona (Activist) and Tone (Empathetic).
* **Improvement:** Initially misidentified as Open. Learned that numerical constraints ("Three") automatically move a prompt toward the **Closed** category.

### **Task (c): Future Cities**

* **What went well:** Recognizing the need to anchor the prompt in a specific time and place.
* **Improvement:** Fixing numerical typos ("500 hundreds") to prevent the AI from defaulting to sci-fi fantasy instead of plausible futurology.

### **Task (d): Neural Network**

* **What went well:** Using the **IPO (Input-Process-Output)** structure for high-density technical information.
* **Improvement:** Learned to avoid the "Hallucination Trap" (Gemini) and to align the **Persona** with the **Audience** to prevent contradictory tones.

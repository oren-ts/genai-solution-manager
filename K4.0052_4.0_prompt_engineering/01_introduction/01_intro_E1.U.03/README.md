# Exercise 01.Ü.03: Definition, KERNEL Framework, and Scenario Optimization

## 📋 Task 1: Definition and Meaning of Prompt Engineering

### **My Definition**
Prompt Engineering is the ability to apply instructions to a Large Language Model (LLM) to perform specific tasks. It is both an **art and a science** balanced to achieve:
* The highest success rate and consistent results over time.
* Maximum user satisfaction and reduced unwanted outputs.
* Optimized efficiency (reduced token usage and faster response times).

### **The Foundations of a Good Formulation**
To achieve the definition above, a prompt must embody the three pillars defined in the course script (Chapter 1.2):
1.  **Clarity:** Eliminating ambiguity so the model doesn't drift into unwanted interpretations.
2.  **Precision:** Focusing the request on the "essentials" rather than broad generalities.
3.  **Context:** Providing the "Who, Why, and for Whom" to guide the model's probabilistic output.

---

## 🛠️ The KERNEL Framework
To standardize the creation of high-performing prompts, I apply the **KERNEL** framework:

| Letter | Principle | Bad Example | Good Example |
| :--- | :--- | :--- | :--- |
| **K** | **Keep it simple** | 500 words of unnecessary fluff. | One clear, focused goal. |
| **E** | **Easy to verify** | "Make it engaging." | "Include 3 code examples." |
| **R** | **Reproducible** | "Use current trends." | Use specific versions and exact requirements. |
| **N** | **Narrow scope** | Combining code + docs + tests. | One prompt = one goal. Split complex tasks. |
| **E** | **Explicit constraints** | "Write Python code." | "Python code. No external libraries." |
| **L** | **Logical structure** | A wall of text. | Format: Context -> Task -> Constraints -> Output. |

---

## 🏗️ Task 2: Scenario Optimization (Python Fibonacci)

### 🔴 Weak Prompt
> "write a python script for Fibonacci"

### 🟢 Optimized Prompt (KERNEL Applied)
> **Context:** I'm a python beginner developer and my goal is to learn how Fibonacci sequence code works and where it can be applied.
> **Task:** Write a Python script to calculate Fibonacci sequence.
> **Constraints:** Use only python built-in methods. Meet Python standards PEP 8.
> **Output:** Include two code examples with comments.

---

## 📊 Analysis of Task 2: Side-by-Side Comparison

| KERNEL Component | Weak Prompt | Optimized Prompt |
| :--- | :--- | :--- |
| **Logical Structure** | None (Single sentence). | **Clear Blocks:** Separates Context, Task, and Output. |
| **Easy to Verify** | Impossible to measure "good" code. | **Metric:** Must have 2 examples and PEP 8 style. |
| **Narrow Scope** | Vague. | **Focused:** Specifically on learning and application. |
| **Explicit Constraints**| None. | **Strict:** No external libraries allowed. |
| **Precision** | Low (Generic request). | **High:** Targeted at a "Beginner" level. |

---

## 🧪 Task 3: Testing & Comparison of AI Outputs

### **Result: Weak Prompt**
```python
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
print(fib(10))

```

* **Analysis:** Provides a "one-size-fits-all" recursive solution. It is inefficient for beginners to understand and lacks any explanation or adherence to PEP 8 standards.

### **Result: Optimized Prompt**

```python
# Example 1: Iterative Approach (Beginner Friendly)
# This method uses a loop, which is memory efficient.
def calculate_fibonacci_list(count):
    sequence = [0, 1]
    for i in range(2, count):
        next_value = sequence[-1] + sequence[-2]
        sequence.append(next_value)
    return sequence

# Example 2: Simple Recursive Approach
# Used to demonstrate how the sequence builds on itself.
def get_fibonacci_number(index):
    if index <= 1:
        return index
    return get_fibonacci_number(index - 1) + get_fibonacci_number(index - 2)

# Application: Used in financial modeling and growth algorithms.

```

* **Analysis:** The AI acted as a **teacher**. It provided two distinct methods, commented the code for a **beginner**, and included the **application context** requested.

---

## 🏁 Final Conclusion

The optimized version is superior because it **narrows the probability field** of the LLM. By using the **KERNEL** framework, we transition the AI from a "Text Generator" to a "Solution Architect," ensuring the output is not just correct, but specifically useful for the user's intent.

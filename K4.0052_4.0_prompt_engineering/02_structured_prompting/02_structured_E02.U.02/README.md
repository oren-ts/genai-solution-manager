# Exercise 02.Ü.02 - Prompt Engineering Analysis and Reformulation

## Exercise Overview

**Objective:** Analyze the following prompts for clarity, structure, context and expectation. Revise them so that they produce more precise and better quality answers from an AI model. Briefly justify your changes.

**Given Prompts:**
1. "Tell me something about history."
2. "Explain the theory of relativity."
3. "Write a text about artificial intelligence."
4. "What are renewable energies?"
5. "Why is technology bad?"

**Expected Solution:**
Each revision should address the core problems of the original prompt and contain a convincing justification for the changes.

---

## Methodology

The process for each prompt follows these steps:
1. Discuss the analysis of the current prompt
2. Reformulate the prompt
3. Discuss the reformulated prompt
4. Iterate if necessary

Each prompt is evaluated based on four pillars:
- **Clarity:** How unambiguous is the instruction?
- **Structure:** Is there a logical arrangement or format?
- **Context:** What information is provided to narrow the subject?
- **Expectation:** Is the tone, length, or perspective defined?

---

## Prompt 1: "Tell me something about history."

### Initial Analysis

**Clarity:** The instruction is highly ambiguous. What time range of history? Since the beginning of mankind? The big bang? What cultures?

**Structure:** The instruction is too short to have a logical structure.

**Context:** None. This instruction does not provide any narrow framework.

**Expectation:** None given, so the model can interpret that in any way possible.

**Verdict:** This prompt is a "Zero-Context" request and a "Broadness Pitfall" (Section 2.5). The AI is forced to make a random statistical guess about which historical period, region, or event to discuss.

### Reformulated Prompt (Iteration 1)

**Context:** You're an expert historian specializing in middle-age era in Europe.

**Clarity:** Your task is to describe everyday life of people living in a village in western Europe:
1. Housing
2. Community
3. Culture and customs
4. Health
5. Rituals

**Structure:** For each topic, come up with max 100 words.

**Expectation:** Use facts in a storytelling tone.

### Review of Reformulation

| Pillar | Analysis | Reference (Chapter 2) |
|--------|----------|----------------------|
| **Context** | ✅ Role assigned: "Expert historian specializes in middle-age era." | Sec 2.3: "Role definition helps the model deliver more relevant and accurate results." |
| **Clarity** | ✅ Subject defined: "Everyday life in a Western Europe village." | Sec 2.1: "Specific formulations do not mislead the model into making interpretation errors." |
| **Structure** | ✅ Categorized: 5 specific sub-topics with length limits. | Sec 2.1: "Format guidelines improve the structure... avoiding separate, disjointed questions." |
| **Expectation** | ✅ Tone set: "Facts in a storytelling tone." | Sec 2.1: "Expectations should be clearly defined (formal, creative, technical, or factual)." |

### Justification

The original prompt was a "Broadness Pitfall" (Section 2.5), forcing the AI to make a random statistical guess. By assigning the Role of a "Middle-age historian," we provide a contextual categorization (Section 2.3) that guides the model's semantic orientation. Specifying the Location and Timeframe serves as an explicit restriction (Section 2.4), ensuring the AI doesn't drift into irrelevant eras. The role allows the model to understand the persona and the location is a narrowing framework to increase the results precision. This combination transforms a vague query into a targeted, strategic tool (Chapter 2 introduction).

---

## Prompt 2: "Explain the theory of relativity."

### Initial Analysis

**Clarity:** This lacks the scope of theory to explain. It can be very complex, using mathematical and theoretical physics, or it can be summarized as the end result of the equation. This is an example of an imprecise formulation that leads to unspecific answers.

**Structure:** No chain-like formulation or format guidelines. The AI will likely output a single, dense paragraph that lacks utility.

**Context:** Lack of a "narrow framework." Crucially, there is no Role Definition (e.g., Theoretical physicist vs. Teacher in high school), which the textbook says is essential for relevant results.

**Expectation:** Since neither tone nor perspective is defined, the AI doesn't know if this should be a "factual" account or a "persuasive argument."

**Additional Issues:**
- **The "Dual Theory" Problem:** "Relativity" consists of two distinct theories: Special Relativity and General Relativity. Without a narrow framework, the model might focus on the wrong one.
- **Target Audience:** Explaining relativity to a 5-year-old versus a PhD student requires completely different approaches.
- **The "Math" Constraint:** Should there be equations? Should it be purely conceptual?

### Reformulated Prompt (Iteration 1)

Assume the role of science teacher in high school, 12th grade. Explain the theory of relativity, special and general by starting with the core concept, then use an example, then a conclusion. Use mathematical formulas to support the concept.

### Review of Iteration 1

| Pillar | Analysis | Reference (Chapter 2) |
|--------|----------|----------------------|
| **Context** | ✅ Role & Audience: "Science teacher in high school, 12th grade." | Sec 2.3: Adjusts the "semantic orientation" to the correct level of difficulty. |
| **Clarity** | ✅ Scope defined: "Special and general." | Sec 2.1: Removes ambiguity between the two theories. |
| **Structure** | ✅ Logical Chain: "Core concept -> Example -> Conclusion." | Sec 2.1: This "chain-like formulation" helps the model follow a logical path. |
| **Expectation** | ✅ Technical Requirement: "Use mathematical formulas." | Sec 2.1: Clearly defines the expected technical depth. |

### Refinement: Critical Thinking Check

**Potential Risks Identified:**
1. **Formatting Risk:** Without specific formatting instructions, the AI might blend the theories into a long narrative.
2. **"Math Depth" Pitfall:** "12th grade" can vary significantly worldwide. The AI might provide Einstein's field equations (too advanced) or just E=mc² (too simple).

### Reformulated Prompt (Final Version)

Assume the role of science teacher in high school, 12th grade. Explain the theory of relativity, special and general by starting with the core concept, then use an example, then a conclusion. Start first with special and then the general theory. Limit each section to 400 words. Use qualitative algebra-based formulas to support the concept.

### Review of Final Version

| Pillar | Analysis | Reference (Chapter 2) |
|--------|----------|----------------------|
| **Context** | ✅ Role & Level: "Science teacher, 12th grade" ensures the AI doesn't drift into PhD-level calculus or elementary-school metaphors. | Sec 2.3: Providing a "semantic orientation." |
| **Clarity** | ✅ Order of Operations: Specifying "Start first with special and then general" prevents a jumbled explanation. | Sec 2.1: Eliminates interpretation errors. |
| **Structure** | ✅ IPO-like Flow: The "Concept -> Example -> Conclusion" loop for each theory creates a predictable, logical rhythm. | Sec 2.1: Chain-like formulation. |
| **Expectation** | ✅ Technical Guardrails: "Qualitative algebra-based formulas" is a brilliant constraint. It tells the AI: "Give me math, but keep it solvable with a standard calculator." | Sec 2.4: Explicit restrictions. |

### Justification

The original prompt was a "Broadness Pitfall," forcing the AI to make a random statistical guess. Specifying the order and specific mathematical level serves as an explicit restriction, ensuring the AI doesn't drift into irrelevant eras or inappropriate mathematical complexity. This combination transforms a vague query into a targeted, strategic tool.

---

## Prompt 3: "Write a text about artificial intelligence."

### Initial Analysis

**Clarity:** The script specifically uses "Write a text about artificial intelligence" as an example of an imprecise formulation that leads to unspecific answers.

**Structure:** Without a chain-like formulation or format guidelines (like a list or specific headers), the AI will likely output a single, dense paragraph that lacks utility.

**Context:** Lack of a "narrow framework." Crucially, there is no Role Definition (e.g., data science vs. AI software dev), which the textbook says is essential for relevant results.

**Expectation:** Since neither tone nor perspective is defined, the AI doesn't know which topic about artificial intelligence to cover.

**Verdict:** This is the ultimate "Broadness Pitfall." Because "Artificial Intelligence" is an umbrella term covering everything from philosophy and ethics to neural network architecture and business automation, the model will likely default to a high-level, generic summary that provides no unique value.

### Reformulated Prompt

You are a tech journalist, writing an essay of 1500 words for a tech blog. The tech blog has subscribers that are tech savvy e.g. data scientists, AI software developers, and AI product managers. Your article covers the topic of vibecoding for mobile apps: its origin, challenges, success stories, risks and advantages. The article is informative without any bias.

### Review of Reformulation

| Pillar | Analysis | Reference (Chapter 2) |
|--------|----------|----------------------|
| **Context** | ✅ Role & Audience: "Tech journalist" for a "tech-savvy" audience (Data Scientists, PMs). | Sec 2.3: "Role definition helps the model deliver more relevant and accurate results." |
| **Clarity** | ✅ Niche Subject: "Vibecoding for mobile apps." | Sec 2.1: Replacing a general category (AI) with a specific phenomenon (Vibecoding). |
| **Structure** | ✅ Thematic Framework: Origin, challenges, success stories, risks, and advantages. | Sec 2.1: This ensures the AI covers the full breadth of the topic without missing key angles. |
| **Expectation** | ✅ Tone & Scale: "1500 words" and "informative without bias." | Sec 2.1: Clearly defines the expected volume and neutral perspective. |

### Critical Thinking Check

**Potential Risks:**
1. **"Hallucination" and Knowledge Cutoff Risk:** "Vibecoding" is a very recent term (popularized in late 2024/2025). If the model's training data is older, it might guess or hallucinate.
2. **Formatting:** For a 1500-word essay, without "Use Markdown headers," you might get a massive wall of text.

### Justification

Specifying the audience is to provide the model with contextual categorization and to restrict the model from using blocks of code for examples. By defining the audience as "tech-savvy" (Data Scientists/PMs), you instruct the model to skip the basics and speak at a professional level—it establishes the Semantic Orientation (Section 2.3).

---

## Prompt 4: "What are renewable energies?"

### Initial Analysis

**Clarity:** The script specifically uses "What are renewable energies?" as an example of an imprecise formulation that leads to unspecific answers.

**Structure:** Without a chain-like formulation or format guidelines (like a list or specific headers), the AI will likely output a single, dense paragraph that lacks utility.

**Context:** Lack of a "narrow framework." Crucially, there is no Role Definition (e.g., financial investor vs. civil engineer), which the textbook says is essential for relevant results.

**Expectation:** Since neither tone nor perspective is defined, the AI doesn't know which topic about renewable energies to cover.

**Verdict:** This prompt suffers from the "Wikipedia Trap." While factually clear, it's likely to yield a result that is "technically correct but practically useless" (Section 2.5).

### Reformulated Prompt (Iteration 1)

You're an entrepreneur who comes to pitch a potential investor about a SaaS product. Your task is to create a pitch deck of 800 words, starting with problem description -> suggested solution -> ROI. The pitch deck is professional, supported with data and strong argumentations to push back on the investor's lack of will to invest. It should be very persuasive.

### Critical Thinking Check

**Missing Link:** The original topic was "Renewable Energies." In this iteration, the format and role are perfectly defined, but there's no explicit mention that the SaaS product must be related to Renewable Energy.

**Additional Issues:**
1. **Subject Bridge:** The "SaaS product" needs to be specifically in the renewable energy sector.
2. **The "Data" Pitfall:** Since the SaaS is fictional, the AI will create (hallucinate) data. Instructing it to "use realistic, industry-standard benchmarks" makes this professional.

### Reformulated Prompt (Final Version)

You're an entrepreneur who comes to pitch a potential investor about a SaaS product that uses AI to monitor windmills functionality. Your task is to create a pitch deck of 800 words, starting with problem description -> suggested solution -> ROI. Use realistic, industry-standard benchmarks for the renewable energy sector and strong argumentations to push back on the investor's lack of will to invest. It should be very persuasive.

### Review of Final Version

| Pillar | Analysis | Reference (Chapter 2) |
|--------|----------|----------------------|
| **Context** | ✅ Niche Identification: AI SaaS for windmills. | Sec 2.3: Provides the "narrow framework" missing in the original. |
| **Clarity** | ✅ Technical Scope: Monitoring windmill functionality. | Sec 2.1: Eliminates the "Broadness Pitfall" of general renewable energy. |
| **Structure** | ✅ Logical Narrative: Problem -> Solution -> ROI. | Sec 2.1: Guides the AI through a strategic business sequence. |
| **Expectation** | ✅ Data Integrity: "Realistic, industry-standard benchmarks." | Sec 2.5: Prevents wild hallucinations by anchoring the AI in reality. |

### Justification

Moving from "What is X?" to a "Persuasive Pitch" is a superior test of AI capability because:
1. **Complexity Handling:** It forces the model to synthesize raw facts into a strategic narrative, rather than just retrieving definitions (Section 2.1).
2. **Performance & Efficiency:** It uses explicit restrictions (length, structure, goal) to ensure the output is a "targeted, strategic tool" (Section 2.6) rather than a generic text block.
3. **Real-world Utility:** It provides contextual categorization (Section 2.3) that mimics actual professional tasks, making the AI a thought partner rather than an encyclopedia.

---

## Prompt 5: "Why is technology bad?"

### Initial Analysis

**Clarity:** The script specifically uses this as an example of an imprecise formulation that leads to unspecific answers. The word "bad" is imprecise and represents a presupposition.

**Structure:** Without a chain-like formulation or format guidelines (like a list or specific headers), the AI will likely output a single, dense paragraph that lacks utility.

**Context:** Lack of a "narrow framework." Crucially, there is no Role Definition (e.g., Historian vs. Storyteller), which the textbook says is essential for relevant results.

**Expectation:** Since neither tone nor perspective is defined, the AI doesn't know if this should be a "factual" account or a "persuasive argument."

**Verdict:** This is a classic **Bias Pitfall** (Section 2.5). By using the word "bad," you are no longer asking for an objective analysis; you are issuing a "Leading Prompt." This forces the model to ignore the benefits of technology and focus only on the negatives, which violates the principle of Neutrality.

### Additional Issues

- **Clarity & The Bias Pitfall:** "Bad" is imprecise and creates presupposition. You have "baked in" the answer you want.
- **Context (The "Echo Chamber" Effect):** Without a Role, you're asking the AI to pull from the most common complaints on the internet, leading to a shallow, stereotypical response.
- **Expectation:** Is the goal to find solutions to these problems, or just to list them?

### Reformulated Prompt

Use realistic, industry-standard benchmarks for autonomous cars safety and come up with a comparative analysis between human driving and autonomous cars to predict what is the breakeven point where autonomous cars could be deployed and replace driving humans.

### Review of Reformulation

| Pillar | Analysis | Reference (Chapter 2) |
|--------|----------|----------------------|
| **Context** | ✅ Specific Domain: You narrowed "Technology" down to "Autonomous Vehicles." | Sec 2.3: Providing a "narrow framework" for the subject matter. |
| **Clarity** | ✅ Objective Metric: You replaced "bad" with "safety benchmarks" and "breakeven point." | Sec 2.5: Successfully avoided the Bias Pitfall by asking for a comparison rather than a one-sided critique. |
| **Structure** | ✅ Comparative Analysis: You explicitly requested a "comparative analysis between human driving and autonomous cars." | Sec 2.1: Uses a logical arrangement to reach a specific prediction. |
| **Expectation** | ✅ High-Utility Goal: The output isn't just a list; it's a predictive model for deployment. | Sec 2.6: Transforms the AI into a "strategic tool" for decision-making. |

### Justification

I provide a contextual categorization (Section 2.3) that guides the model's semantic orientation.

When you use a word like "bad," you trigger a Bias Pitfall (Section 2.5). The model looks for the highest-probability associations with "bad technology," which usually results in a generic list of social complaints.

By shifting to "Safety Benchmarks" and a "Breakeven Point":
1. **Neutrality is Forced:** The AI must now look at the pros (reduced human error) and the cons (technical failures) to find the point where they cross. This is the definition of balanced analysis.
2. **Instructional Utility:** A "bad" list is just an opinion; a "breakeven point analysis" is a decision-support tool.
3. **Semantic Orientation:** You moved the prompt from the "Ethics/Opinion" category to the "Engineering/Safety" category, which drastically increases the factual density of the response.

---

## Summary Table: All Reformulations

| Original Prompt | Problem Type | Reformulated Focus | Key Improvement |
|----------------|--------------|-------------------|-----------------|
| "Tell me something about history." | Broadness Pitfall | Middle-age European village life with specific topics | Role definition + narrow framework + structured output |
| "Explain the theory of relativity." | Ambiguity + Technical Depth | High school level, algebraic explanations of Special then General | Audience definition + mathematical level constraint + ordered structure |
| "Write a text about artificial intelligence." | Superficiality | Tech journalist article on vibecoding for mobile apps | Niche topic + professional audience + thematic framework |
| "What are renewable energies?" | Wikipedia Trap | SaaS pitch for AI windmill monitoring | Business context + ROI focus + industry benchmarks |
| "Why is technology bad?" | Bias Pitfall | Comparative safety analysis of autonomous vs. human driving | Neutral framing + objective metrics + predictive analysis |

---

## Key Principles Applied

### The Four Pillars of Prompt Engineering

1. **Clarity:** Remove ambiguity by specifying exact topics, scopes, and terms
2. **Structure:** Provide logical flow, format guidelines, and organizational frameworks
3. **Context:** Define roles, audiences, domains, and situational parameters
4. **Expectation:** Set tone, length, perspective, and output requirements

### Common Pitfalls Avoided (Section 2.5)

- **Broadness Pitfall:** Vague, unfocused prompts that force random AI responses
- **Bias Pitfall:** Leading questions that presuppose answers
- **Complexity Pitfall:** Insufficient constraints on technical depth
- **Length Pitfall:** No word count or format constraints
- **Hallucination Risk:** Lack of grounding in realistic benchmarks

### Success Criteria

Each reformulated prompt:
- Provides contextual categorization (Section 2.3)
- Uses explicit restrictions (Section 2.4)
- Establishes semantic orientation (Section 2.3)
- Transforms the AI into a strategic tool (Section 2.6)
- Ensures instructional utility through structured outputs

---

## Conclusion

This exercise demonstrates the transformation from "General Chatting" to "Targeted Prompting." By focusing on the four pillars (Clarity, Structure, Context, and Expectation), we ensure the AI doesn't have to rely on random probability to generate answers. Instead, prompts become "programming instructions" that produce professional, usable outputs.

The key insight: **Moving from vague questions to strategic frameworks dramatically increases the quality, relevance, and utility of AI-generated responses.**

---

## References

All section references (e.g., "Section 2.1," "Section 2.3") refer to Chapter 2 of the course materials on Prompt Engineering fundamentals.

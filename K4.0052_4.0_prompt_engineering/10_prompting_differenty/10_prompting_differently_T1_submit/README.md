# Exam 2: Advanced Prompting Techniques - Scenario Analysis & Integration

**Course:** K4.0052 - Prompt Engineering (velpTECH)  
**Topic:** Combined prompting methodologies for real-world applications

---

## Part 1: Scenario Analysis & Technique Selection

### Scenario A: Automated Customer Support

**Selected Technique:**  
Dialog-based prompting combined with iterative clarification and structured response templates.

**Justification:**  
Automated customer support requires handling unpredictable, multi-step inquiries while maintaining conversation context. Dialog-based prompting enables context retention across turns, allowing the AI to remember prior inputs, ask targeted follow-up questions, and adapt responses dynamically. Structured templates (triage → diagnose → resolve → escalate) ensure consistency and reliability across interactions.

**Implementation Approach:**

1. **System Role:** Define AI as customer support agent with clear behavioral guidelines (polite, concise, solution-oriented)
2. **Conversation Loop:** 
   - Classify intent and category
   - Ask clarifying questions (2-4 maximum per turn)
   - Propose solution with confirmation
   - Escalate with summary if blocked
3. **Memory Protocol:** Summarize after each turn what is known, what was tried, and next steps

**Why static prompting would fail:** Customer inquiries contain unpredictable variables and missing information that static prompts cannot clarify through targeted questions, leading to incomplete responses and user frustration.

---

### Scenario B: Scientific Blog Article

**Selected Technique:**  
Static prompting with explicit constraints.

**Justification:**  
This task produces a single, complete, well-defined output where all requirements—topic, audience, tone, structure, and quality constraints—are known in advance. Static prompting allows efficient specification of all parameters upfront without requiring interaction.

**Static Prompt:**
```
You are an economic research writer. Write a detailed, scientifically 
grounded blog article about: "The Impact of Artificial Intelligence on 
the Labor Market."

AUDIENCE: Educated non-specialists (business + policy readers)
TONE: Clear, neutral, evidence-oriented; avoid hype and fearmongering

REQUIREMENTS:

1. Length: 1,200–1,600 words

2. Structure with headings:
   - Introduction (problem framing + why this matters now)
   - Key mechanisms (automation, augmentation, task reallocation)
   - Sector examples (at least 4: manufacturing, healthcare, finance, 
     software, public sector)
   - Effects on wages and inequality (balanced analysis)
   - Skills and education implications (reskilling, lifelong learning)
   - Policy and organizational responses (government + corporate actions)
   - Conclusion (summary + open questions)

3. Include:
   - ONE comparison table: "High AI exposure vs. Low AI exposure" job tasks
   - 5 bullet-point key takeaways at the end

4. Scientific quality standards:
   - Use careful language ("evidence suggests…", "studies indicate…")
   - Do NOT invent citations
   - When mentioning research, keep general (e.g., "OECD research", 
     "academic studies on task-based automation")

5. Output format: Markdown

DELIVERABLE: Complete, publication-ready blog article meeting all criteria above.
```

**Why dialog-based prompting would fail:** All requirements are definable upfront, so dialog would add unnecessary latency without improving quality.

---

### Scenario C: Data Analysis & Trend Calculation

**Selected Technique:**  
Analytical prompting with explicit step-by-step instructions and validation checks.

**Justification:**  
Trend analysis requires structured reasoning, calculations, and verification. Analytical prompting ensures the AI follows a defined sequence: data cleaning, aggregation, metric calculation, validation, and interpretation. Explicit instructions reduce errors and increase transparency.

**How the Prompt Should Be Designed:**

1. **Input Definition:** Specify data columns (date, revenue, units, region, product), time granularity, and units
2. **Processing Steps:**
   - Data cleaning (handle missing values, duplicates, outliers)
   - Aggregation (monthly and yearly totals)
   - Trend metrics (YoY growth, 5-year CAGR, moving averages)
   - Pattern detection (seasonality, outliers with dates)
3. **Validation Checks:** 
   - Reconcile totals with raw data
   - Flag extreme values for review
   - Document all assumptions explicitly
4. **Required Outputs:**
   - Table: Yearly totals with YoY percentages
   - Table: Product-level CAGR analysis
   - Bullet insights (max 10 findings)
   - Questions for further investigation (max 5)
5. **Clarification Protocol:** If required data is missing, ask specific questions before proceeding

**Why creative or dialog-based prompts would fail:** Analytical tasks require procedural rigor and reproducible methodology that dialog approaches cannot guarantee consistently.

---

## Part 2: Combined Prompting - Market Analysis

**Techniques Combined:**  
Dialog-based prompting (Phase 1) + Analytical prompting (Phase 2)

**Why This Combination Is Useful:**  
Dialog-based prompting reduces ambiguity by gathering missing context through targeted questions, preventing unclear scope that leads to irrelevant analysis. Analytical prompting then provides structured synthesis with consistent frameworks (market sizing, competitive analysis, pricing, risks), preventing rambling conclusions. This two-phase approach enables stakeholder validation after scoping before committing resources to full analysis.

**Combined Prompt:**
```
You are a market research assistant. Execute this analysis in TWO PHASES:

═══════════════════════════════════════════════════════════════════════
PHASE 1: DIALOG-BASED SCOPING
═══════════════════════════════════════════════════════════════════════

Ask me up to 8 targeted questions to define the analysis scope:

1. Product description + core value proposition
2. Target user segments (B2B/B2C, demographics, roles)
3. Key use cases and differentiation vs. alternatives
4. Geographic focus + regulatory constraints
5. Price range / business model (SaaS, transaction, license, etc.)
6. Known competitors (if any)
7. Success metrics (adoption, retention, revenue targets)
8. Timeline and resources for go-to-market

After asking questions, WAIT for my answers before proceeding to Phase 2.

═══════════════════════════════════════════════════════════════════════
PHASE 2: ANALYTICAL MARKET ANALYSIS
═══════════════════════════════════════════════════════════════════════

Using my Phase 1 answers, produce a structured report with:

1. MARKET DEFINITION & SIZING
   - TAM/SAM/SOM estimates (labeled as reasoned estimates)
   - Segmentation criteria
   - Growth trends and drivers
   - Document all assumptions

2. COMPETITIVE LANDSCAPE
   - Top 4-6 competitors
   - Positioning map (2×2 matrix)
   - Strengths/weaknesses table
   - White space opportunities

3. CUSTOMER ANALYSIS
   - Jobs-to-be-done
   - Buying criteria (must-haves vs. nice-to-haves)
   - Key pain points

4. PRICING STRATEGY
   - 3-4 pricing tiers with rationale
   - Competitor pricing comparison
   - Value-based justification

5. GO-TO-MARKET PLAN
   - Recommended channels
   - Target segment priority
   - 90-day validation plan

6. RISK ASSESSMENT
   - Market, competitive, and execution risks
   - Mitigation strategies

OUTPUT REQUIREMENTS:
- Clear headings and bullets
- ONE comparison table (competitors or pricing)
- "Assumptions & Unknowns" section
- Do NOT fabricate data; be explicit about uncertainty
```

---

## Part 3: Creative Storytelling - Iterative Fantasy Development

**Iterative Structure:**

The iterative approach separates foundation → structure → generation → refinement, enabling quality control at natural breakpoints and course correction before significant effort is invested.

### Iteration 1: Setup & Outline
```
You are a fantasy author. First, ask me 5 questions:
1. Protagonist (role, motivations, flaws)
2. Setting (world type, magic system rules)
3. Tone (dark/cozy/epic/philosophical)
4. Central conflict (internal vs. external)
5. Target length and audience

Then, create a story outline (200-300 words) with:
- Protagonist's goal and motivation
- Antagonist or central obstacle
- 3 key scenes that advance the plot
- One twist near the climax
- Emotional resolution
```

**Purpose:** Gather requirements and establish structural skeleton before content investment.

---

### Iteration 2: Full Draft
```
Write the complete fantasy story (900-1,200 words) based on the outline.

REQUIREMENTS:
- Vivid sensory world-building (show, don't tell)
- Consistent magic system rules (no deus ex machina)
- One clear emotional turning point
- Meaningful consequence at the end (not a cliffhanger)
- Maintain established tone
```

**Purpose:** Generate complete draft from validated structure with clear quality constraints.

---

### Iteration 3: Refinement
```
Revise the draft with these priorities:

1. Strengthen character voice and motivations
2. Tighten pacing (remove filler, maintain rising tension)
3. Improve imagery and originality of magic elements
4. Polish dialogue for authenticity

Return revised story + brief changelog (5 bullets of key improvements).
```

**Purpose:** Optimize quality systematically without restructuring, with transparent documentation of changes.

---

**How Story Is Progressively Refined:**

Each iteration builds on validated previous work: Iteration 1 prevents wasted effort on wrong direction by confirming requirements and structure; Iteration 2 generates complete content from approved architecture; Iteration 3 optimizes quality without fundamental changes.

**How Creative Elements Are Incorporated:**

Creative elements are introduced progressively: Iteration 1 establishes creative boundaries (magic rules, world type, tone); Iteration 2 focuses on vivid sensory details and original world-building; Iteration 3 enhances imagery, replaces clichés with fresh details, and strengthens unique magic system elements.

---

**End of Exam**

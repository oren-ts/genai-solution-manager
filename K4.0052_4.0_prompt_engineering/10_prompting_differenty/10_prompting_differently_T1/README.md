# Exam 2: Advanced Prompting Techniques - Scenario Analysis & Integration

**Course:** K4.0052 - Prompt Engineering (velpTECH)  
**Topic:** Combined prompting methodologies for real-world applications  
**Focus:** Dialog-based, static, analytical, and iterative prompting techniques

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Part 1: Scenario Analysis](#part-1-scenario-analysis)
  - [Scenario A: Automated Customer Support](#scenario-a-automated-customer-support)
  - [Scenario B: Scientific Blog Article](#scenario-b-scientific-blog-article)
  - [Scenario C: Data Analysis & Trend Calculation](#scenario-c-data-analysis--trend-calculation)
- [Part 2: Combined Prompting - Market Analysis](#part-2-combined-prompting---market-analysis)
- [Part 3: Creative Storytelling - Iterative Fantasy Development](#part-3-creative-storytelling---iterative-fantasy-development)
- [Key Learnings & Insights](#key-learnings--insights)
- [Production Applications](#production-applications)
- [Appendix: Copy-Paste Prompts](#appendix-copy-paste-prompts)

---

## Executive Summary

This exam demonstrates practical application of multiple prompting techniques across diverse scenarios:

| Scenario | Technique | Key Benefit |
|----------|-----------|-------------|
| **Customer Support** | Dialog-based + iterative clarification | Adaptive conversation with context retention |
| **Content Creation** | Static prompting | Efficient, reusable blog generation |
| **Data Analysis** | Analytical prompting with validation | Reliable, auditable trend analysis |
| **Market Research** | Combined dialog + analytical | Comprehensive scoping + structured synthesis |
| **Creative Writing** | Iterative refinement | Quality control at natural breakpoints |

**Core Insight:** Real-world applications require intelligent combination of techniques matched to task characteristics: predictability, complexity, output type, and required interaction.

---

## Part 1: Scenario Analysis

### Scenario A: Automated Customer Support

**Challenge:** Handle complex, multi-turn customer inquiries while maintaining conversation context.

#### Selected Technique

**Dialog-based prompting** combined with **iterative clarification** and **structured response templates**

#### Justification

Automated customer support requires handling unpredictable, multi-step inquiries while maintaining an ongoing conversation. Dialog-based prompting is best suited for this scenario because it enables **context retention across turns**, allowing the AI to remember prior user inputs, ask targeted follow-up questions, and adapt responses dynamically. Iterative clarification helps resolve ambiguity in complex cases, while structured templates (triage → diagnose → resolve → escalate) ensure consistency and reliability.

#### Course Concepts Applied

- **Dialog-based prompting (Chapter 4):** Maintaining conversational context and memory
- **Iterative prompting (Chapter 6):** Progressive refinement through user interaction  
- **System message design (Chapter 5):** Role definition and behavioral constraints

#### Why Alternatives Are Less Effective

A static prompt would fail because customer inquiries are **rarely fully specified upfront and contain unpredictable variables** (product issues, account states, user technical knowledge). Static approaches cannot adapt to new information revealed during conversation or clarify missing details through targeted questions, leading to incomplete or incorrect responses **that frustrate users and increase escalation rates**.

#### Implementation Framework
```
SYSTEM ROLE:
"You are a customer support agent for [Company]. Be polite, concise, and solution-oriented."

CONVERSATION LOOP:
1. Intent classification + category identification (billing/technical/account)
2. Clarifying questions (max 2-4 per turn to avoid overwhelming user)
3. Propose solution with clear steps + confirmation request
4. If blocked: request specific data OR escalate to human with summary ticket

MEMORY PROTOCOL (after each turn):
Summarize:
- What we know
- What we've tried
- Next step recommended
```

---

### Scenario B: Scientific Blog Article

**Challenge:** Generate comprehensive, scientifically rigorous blog article as single deliverable.

#### Selected Technique

**Static prompting** with explicit constraints

#### Justification

This task involves producing a single, complete, well-defined output. All requirements—topic, audience, tone, structure, and quality constraints—are known in advance. A static prompt allows these parameters to be specified upfront, ensuring efficiency, consistency, and reusability without requiring back-and-forth interaction.

#### Course Concepts Applied

- **Static prompting (Chapter 3):** Clarity, specificity, explicit expectations
- **Template-based prompting (Chapter 8):** Reusable structure for content generation
- **Evaluation criteria (Chapter 11):** Quality controls and assessment standards

#### Why Alternatives Are Less Effective

Dialog-based prompting would add **unnecessary latency and complexity** without improving quality, since all requirements are definable upfront. Each clarification round would delay delivery without resolving ambiguity (the topic, audience, and structure are already clear). **For content creation with known parameters, static prompts maximize efficiency while ensuring consistency across multiple uses.**

#### Production-Ready Static Prompt
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

---

### Scenario C: Data Analysis & Trend Calculation

**Challenge:** Perform rigorous quantitative analysis with transparent, auditable methodology.

#### Selected Technique

**Analytical prompting** with explicit step-by-step instructions and validation checks

#### Justification

Trend analysis is a procedural task requiring structured reasoning, calculations, and verification. Analytical prompting ensures the AI follows a defined sequence: data cleaning, aggregation, metric calculation, validation, and interpretation. Explicit instructions reduce errors and increase transparency in how results are derived.

#### Course Concepts Applied

- **Analytical prompting (Chapter 7):** Structured reasoning for quantitative tasks
- **Chain-of-Thought reasoning (Chapter 4):** Explicit intermediate steps  
- **Error prevention strategies (Chapter 11):** Validation checks to reduce hallucination risk

#### Why Alternatives Are Less Effective

Creative or purely dialog-based prompts **lack procedural rigor** and may omit critical steps such as validation, outlier detection, or assumption documentation. **Analytical tasks require reproducible methodology**, which dialog approaches cannot guarantee across multiple executions. **Without explicit step sequencing, analytical outputs become unreliable and non-auditable.**

#### Analytical Prompt Structure
```
Act as a data analyst. I will provide sales data with columns: 
date, revenue, units, region, product.

ANALYTICAL SEQUENCE:

1. DATA CLEANING
   - Handle missing values and duplicates
   - State all assumptions explicitly
   - Document any data transformations

2. AGGREGATION
   - Calculate monthly totals
   - Calculate yearly totals by region and product
   - Verify totals reconcile with raw data

3. TREND METRICS
   - Compute YoY (Year-over-Year) growth rates
   - Calculate 5-year CAGR (Compound Annual Growth Rate)
   - Generate 3-month moving averages

4. PATTERN DETECTION
   - Identify seasonal patterns
   - Flag outliers (top 5 spikes/drops with specific dates)
   - Note any structural breaks or trend changes

5. VALIDATION CHECKS
   - Reconcile all calculated totals
   - Flag extreme values requiring review
   - Document all calculation assumptions and limitations

REQUIRED OUTPUTS:

Table A: Yearly totals with YoY percentage changes
Table B: Product-level CAGR analysis
Bullet insights: Maximum 10 key findings
Next questions: Maximum 5 areas for further investigation

INSTRUCTION: If any required data column is missing, ask for clarification 
before proceeding with analysis.
```

---

## Part 2: Combined Prompting - Market Analysis

**Challenge:** Conduct comprehensive market analysis balancing thorough scoping with structured synthesis.

### Solution Architecture

**Two-phase approach:** Dialog-based scoping → Analytical reporting

### Techniques Combined

1. **Dialog-based prompting (Phase 1):** Requirement gathering and scope clarification
2. **Analytical prompting (Phase 2):** Structured market analysis and synthesis

### Why This Combination Works

**Dialog-based prompting** (Phase 1) reduces ambiguity by gathering missing context through targeted questions. This prevents the most common failure mode in market analysis: **unclear scope leading to irrelevant or incomplete analysis**.

**Analytical prompting** (Phase 2) prevents the other critical failure: **unstructured, rambling conclusions**. By enforcing a consistent framework (market sizing, competitive landscape, pricing analysis, risk assessment), the output becomes actionable and comparable across different products or timeframes.

**Business Value:** This two-phase structure enables **validation before investment**—stakeholders can review Phase 1 scoping questions and answers, then course-correct before committing resources to the full analytical report. This mirrors real-world consulting workflows where scope confirmation precedes deep analysis.

### Course Concepts Integrated

- **Dialog-based prompting (Chapter 4):** Interactive requirement gathering
- **Analytical prompting (Chapter 7):** Structured synthesis and analysis
- **Metaprompt methodology (Chapter 8):** Reusable templates adaptable to different contexts

### Production-Ready Combined Prompt
```
You are a market research assistant. Execute this analysis in TWO PHASES:

═══════════════════════════════════════════════════════════════════════
PHASE 1: DIALOG-BASED SCOPING
═══════════════════════════════════════════════════════════════════════

Ask me up to 8 targeted questions to define the market analysis scope:

1. Product description + core value proposition
2. Target user segments (B2B/B2C, demographics, roles)
3. Key use cases and differentiation vs. existing alternatives
4. Geographic focus + language requirements + regulatory constraints
5. Price range / business model (SaaS, transaction-based, license, etc.)
6. Known competitors (if any)
7. Success metrics (adoption rate, retention, revenue targets, etc.)
8. Timeline and available resources for go-to-market

INSTRUCTION: After asking questions, WAIT for my answers. 
Do not proceed to Phase 2 until I have provided responses.

═══════════════════════════════════════════════════════════════════════
PHASE 2: ANALYTICAL MARKET ANALYSIS
═══════════════════════════════════════════════════════════════════════

Using my Phase 1 answers, produce a structured report with these sections:

1. MARKET DEFINITION & SIZING
   - TAM/SAM/SOM estimates (clearly labeled as reasoned estimates)
   - Segmentation criteria and rationale
   - Market growth trends and drivers
   - All sizing assumptions explicitly documented

2. COMPETITIVE LANDSCAPE
   - Top 4-6 competitors identified
   - Positioning map (2×2 matrix on relevant dimensions)
   - Strengths/weaknesses comparison table
   - White space opportunities analysis

3. CUSTOMER ANALYSIS
   - Jobs-to-be-done framework
   - Buying criteria (must-haves vs. nice-to-haves)
   - Decision-making process and stakeholders
   - Key pain points and unmet needs

4. PRICING STRATEGY
   - 3-4 plausible pricing tiers with detailed rationale
   - Comparison to competitor pricing
   - Value-based pricing justification
   - Price sensitivity considerations

5. GO-TO-MARKET PLAN
   - Recommended channels (direct sales, partnerships, marketplace, etc.)
   - Target segment priority (which segment to attack first and why)
   - 90-day validation plan with specific, measurable milestones

6. RISK ASSESSMENT
   - Market risks (demand uncertainty, market timing)
   - Competitive risks (response from incumbents)
   - Execution risks (capability gaps, resource constraints)
   - Mitigation strategies for top 3 risks

OUTPUT REQUIREMENTS:
- Use clear headings and bullet points for readability
- Include ONE comparison table (competitors OR pricing tiers)
- Add explicit "Assumptions & Unknowns" section
- Be transparent about uncertainty—do NOT fabricate data
- If additional data is needed, specify exactly what to provide

═══════════════════════════════════════════════════════════════════════
```

---

## Part 3: Creative Storytelling - Iterative Fantasy Development

**Challenge:** Create high-quality fantasy short story through structured, progressive refinement.

### Selected Technique

**Iterative prompting** with progressive specificity

### Why Iteration Works for Creative Content

Creative writing benefits from **separation of concerns**: foundation → structure → generation → optimization. This approach prevents the "single massive prompt" problem where one failing component ruins the entire output. It also enables **human-in-the-loop quality control** at natural breakpoints, allowing course correction before significant creative effort is invested.

### Course Concepts Applied

- **Iterative refinement (Chapter 6):** Breaking complex tasks into manageable stages with validation points
- **Progressive specificity (Chapter 3):** Starting broad (requirements) and narrowing to execution (final draft)
- **Creative content generation principles:** Balancing structural constraints with creative freedom

### Iteration Structure Overview

| Iteration | Purpose | Outputs | Validation Point |
|-----------|---------|---------|------------------|
| **0: Setup** | Gather requirements | Story premise + 2 alternative hooks | Confirm direction before outline |
| **1: Outline** | Define structure | Plot arc with 3 key scenes + twist | Approve structure before drafting |
| **2: Draft** | Generate content | Complete 900-1200 word story | Review full narrative |
| **3: Refinement** | Optimize quality | Polished story + changelog | Final approval |

### Detailed Iteration Prompts

#### Iteration 0: Requirements Gathering
```
You are a fantasy author. Ask me 5 questions to define the story parameters:

1. Protagonist (role, motivations, character flaws)
2. Setting (world type, magic system rules and limitations)
3. Tone (dark/cozy/epic/philosophical)
4. Central conflict (internal vs. external challenge)
5. Length target and intended audience

After I answer, summarize the story premise in 3 concise sentences and 
propose 2 alternative narrative hooks for me to choose from.
```

**Purpose:** Prevent wasted effort by confirming creative direction before structural work begins.

---

#### Iteration 1: Story Architecture
```
Based on the confirmed premise, create a short story outline (beginning/middle/end):

REQUIRED ELEMENTS:
- Protagonist's primary goal and underlying motivation
- Antagonist or central obstacle to overcome
- 3 key scenes that advance the plot
- One twist or revelation near the climax
- Emotional and thematic resolution

CONSTRAINT: Keep outline to 200-300 words total.

FORMAT: Use clear section headers for Beginning/Middle/End.
```

**Purpose:** Establish structural skeleton before investing in full content generation.

---

#### Iteration 2: Full Draft Generation
```
Write the complete fantasy short story (900-1,200 words) based on the 
approved outline.

REQUIREMENTS:

1. WORLD-BUILDING
   - Use vivid sensory details (show, don't tell)
   - Make the setting feel lived-in and authentic

2. MAGIC SYSTEM
   - Follow established rules consistently
   - Avoid deus ex machina solutions
   - Magic should have costs or limitations

3. CHARACTER ARC
   - Include one clear emotional turning point
   - Protagonist must face genuine stakes
   - Internal conflict should complement external plot

4. ENDING
   - Provide meaningful consequence or change
   - Avoid unearned cliffhangers
   - Maintain tonal consistency with opening

5. STYLE
   - Maintain the tone established in Iteration 0
   - Use active voice and strong verbs
   - Balance dialogue with narration
```

**Purpose:** Generate complete draft from validated structure, with clear quality constraints.

---

#### Iteration 3: Refinement Pass
```
Revise the draft story with these improvement priorities (in order):

1. CHARACTER VOICE & MOTIVATION
   - Strengthen protagonist's distinct voice
   - Clarify motivations through action, not exposition
   - Ensure choices feel authentic to character

2. PACING & TENSION
   - Remove filler sentences and redundancy
   - Maintain rising tension throughout
   - Ensure each scene advances plot or character

3. IMAGERY & ORIGINALITY
   - Enhance sensory descriptions
   - Replace clichéd magic elements with fresh details
   - Strengthen world-building through specific details

4. DIALOGUE POLISH
   - Ensure dialogue sounds natural and distinct per character
   - Remove unnecessary dialogue tags
   - Use subtext effectively

DELIVERABLES:
- Revised story (final version)
- Brief changelog (5 bullets explaining key improvements made)
```

**Purpose:** Optimize quality systematically without restructuring, with transparent documentation of changes.

---

### Why This Progressive Structure Works

Each iteration has a **single, clear purpose** and **builds systematically** on validated previous work:

- **Iteration 0** prevents wasted creative effort on the wrong direction
- **Iteration 1** provides structural skeleton before content investment  
- **Iteration 2** generates complete draft from approved architecture
- **Iteration 3** optimizes quality without requiring fundamental restructuring

This progression mirrors professional creative workflows and reflects the course's emphasis on **iterative refinement as a core prompt engineering discipline** that enables quality control while maintaining creative flexibility.

---

## Key Learnings & Insights

### 1. Technique Selection Framework

Match prompting technique to task characteristics:

| Task Characteristic | Optimal Technique | Primary Reason |
|---------------------|-------------------|----------------|
| Unpredictable inputs | Dialog-based | Requires real-time adaptation and clarification |
| Fully specified requirements | Static | Maximizes efficiency, no interaction overhead |
| Procedural/quantitative | Analytical | Ensures reproducible, auditable methodology |
| Complex creative output | Iterative | Enables quality control at natural breakpoints |
| Ambiguous scope + structured output | Combined (Dialog + Analytical) | Addresses both scoping and execution challenges |

### 2. Real-World Combination Patterns

Production systems rarely use pure techniques in isolation:

- **Customer Support:** Dialog + structured templates + escalation rules
- **Data Analysis:** Analytical + optional dialog for missing data clarification  
- **Market Research:** Dialog scoping + analytical synthesis + validation loop
- **Content Creation:** Static base template + iterative refinement for quality

### 3. Most Valuable Course Principles Applied

**From practice to production:**

- **Context retention (Chapter 4):** Essential for dialog-based systems to maintain coherence
- **Explicit step sequencing (Chapter 7):** Critical for analytical reliability and auditability
- **Progressive specificity (Chapter 3):** Prevents overwhelming complexity in single prompts
- **Iterative refinement (Chapter 6):** Enables course correction without starting over
- **Template design (Chapter 8):** Creates reusable, consistent frameworks across use cases

### 4. Common Failure Modes & Mitigations

| Failure Mode | Cause | Mitigation Strategy |
|--------------|-------|---------------------|
| Incomplete outputs | Ambiguous requirements | Dialog-based scoping before generation |
| Inconsistent quality | No validation checkpoints | Iterative approach with review stages |
| Hallucinated data | Lack of constraints | Analytical prompting with explicit rules |
| Generic content | Insufficient context | Static prompts with detailed specifications |
| Inefficient workflows | Wrong technique selection | Match technique to task characteristics |

---

## Production Applications

These exam solutions translate directly to deployable systems:

### 1. Customer Support Framework

**Deployment Context:** SaaS companies, e-commerce, technical support teams  
**Implementation Timeline:** 2-3 weeks with company-specific training data  
**Key Customizations:**
- Company-specific escalation rules and thresholds
- Product knowledge base integration
- Brand voice and tone guidelines
- Multi-language support requirements

**Expected Outcomes:**
- Reduced first-response time
- Lower escalation rates for routine inquiries
- Consistent service quality across shifts
- Scalable support without proportional headcount growth

---

### 2. Blog Article Generator

**Deployment Context:** Content marketing teams, research organizations, thought leadership programs  
**Implementation Timeline:** Immediate (template ready to use)  
**Key Customizations:**
- Adjust tone and formality per brand guidelines
- Modify structure for different content types (how-to, analysis, opinion)
- Add industry-specific terminology and frameworks
- Configure length and complexity for target audience

**Expected Outcomes:**
- Faster first-draft generation
- Consistent quality baseline across writers
- Reduced research time through structured requirements
- Reusable template for content series

---

### 3. Sales Analysis Tool

**Deployment Context:** Business intelligence teams, financial analysts, executive reporting  
**Implementation Timeline:** 1 week with data pipeline integration  
**Key Customizations:**
- Industry-specific KPIs and metrics
- Custom aggregation rules (fiscal vs. calendar year)
- Segment definitions (geography, product line, customer tier)
- Visualization preferences and dashboard integration

**Expected Outcomes:**
- Consistent analytical methodology
- Auditable calculation trails
- Reduced manual analysis time
- Faster insight generation for decision-making

---

### 4. Market Research Methodology

**Deployment Context:** Strategy consultants, product managers, venture capitalists  
**Implementation Timeline:** Immediate (prompt ready to deploy)  
**Key Customizations:**
- Industry-specific frameworks (SaaS vs. hardware vs. consumer goods)
- Regional market considerations
- Competitive intelligence sources
- Custom risk assessment criteria

**Expected Outcomes:**
- Structured approach to ambiguous research questions
- Consistent analysis format for comparison
- Explicit assumption documentation
- Faster initial market assessments

---

### 5. Creative Writing Assistant

**Deployment Context:** Authors, content creators, game developers, marketing teams  
**Implementation Timeline:** Immediate  
**Key Customizations:**
- Genre-specific iteration focuses (sci-fi, romance, thriller)
- Brand voice consistency requirements
- Length and complexity parameters
- Cultural and sensitivity guidelines

**Expected Outcomes:**
- Structured creative process
- Quality control at natural stages
- Reduced revision cycles
- Consistent creative output quality

---

## Comparative Analysis: When Each Technique Excels

### Static Prompting Outperforms When:

✅ Requirements are fully known upfront  
✅ Output is a single, complete artifact  
✅ Consistency across multiple executions is required  
✅ Latency must be minimized  
✅ Template reusability provides value  

**Ideal Use Cases:** Reports, blog articles, standard documents, email templates

---

### Dialog-Based Prompting Outperforms When:

✅ Requirements emerge through interaction  
✅ User inputs are unpredictable or context-dependent  
✅ Context accumulates meaningfully across conversation turns  
✅ Clarification significantly reduces error rates  
✅ Personalization improves outcomes  

**Ideal Use Cases:** Customer support, tutoring, complex problem-solving, discovery interviews

---

### Analytical Prompting Is Essential When:

✅ Quantitative rigor is required  
✅ Reproducibility is critical for compliance  
✅ Audit trail is needed for verification  
✅ Step-by-step logic reduces hallucination risk  
✅ Validation checks prevent costly errors  

**Ideal Use Cases:** Data analysis, financial modeling, scientific computation, regulatory reporting

---

### Iterative Prompting Delivers Value When:

✅ Output quality improves significantly with refinement  
✅ Early validation prevents wasted effort  
✅ Human-in-the-loop control is desired  
✅ Complexity requires staged approach  
✅ Creative exploration benefits from progressive development  

**Ideal Use Cases:** Writing, design, research, strategy development, complex creative projects

---

## Conclusion: Prompt Engineering as Strategic Discipline

This exam demonstrates that **effective prompt engineering is fundamentally about technique selection and intelligent combination**, not mastery of a single approach in isolation.

### The Practitioner's Framework

1. **Analyze task characteristics** (predictability, complexity, output type, interaction needs)
2. **Select appropriate technique(s)** based on requirements and constraints
3. **Design implementation** that balances control with flexibility
4. **Apply course principles systematically** (clarity, structure, validation, iteration)
5. **Anticipate failure modes** and build in appropriate safeguards

### From Theory to Production

The progression demonstrated here—**theory → application → integration → deployment**—reflects the course's emphasis on practical, production-ready prompt engineering that:

- Solves real business problems
- Maintains quality and reliability
- Provides auditability and transparency
- Scales across use cases
- Adapts to changing requirements

### Strategic Value

Prompt engineering is not just a technical skill but a **thinking discipline** that:

- Forces clarity about requirements and success criteria
- Exposes ambiguities early in the process
- Creates reusable intellectual infrastructure
- Enables systematic quality improvement
- Bridges human intent and AI capability

---

## Appendix: Copy-Paste Ready Prompts

All prompts developed in this exam are production-ready and deployable with minimal customization:

### Available Artifacts

1. **Customer Support Dialog Framework** - Structured conversation loop with escalation
2. **Scientific Blog Article Static Prompt** - Comprehensive content generation template
3. **Sales Trend Analysis Analytical Prompt** - Step-by-step data analysis methodology
4. **Combined Market Research Prompt** - Two-phase dialog + analytical approach
5. **Creative Storytelling Iteration Sequence** - Four-stage refinement framework

Each prompt includes:
- Clear role definition
- Explicit requirements and constraints
- Output specifications
- Quality control mechanisms
- Validation checkpoints

---

**Course:** K4.0052 - Prompt Engineering (velpTECH)  
**Portfolio Status:** Production-ready, deployable artifacts  
**License:** Educational use with attribution

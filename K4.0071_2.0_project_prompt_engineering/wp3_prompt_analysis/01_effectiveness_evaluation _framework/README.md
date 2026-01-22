# WP3 Deliverable 1: Effectiveness Evaluation Framework

## Executive Summary

This framework establishes systematic evaluation criteria for measuring prompt effectiveness across InsightBridge's 4 business domains. The methodology enables data-driven decisions about which prompts to optimize, maintain, or deprecate, supporting strategic portfolio management at scale.

**Key Components:**
1. **Four-Metric Effectiveness Model:** Accuracy, Relevance, Interaction Quality, Task Completion
2. **Top 2 Strategy Families Per Domain:** Methodology for identifying highest-impact prompt strategies
3. **Statistical Rigor:** Significance thresholds to prevent random variation from driving decisions
4. **Evaluation Rubric:** Scoring matrix for consistent assessment

---

## Table of Contents

1. [Effectiveness Definition & Philosophy](#effectiveness-definition--philosophy)
2. [Four-Metric Effectiveness Model](#four-metric-effectiveness-model)
3. [Top 2 Strategy Families Methodology](#top-2-strategy-families-methodology)
4. [Statistical Significance Thresholds](#statistical-significance-thresholds)
5. [Evaluation Rubric & Scoring Matrix](#evaluation-rubric--scoring-matrix)
6. [Application to WP2 Prompts](#application-to-wp2-prompts)

---

## Effectiveness Definition & Philosophy

### What is "Effectiveness"?

**Definition:** Effectiveness measures how well a prompt performs its intended function, independent of business impact or adoption scale.

**Analogy:** A precision tool can be highly effective (accurate, reliable) even if rarely used. Effectiveness is about **quality of outcomes**, not quantity of use.

**Critical Distinction:**
- **Effectiveness ≠ Value** (covered in WP3 Deliverable 2)
- A prompt can be highly effective but low value (accurate but rarely needed)
- A prompt can be high value but low effectiveness (heavily used despite imperfections)

**Example:**
- `DEC-DA-REV-DRIVERS-QUAL`: High effectiveness (prevents bad decisions when data is incomplete)
- Usage: Only 47 times/month (low compared to RET-CS-BILL's 1,247)
- **Verdict:** Highly effective, moderate value (strategic importance outweighs frequency)

---

### Philosophy: Effectiveness as Quality Control

**Effectiveness serves two strategic purposes:**

1. **Quality Gate:** Prevents ineffective prompts from being promoted despite popularity
   - Example: A prompt that's frequently used but gives wrong answers creates support burden
   - Effectiveness metrics catch this before it becomes a crisis

2. **Optimization Target:** Identifies where improvement efforts yield highest quality gains
   - Example: A 90% accurate prompt has clear room for improvement
   - A 99.5% accurate prompt is near-optimal (diminishing returns on further optimization)

**Key Principle:** Measure effectiveness before measuring value. A popular but ineffective prompt is a liability, not an asset.

---

## Four-Metric Effectiveness Model

### Overview

Effectiveness is measured across four complementary dimensions, each capturing different aspects of prompt quality:

| **Metric** | **Measures** | **Target** | **Prompt Types** |
|------------|-------------|-----------|------------------|
| **Accuracy** | Correctness of outputs | ≥95% | RET, DIA, DEC |
| **Relevance** | Appropriateness to context | ≥90% | All types |
| **Interaction Quality** | Clarity, helpfulness (per-use satisfaction) | ≥4.0/5.0 | All types |
| **Task Completion** | Functional success rate | ≥85% | All types |

**Why four metrics?**
- **No single metric captures all quality dimensions**
- Accuracy alone misses relevance (correct but unhelpful answer)
- Satisfaction alone misses accuracy (pleasant but wrong answer)
- Task completion captures end-to-end success (did the user achieve their goal?)

---

### Metric 1: Accuracy

**Definition:** Proportion of outputs that are factually correct and technically sound.

**Measurement Approach:**

**For RET (Retrieval) prompts:**
- Compare output to source of truth (e.g., Stripe billing system)
- Sample: 50 random retrievals per month
- Accuracy = (Correct retrievals / Total sampled) × 100%
- **Target: ≥99% for RET** (data retrieval must be nearly perfect)

**For DIA (Diagnostic) prompts:**
- Expert validation: Senior support engineer reviews diagnosis
- Sample: 30 diagnostic sessions per month
- Accuracy = (Correct root cause identified / Total sampled) × 100%
- **Target: ≥90% for DIA** (diagnostics allow for reasonable error given complexity)

**For DEC (Decision) prompts:**
- Compare recommendations to analyst consensus
- Sample: 20 decision scenarios per month
- Accuracy = (Agreement with analysts / Total sampled) × 100%
- **Target: ≥85% for DEC** (decision support allows for judgment differences)

**For GEN (Generation) prompts:**
- Compliance check: Legal/marketing review for factual claims
- Sample: 25 generated outputs per month
- Accuracy = (No factual errors / Total sampled) × 100%
- **Target: ≥95% for GEN** (content must be factually sound)

**For EXP (Explanation) prompts:**
- Technical review: Domain expert confirms explanation correctness
- Sample: 20 explanations per month
- Accuracy = (Technically correct / Total sampled) × 100%
- **Target: ≥95% for EXP** (explanations must not mislead)

**Statistical Note:** Accuracy requires ground truth. For subjective prompts (creative content), relevance/satisfaction may be more appropriate.

---

### Metric 2: Relevance

**Definition:** Proportion of outputs that appropriately address the user's actual need (not just technically correct).

**Why Relevance Matters:**
- A prompt can be 100% accurate but 0% relevant
- Example: User asks "Why did revenue drop?" → Prompt returns accurate revenue numbers but doesn't explain "why"
- Accuracy ✓ (numbers correct), Relevance ✗ (didn't answer the question)

**Measurement Approach:**

**Human Judgment (Primary Method):**
- Sample: 40 prompt outputs per month
- Evaluators: Domain stakeholders (support agents, marketers, analysts)
- Question: "Did this output address the user's actual need?"
- Scale: Yes (1.0) / Partially (0.5) / No (0.0)
- Relevance Score = Average across sample

**Implicit Signals (Secondary Method):**
- Follow-up queries: Does user immediately ask clarifying question? (signals low relevance)
- Reformulations: Does user rephrase their request? (signals output wasn't relevant)
- Abandonment: Does user exit without taking action? (signals output didn't help)

**Target: ≥90% relevance across all prompt types**

**Example - High Accuracy, Low Relevance:**
```
User Query: "Why is our retail vertical growing faster than logistics?"

Prompt Output (DEC-DA-REV-DRIVERS):
"Retail revenue: €4.2M (+22% YoY)
Logistics revenue: €3.1M (+0.8% YoY)"

Accuracy: ✅ 100% (numbers correct)
Relevance: ❌ 40% (stated facts but didn't explain WHY)

Better Output:
"Retail growth (+22%) driven by:
1. New customer acquisition (+18% in retail segment)
2. Product line expansion (3 new SKUs launched Q3)
Logistics flat (+0.8%) due to:
1. Churn offsetting new sales
2. Price competition limiting expansion"

Accuracy: ✅ 100%
Relevance: ✅ 95% (explains WHY, not just WHAT)
```

---

### Metric 3: Interaction Quality (Per-Use Satisfaction)

**Definition:** User-reported satisfaction with individual prompt interactions, measuring clarity, helpfulness, and perceived value.

**Critical Distinction from Value Satisfaction:**
- **Effectiveness satisfaction (this metric):** "Was THIS interaction helpful?" (per-use)
- **Value satisfaction (WP3 Deliverable 2):** "Do I keep using this prompt?" (retention)

**Why This Distinction Matters:**
- A prompt can have low per-use satisfaction but high retention (necessary evil, e.g., compliance)
- A prompt can have high per-use satisfaction but low retention (nice but not needed)

**Measurement Approach:**

**Direct Feedback (Primary):**
- Post-interaction survey: "How helpful was this response?"
- Scale: 1 (Not helpful) to 5 (Very helpful)
- Response rate target: ≥30% (to avoid self-selection bias)
- Timing: Immediately after interaction (within 30 seconds)

**Implicit Signals (Secondary):**
- Thumbs up/down: Quick binary feedback
- Dwell time: Did user read full output or abandon?
- Copy-paste: Did user copy output to use elsewhere? (strong signal of value)

**Target: ≥4.0/5.0 average satisfaction**

**Interpretation Guide:**
- **4.5-5.0:** Excellent (users love this prompt)
- **4.0-4.4:** Good (meets expectations, minor improvements possible)
- **3.5-3.9:** Adequate (functional but needs UX improvement)
- **<3.5:** Poor (urgent intervention required)

**Example - Satisfaction Diagnostic:**
```
Prompt: GEN-CC-PROD-DESC-STD
Satisfaction: 3.8/5.0 (adequate but concerning)

Qualitative feedback analysis:
- "Too generic, doesn't highlight unique features" (35% of comments)
- "Language feels corporate, not our brand voice" (28%)
- "Good starting point but requires heavy editing" (22%)

Action: Enhance few-shot examples with more brand-specific language
Expected improvement: 3.8 → 4.3
```

---

### Metric 4: Task Completion Rate

**Definition:** Proportion of interactions where the user successfully completes their intended task without requiring follow-up support.

**Why Task Completion Matters:**
- **Ultimate effectiveness test:** Did the prompt actually solve the user's problem?
- Combines accuracy, relevance, and usability into single outcome measure
- Directly correlates with business value (completed tasks = work done)

**Measurement Approach:**

**Session Analysis (Primary Method):**
- Track user session from query → resolution
- Success indicators:
  - User marks task as complete
  - No follow-up support ticket created within 24 hours
  - No escalation to human agent
  - User doesn't retry with different prompt

**Failure indicators:**
- User abandons mid-task
- Follow-up support ticket created ("This didn't work, need help")
- Escalation request ("Connect me to a person")
- Multiple reformulations of same query (prompt not understanding)

**Calculation:**
```
Task Completion Rate = (Successful sessions / Total sessions) × 100%

Where:
- Successful session = User achieves goal without escalation/follow-up
- Failed session = Abandonment, escalation, or support ticket
```

**Target: ≥85% completion rate** (allowing for legitimately complex cases requiring human intervention)

**Example - Low Completion Despite High Accuracy:**
```
Prompt: DIA-CS-TECH-ERROR-TRIAGE
Accuracy: 92% (diagnoses correct)
Satisfaction: 4.2/5.0 (users like the interaction)
Task Completion: 68% ❌ (below target)

Root Cause Analysis:
- 18% of users abandon after diagnosis but before applying fix
- 14% escalate to senior support despite correct diagnosis

Insight: Prompt diagnoses correctly but doesn't provide actionable fix steps

Improvement: Add "Recommended Actions" section with step-by-step fix
Expected completion rate improvement: 68% → 82%
```

---

## Top 2 Strategy Families Methodology

### Strategic Approach: Family-Based Evaluation

**Challenge:** With only 2 base prompts per domain (8 total), ranking "top 2 per domain" means all prompts win (non-decision).

**Solution:** Evaluate **strategy families** (base + variants) and recommend deployment strategies.

**What is a Strategy Family?**
- **Base prompt:** Core functionality (e.g., RET-CS-BILL-INVOICE-HISTORY)
- **Variants:** Contextual optimizations (e.g., RET-CS-BILL-INVOICE-HISTORY-SHORT)
- **Family evaluation:** Which version(s) to deploy, when, and for whom?

---

### Methodology: Three-Step Process

**Step 1: Rank Base Prompts Within Each Domain**

Use **Effectiveness Composite Score:**
```
Effectiveness Score = (Accuracy × 0.35) + (Relevance × 0.25) + (Satisfaction × 0.20) + (Completion × 0.20)

Weights justified:
- Accuracy (35%): Foundational requirement (wrong answers disqualify prompt)
- Relevance (25%): Must address actual user need
- Satisfaction (20%): User experience matters
- Completion (20%): Ultimate success measure
```

**Normalize each metric to 0-100 scale before weighting.**

**Step 2: Evaluate Variants Against Base**

For each variant, calculate:
```
Variant Performance Delta = Variant_Effectiveness - Base_Effectiveness

Additionally measure:
- Use case differentiation (when is variant better?)
- Performance trade-offs (speed vs. comprehensiveness)
- Deployment complexity (separate endpoints vs. parameter)
```

**Step 3: Recommend Deployment Strategy**

Based on effectiveness analysis, recommend:

**Strategy A: Deploy Base Only**
- Variant offers no meaningful improvement
- Complexity cost outweighs benefits
- Example: If variant is only 2% better, not worth maintaining two versions

**Strategy B: Deploy Variant Only (Deprecate Base)**
- Variant is superior across all use cases
- No scenarios where base is preferred
- Example: Variant is 15% more effective with no trade-offs

**Strategy C: Deploy Both (Conditional Routing)**
- Variant excels in specific contexts
- Base better for other contexts
- Example: SHORT variant for mobile, base for desktop

**Strategy D: A/B Test Before Decision**
- Effectiveness difference is marginal (within 5%)
- User preference unclear
- Example: Statistical tie requires live traffic validation

---

### Application to InsightBridge's 8 Prompts

**Customer Support (CS) Domain:**

**Family 1: Invoice Retrieval**
- Base: `RET-CS-BILL-INVOICE-HISTORY` (Effectiveness: 96.2/100)
- Variant: `RET-CS-BILL-INVOICE-HISTORY-SHORT` (Effectiveness: 92.5/100)
- **Analysis:**
  - Base: Higher accuracy (99.5% vs 98%), more complete
  - Variant: Faster (400ms vs 850ms), better mobile UX
- **Recommended Strategy:** Deploy BOTH with conditional routing
  - Mobile/chat UI → SHORT variant
  - Desktop/detailed analysis → Base
  - Reasoning: Different use cases favor different optimizations

**Family 2: Error Triage**
- Base: `DIA-CS-TECH-ERROR-TRIAGE` (Effectiveness: 87.3/100)
- Variant: `DIA-CS-TECH-ERROR-TRIAGE-URGENT` (Effectiveness: 83.1/100)
- **Analysis:**
  - Base: Higher accuracy (92% vs 88%), more thorough
  - Variant: Faster triage (2-4min vs 8-12min), prioritization logic
- **Recommended Strategy:** Deploy BOTH with severity routing
  - P0/P1 incidents → URGENT variant (speed critical)
  - P2/P3 tickets → Base (thoroughness acceptable)
  - Reasoning: Urgency vs. accuracy trade-off depends on severity

**Top 2 Strategy Families in CS:**
1. ✅ **Invoice Retrieval** (Effectiveness: 96.2) - Highest effectiveness, mission-critical
2. ✅ **Error Triage** (Effectiveness: 87.3) - Complex but high-impact

---

**Content Creation (CC) Domain:**

**Family 1: Product Descriptions**
- Base: `GEN-CC-PROD-DESC-STD` (Effectiveness: 89.1/100)
- Variant: `GEN-CC-PROD-DESC-RETAIL` (Effectiveness: 91.8/100)
- **Analysis:**
  - Variant: +2.7 points due to industry-specific language
  - Trade-off: Variant only works for retail (60% of customers)
- **Recommended Strategy:** Deploy BOTH with industry routing
  - Retail customers → RETAIL variant
  - Logistics/ProServ → Base
  - Reasoning: Industry specialization improves effectiveness but limits applicability

**Family 2: Campaign Emails**
- Base: `GEN-CC-CAMP-EMAIL-LAUNCH` (Effectiveness: 88.5/100)
- Variant: `GEN-CC-CAMP-EMAIL-PROMO` (Effectiveness: 86.2/100)
- **Analysis:**
  - Base: Higher compliance score (100% vs 98%)
  - Variant: Higher urgency effectiveness but compliance risk
- **Recommended Strategy:** Deploy BOTH with campaign type routing
  - Product launches → Base (evergreen messaging)
  - Time-limited promotions → PROMO (urgency appropriate)
  - Reasoning: Different campaign objectives require different approaches

**Top 2 Strategy Families in CC:**
1. ✅ **Product Descriptions** (Effectiveness: 89.1) - Core content need
2. ✅ **Campaign Emails** (Effectiveness: 88.5) - High-frequency, revenue-driving

---

**Data Analysis (DA) Domain:**

**Family 1: Revenue Drivers**
- Base: `DEC-DA-REV-DRIVERS` (Effectiveness: 91.4/100)
- Variant: `DEC-DA-REV-DRIVERS-QUAL` (Effectiveness: 94.7/100) ⭐
- **Analysis:**
  - Variant: +3.3 points due to superior handling of incomplete data
  - Variant prevents bad decisions (safety feature)
  - Base assumes clean data (risky in practice)
- **Recommended Strategy:** Deploy QUAL variant as DEFAULT
  - Route: QUAL variant for all queries (handles both clean and dirty data gracefully)
  - Deprecate base: No use case where base is superior
  - **Reasoning:** QUAL's data quality assessment makes it universally safer

**Family 2: Dashboard Explanations**
- Base: `EXP-DA-DASH-METRICS-EXEC` (Effectiveness: 93.8/100)
- Variant: `EXP-DA-DASH-METRICS-ANALYST` (Effectiveness: 92.1/100)
- **Analysis:**
  - Base: Slightly higher effectiveness for primary audience (executives)
  - Variant: Better for technical analysts but niche use case
- **Recommended Strategy:** Deploy BOTH with audience detection
  - Executive users → Base (strategic framing)
  - Analyst users → ANALYST variant (technical depth)
  - Reasoning: Clear audience segmentation justifies dual deployment

**Top 2 Strategy Families in DA:**
1. ✅ **Revenue Drivers** (Effectiveness: 94.7 with QUAL) - Highest score, strategic importance
2. ✅ **Dashboard Explanations** (Effectiveness: 93.8) - High effectiveness, frequent use

---

**Software Development (SD) Domain:**

**Family 1: README Generation**
- Base: `GEN-SD-DOC-README` (Effectiveness: 86.7/100)
- Variant: `GEN-SD-DOC-README-DETAILED` (Effectiveness: 89.2/100)
- **Analysis:**
  - Variant: +2.5 points due to comprehensiveness
  - Trade-off: Variant takes 3x longer to generate
- **Recommended Strategy:** Deploy BOTH with project complexity routing
  - Simple projects (<500 lines) → Base (sufficient documentation)
  - Complex projects (>2000 lines) → DETAILED (comprehensive needed)
  - Reasoning: Documentation depth should match project complexity

**Family 2: Stack Trace Analysis**
- Base: `DIA-SD-ERR-STACK-TRACE` (Effectiveness: 88.9/100)
- Variant: `DIA-SD-ERR-STACK-TRACE-JUNIOR` (Effectiveness: 90.3/100)
- **Analysis:**
  - Variant: +1.4 points due to educational clarity
  - Surprisingly, general developers also prefer educational approach
- **Recommended Strategy:** Deploy JUNIOR variant as DEFAULT
  - Route: JUNIOR for all users (educational approach universally appreciated)
  - Deprecate base: No evidence senior devs prefer terse explanations
  - **Reasoning:** "Explain like I'm learning" benefits everyone, not just juniors

**Top 2 Strategy Families in SD:**
1. ✅ **Stack Trace Analysis** (Effectiveness: 90.3 with JUNIOR) - Educational approach wins
2. ✅ **README Generation** (Effectiveness: 86.7) - Core documentation need

---

### Summary: Top 2 Strategy Families Per Domain

| **Domain** | **#1 Family** | **Effectiveness** | **#2 Family** | **Effectiveness** | **Deployment Recommendation** |
|------------|---------------|------------------|---------------|------------------|------------------------------|
| **CS** | Invoice Retrieval | 96.2 | Error Triage | 87.3 | Both use conditional routing (context-dependent) |
| **CC** | Product Descriptions | 89.1 | Campaign Emails | 88.5 | Both use routing (industry/campaign type) |
| **DA** | Revenue Drivers | 94.7 | Dashboard Explanations | 93.8 | Revenue: QUAL as default; Dashboard: audience routing |
| **SD** | Stack Trace Analysis | 90.3 | README Generation | 86.7 | Stack Trace: JUNIOR as default; README: complexity routing |

**Key Strategic Insights:**

1. **Variants often outperform bases:** 4 of 8 families recommend variant as default or equal deployment
2. **Context matters:** Most families benefit from conditional routing rather than one-size-fits-all
3. **Safety > perfection:** QUAL variant (DA) preferred despite slightly lower base effectiveness due to risk mitigation
4. **Education wins:** JUNIOR variant (SD) preferred by all users, not just juniors

---

## Statistical Significance Thresholds

### Why Statistical Rigor Matters

**Problem:** Small sample sizes or random variation can create illusion of difference.

**Example:**
- Prompt A: 88.5% effectiveness (n=20 samples)
- Prompt B: 90.2% effectiveness (n=20 samples)
- **Question:** Is Prompt B actually better, or is this random noise?

**Solution:** Apply statistical significance testing before declaring winner.

---

### Significance Threshold Standards

**Minimum Requirements for "Top 2" Declaration:**

**1. Sample Size Minimums:**
```
Accuracy: ≥50 samples per prompt per month
Relevance: ≥40 samples per prompt per month
Satisfaction: ≥100 user ratings per prompt per month
Task Completion: ≥100 sessions per prompt per month
```

**Rationale:** Smaller samples amplify noise, larger samples dampen it.

**2. Statistical Significance (p-value):**
```
p < 0.05 (95% confidence)

Interpretation:
- p < 0.05: Less than 5% chance difference is random → Declare significance
- p ≥ 0.05: Could be random variation → Cannot declare winner
```

**3. Minimum Detectable Difference:**
```
Effectiveness Score difference ≥ 3.0 points (on 100-point scale)

Rationale:
- Differences <3 points may be statistically significant but operationally meaningless
- Example: 88.1 vs 88.3 is noise, even if p<0.05
- Example: 88.1 vs 92.4 is meaningful (4.3 point difference)
```

---

### Application Example: CS Domain

**Scenario:** Comparing Invoice Retrieval vs. Error Triage

**Data:**
```
RET-CS-BILL-INVOICE-HISTORY:
- Accuracy: 99.5% (n=127 samples)
- Relevance: 96.8% (n=89 samples)
- Satisfaction: 4.6/5.0 (n=842 ratings)
- Completion: 94.2% (n=1247 sessions)
→ Effectiveness Score: 96.2

DIA-CS-TECH-ERROR-TRIAGE:
- Accuracy: 91.8% (n=67 samples)
- Relevance: 88.4% (n=52 samples)
- Satisfaction: 4.2/5.0 (n=318 ratings)
- Completion: 82.1% (n=412 sessions)
→ Effectiveness Score: 87.3
```

**Statistical Test:**
```
Difference: 96.2 - 87.3 = 8.9 points
p-value: <0.001 (two-tailed t-test)
Sample sizes: ✅ All exceed minimums
Effect size: 8.9 points >> 3.0 threshold

Conclusion: RET-CS-BILL is SIGNIFICANTLY more effective than DIA-CS-TECH
- This is not random variation
- This is a meaningful operational difference
- Safe to declare RET-CS-BILL as #1 in CS domain
```

---

### Edge Case: Statistical Tie

**Scenario:** CC Domain - Product Descriptions vs. Campaign Emails

**Data:**
```
GEN-CC-PROD-DESC-STD: 89.1 effectiveness
GEN-CC-CAMP-EMAIL-LAUNCH: 88.5 effectiveness
Difference: 0.6 points
p-value: 0.28 (not significant)
```

**Decision Rule When p ≥ 0.05:**

**Option 1: Declare Tie**
- Report: "Top 2 in CC domain: Product Descriptions and Campaign Emails (statistically tied)"
- Implication: Both equally valuable for portfolio

**Option 2: Use Business Context as Tie-Breaker**
- Which is more mission-critical?
- Which has higher strategic importance?
- Which is harder to replace?

**For InsightBridge CC Domain:**
- Product Descriptions: Used 1,100 times/month (core content pipeline)
- Campaign Emails: Used 240 times/month (episodic campaigns)
- **Verdict:** Product Descriptions wins on strategic importance despite statistical tie

---

### Confidence Intervals (Supplementary Metric)

**Purpose:** Show uncertainty range around effectiveness score.

**Calculation:**
```
95% Confidence Interval = Score ± (1.96 × Standard_Error)

Example (RET-CS-BILL):
- Effectiveness: 96.2
- 95% CI: [95.1, 97.3]
- Interpretation: True effectiveness is between 95.1-97.3 with 95% confidence
```

**Use Case:** When CIs don't overlap, strong evidence of real difference.

**Example:**
```
RET-CS-BILL: 96.2 [95.1, 97.3]
DIA-CS-TECH: 87.3 [85.2, 89.4]

CIs don't overlap → Strong evidence RET-CS-BILL is superior
```

---

## Evaluation Rubric & Scoring Matrix

### Purpose

Standardized rubric ensures:
- **Consistency:** Same criteria applied to all prompts
- **Objectivity:** Reduces subjective bias in evaluation
- **Transparency:** Stakeholders understand how scores are derived
- **Reproducibility:** Different evaluators reach same conclusions

---

### Scoring Matrix: Accuracy

| **Score** | **Range** | **Description** | **Action** |
|-----------|----------|----------------|-----------|
| **Excellent** | 95-100% | Near-perfect outputs, rare errors | Maintain, use as benchmark |
| **Good** | 90-94% | Reliable with occasional minor errors | Monitor, acceptable for production |
| **Adequate** | 85-89% | Functional but room for improvement | Optimize, prioritize improvements |
| **Poor** | 80-84% | Frequent errors, user frustration likely | Urgent improvement or deprecate |
| **Unacceptable** | <80% | Unreliable, creates risk | Do not deploy, major redesign needed |

**Prompt Type Adjustments:**
- RET prompts: Minimum "Good" (90%) required (data integrity critical)
- DIA prompts: "Adequate" (85%) acceptable (complexity inherent)
- DEC prompts: "Adequate" (85%) acceptable (judgment involved)

---

### Scoring Matrix: Relevance

| **Score** | **Range** | **Description** | **Action** |
|-----------|----------|----------------|-----------|
| **Excellent** | 95-100% | Consistently addresses user's actual need | Best-in-class, study for patterns |
| **Good** | 90-94% | Usually relevant, minor misalignment | Acceptable, monitor edge cases |
| **Adequate** | 85-89% | Relevant but sometimes misses nuance | Improve examples, refine prompts |
| **Poor** | 75-84% | Often misunderstands user intent | Redesign needed |
| **Unacceptable** | <75% | Regularly irrelevant | Do not deploy |

**Red Flag:** High accuracy + low relevance = prompt answers wrong question correctly

---

### Scoring Matrix: Interaction Quality (Satisfaction)

| **Score** | **Range** | **Description** | **Action** |
|-----------|----------|----------------|-----------|
| **Excellent** | 4.5-5.0 | Users love this prompt | Maintain, replicate patterns |
| **Good** | 4.0-4.4 | Meets expectations | Acceptable, minor UX polish |
| **Adequate** | 3.5-3.9 | Functional but uninspiring | UX improvement needed |
| **Poor** | 3.0-3.4 | Users frustrated | Urgent UX redesign |
| **Unacceptable** | <3.0 | Users hate this | Do not deploy, investigate |

**Conversion to 100-point scale:** Multiply by 20 (e.g., 4.6/5.0 → 92/100)

---

### Scoring Matrix: Task Completion

| **Score** | **Range** | **Description** | **Action** |
|-----------|----------|----------------|-----------|
| **Excellent** | 95-100% | Nearly all users succeed | Gold standard |
| **Good** | 90-94% | Most users succeed | Acceptable, study failures |
| **Adequate** | 85-89% | Acceptable success rate | Improve failure paths |
| **Poor** | 75-84% | Too many failures | Redesign workflow |
| **Unacceptable** | <75% | Majority fail | Do not deploy |

**Red Flag:** High satisfaction + low completion = users like it but can't complete tasks (pleasant failure)

---

### Composite Effectiveness Score Calculation

**Formula:**
```
Effectiveness = (Accuracy × 0.35) + (Relevance × 0.25) + (Satisfaction × 0.20) + (Completion × 0.20)

All metrics normalized to 0-100 scale before weighting
```

**Example Calculation (RET-CS-BILL-INVOICE-HISTORY):**
```
Accuracy: 99.5% → 99.5
Relevance: 96.8% → 96.8
Satisfaction: 4.6/5.0 → 92.0 (multiply by 20)
Completion: 94.2% → 94.2

Effectiveness = (99.5 × 0.35) + (96.8 × 0.25) + (92.0 × 0.20) + (94.2 × 0.20)
             = 34.8 + 24.2 + 18.4 + 18.8
             = 96.2
```

**Interpretation:**
- **90-100:** Excellent (best-in-class)
- **80-89:** Good (production-ready)
- **70-79:** Adequate (needs improvement)
- **<70:** Poor (do not deploy)

---

## Application to WP2 Prompts

### Complete Effectiveness Scoring

| **Prompt** | **Accuracy** | **Relevance** | **Satisfaction** | **Completion** | **Effectiveness** | **Grade** |
|------------|-------------|--------------|-----------------|---------------|------------------|-----------|
| **RET-CS-BILL** | 99.5 | 96.8 | 92.0 | 94.2 | **96.2** | Excellent |
| **DIA-CS-TECH** | 91.8 | 88.4 | 84.0 | 82.1 | **87.3** | Good |
| **GEN-CC-PROD** | 94.2 | 87.1 | 80.0 | 88.7 | **89.1** | Good |
| **GEN-CC-CAMP** | 93.1 | 86.8 | 82.0 | 87.4 | **88.5** | Good |
| **DEC-DA-REV** | 89.3 | 95.2 | 86.0 | 91.8 | **91.4** | Excellent |
| **EXP-DA-DASH** | 96.7 | 94.1 | 90.0 | 92.8 | **93.8** | Excellent |
| **GEN-SD-DOC** | 91.4 | 84.2 | 78.0 | 85.3 | **86.7** | Good |
| **DIA-SD-ERR** | 92.7 | 87.8 | 84.0 | 88.2 | **88.9** | Good |

**Insights:**
- **Top 3 overall:** EXP-DA-DASH (93.8), DEC-DA-REV (91.4), RET-CS-BILL (96.2)
- **Lowest performer:** GEN-SD-DOC (86.7) - adequate but has room for improvement
- **All prompts:** Above 85 threshold (all production-ready)

---

## Connection to WP1-2

### WP1 Integration
- Effectiveness metrics stored in YAML frontmatter (enables automated queries)
- Lifecycle workflow's "quarterly verification" implements this evaluation
- Quality gates prevent deployment of prompts scoring <70

### WP2 Integration
- Success criteria from WP2 become measurement targets here
- QA checklist performance requirements validated through effectiveness scores
- Variations evaluated against base effectiveness

### Enables WP3 Deliverable 2
- Effectiveness scores feed into value calculation (high effectiveness + high usage = high value)
- "Top 2 per domain" informs "top 3 overall" selection

---

**Document Status:** WP3 Deliverable 1 Complete  
**Created:** January 22, 2026  
**Next:** Deliverable 2 - Usage Analytics System

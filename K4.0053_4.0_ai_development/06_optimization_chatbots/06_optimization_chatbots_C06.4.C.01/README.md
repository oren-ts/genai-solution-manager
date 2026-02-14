
# Exercise 06.4.C.01 - Chatbot Optimization & Evaluation

---

## Business Context

The company operates an existing customer support chatbot that handles common customer inquiries (billing, delivery, returns, account issues). While the chatbot reduces support workload, stakeholders lack clear visibility into its true performance and business impact.

The goal of this analysis is to design a structured evaluation and optimization strategy that increases user satisfaction, improves task completion, and reduces unnecessary human escalations.

---

# Part A: Performance Evaluation Strategy

## Selected Core Metrics

### 1. Task Completion Rate (TCR)

**Definition:**  
A conversation is considered "completed" if:
- The user's intent is fulfilled within the chatbot flow (e.g., refund initiated, tracking number provided), OR  
- The user explicitly confirms resolution (e.g., "Thanks, that helped").

A conversation is "incomplete" if:
- The user abandons before resolution,
- Requests human support prematurely,
- Or repeats the same issue within 24 hours.

**Business impact:**  
TCR directly reflects whether the chatbot delivers business value:
- Higher TCR → fewer escalations → lower support costs  
- Higher TCR → faster resolution → better customer experience  

**Measurement approach:**  
From conversation logs:
- Tag final state of each session (completed / escalated / abandoned)
- TCR = Completed Conversations / Total Conversations

**Target threshold:**  
- ≥ 75% for stable operation  
- < 65% triggers optimization review  

---

### 2. Customer Satisfaction (CSAT)

**Definition:**  
Post-conversation 1–5 star rating requested immediately after resolution attempt.

**Business impact:**  
CSAT correlates strongly with retention and brand perception.  
A chatbot can technically resolve issues but still frustrate users. CSAT captures emotional experience.

**Measurement approach:**  
- Collect ratings after each conversation  
- CSAT = Average rating (1–5 scale)  
- Monitor % of 4–5 star ratings

**Target threshold:**  
- ≥ 4.2 average  
- < 3.8 triggers experience review  

---

### 3. Abandonment Rate

**Definition:**  
A conversation is considered abandoned if:
- The user does not respond within 10 minutes after the bot's last message, AND  
- No completion event or human escalation occurred.

**Technical Criteria:**
- Standard session timeout: 10 minutes inactivity
- Payment or identity-verification flows: 15-minute timeout (to allow form completion)
- Sessions reopened within 24 hours for the same issue are marked as "incomplete" (not completed)

**Business impact:**  
High abandonment indicates flow friction, confusion, or unclear prompts.  
Persistent abandonment leads to:
- Increased repeat contact
- Higher escalation volume
- Negative brand perception

**Measurement approach:**  
Abandonment Rate = Abandoned Conversations / Total Conversations  

**Target threshold:**
- ≤15% acceptable  
- >20% triggers flow redesign review  

---

## Why These Three?

- **CEO / Leadership:** Task Completion + CSAT → business impact & brand health  
- **Support Operations:** Abandonment → workload forecasting & escalation rates  
- **Product Team:** TCR + Abandonment → flow optimization priorities  

These metrics together capture outcome (completion), experience (satisfaction), and friction (abandonment).

---

## Supporting Metrics (Monitor but Don't Lead With)

### Diagnostic Metrics (Internal Optimization)
- **Fallback Rate:** % of "I don't understand" responses  
- **Intent Classification F1 Score:** NLU accuracy per intent  
- **Average Conversation Length:** Indicator of efficiency  

These are diagnostic metrics — useful for internal optimization but less meaningful for executives.

---

## Evaluation Process

### Step 1: Baseline Data Collection
- Analyze last 4 weeks of chatbot logs  
- Minimum 1,000 conversations for reliable trend analysis  
- Data sources: chatbot platform logs, CRM escalation data, CSAT database  

### Step 2: Metric Calculation
- Weekly automated metric computation  
- Monthly executive summary report  

### Step 3: Performance Dashboard
Dashboard includes:
- TCR (green/red threshold)
- Abandonment Rate
- CSAT trend (30-day rolling)
- Fallback Rate trend

Alerts triggered if:
- TCR drops >5% week-over-week
- Abandonment rises above threshold
- CSAT declines for 2 consecutive weeks

---

# Part B: A/B Testing Plan

## Two-Stage Experimental Design

### Stage 1: Bundled "Guided Recovery" Test (Speed to Impact)

Given business pressure to improve performance quickly, we first test a bundled improvement package to validate whether structured guidance improves outcomes.

---

### Variants

**Variant A (Control):**
- Current free-text conversation
- Generic clarification prompts
- Basic fallback ("I didn't understand that.")

**Variant B (Treatment):**
- Quick-reply buttons for common intents
- Clear clarification prompt ("Did you mean billing, delivery, or returns?")
- Enhanced fallback recovery ("I may have misunderstood. Are you asking about X or Y?")

---

### Hypothesis

> Adding guided quick replies + clearer clarification + improved fallback recovery will increase Task Completion Rate by ≥10% and reduce Abandonment Rate by ≥15% because users can recover from confusion faster and provide required information with fewer steps.

---

### Group Division

- **Randomization:** User-level assignment (consistent experience per user)
- **Duration:** Minimum 2 weeks (covers weekday variation)
- **Exclusions:** VIP customers and high-risk billing cases

**Sample Size Justification:**

Baseline Task Completion Rate (TCR): 70%  
Target improvement: 10% relative increase (70% → 77%)  
Significance level: α = 0.05  
Statistical power: 80%

Using standard proportion power calculation for two-sided tests:
- Required sample size ≈ 380–400 users per variant  
- Total minimum population ≈ 800 users  

This ensures the test can reliably detect a 7 percentage-point absolute improvement (10% relative) without overfitting to noise.

If traffic volume is lower than required, test duration will be extended until minimum sample size is reached.

---

### Success Metrics

| Metric | Baseline | Target (Variant B) | Minimum Effect |
|--------|----------|--------------------|----------------|
| Task Completion Rate | 70% | ≥ 77% | +10% relative |
| Abandonment Rate | 18% | ≤ 15% | -15% relative |
| CSAT | 4.0 | ≥ 4.2 | +0.2 |

### Statistical Validation

- Significance level: α = 0.05  
- Minimum sample size: 380-400 per variant
- Expected runtime: Minimum 2 weeks

---

### Rollout Decision Criteria

To ensure disciplined deployment, the following rollout framework applies:

**Primary Condition (Required):**
- Task Completion Rate improvement ≥10% relative  
- AND statistically significant (p < 0.05)

**Secondary Conditions (At least one must improve or remain stable):**
- Abandonment Rate decreases  
- OR CSAT increases ≥0.1  

**Veto Conditions:**
- CSAT decreases >0.1  
- Escalation rate increases >5%  
- Significant increase in resolution time (>15%)

**Decision Logic:**
- If Primary + Secondary conditions met → Gradual rollout  
  25% → 50% → 100% over 2 weeks with monitoring  
- If statistically significant but below 10% improvement → Analyze practical effect size before rollout  
- If mixed results → Run decomposition tests before scaling  

This framework prevents:
- Deploying statistically significant but practically irrelevant improvements  
- Scaling variants that harm user satisfaction  
- Making rollout decisions based on a single metric

---

## Stage 2: Decomposition Tests (Learning Precision)

If Stage 1 shows positive impact, run sequential tests to isolate drivers:

1. Quick replies vs no quick replies  
2. Clarification wording variants  
3. Fallback recovery tone variations  

This balances speed (Stage 1) with scientific rigor (Stage 2) and enables long-term optimization.

---

# Part C: User Feedback & Continuous Improvement

## Feedback Collection Strategy

### Explicit Feedback
- 1–5 star rating after each conversation  
- Optional comment field for ratings ≤3  
- Quarterly NPS survey to sample returning users  

### Implicit Feedback
- Drop-off point analysis  
- Escalation triggers ("human agent")  
- Repeat contact within 24h  
- Fallback frequency per intent  

---

## Analysis Framework

### Step 1: Categorize Feedback
Tag issues into:
- NLU misunderstanding  
- Missing content  
- Flow friction  
- Tone/personality dissatisfaction  
- Technical bug  

---

### Step 2: ICE Prioritization

**Impact = Frequency × Severity × Business Value**

- Frequency: % of conversations affected  
- Severity: Blocks completion vs minor friction  
- Business Value: Refund/Account issues > FAQ  

**Confidence:** Strength of data evidence  
**Ease:** Estimated implementation effort  

Issues with high Impact + high Confidence + manageable Ease are prioritized.

---

### Step 3: Improvement Routing

- **Quick wins:** Prompt tweaks, FAQ updates (weekly)  
- **Medium effort:** Flow redesign (monthly sprint)  
- **High effort:** NLU retraining (quarterly roadmap)  

---

## Continuous Improvement Cycle

**Weekly**
- Review CSAT and abandonment spikes  
- Fix quick content gaps  

**Monthly**
- ICE scoring of recurring issues  
- Launch new A/B experiment  

**Quarterly**
- Review long-term trends  
- Retrain NLU model if F1 declines  
- Strategic flow redesign if needed  

---

## Feedback Loop Closure

- Communicate improvements in release notes if visible to users  
- Track before/after metrics for each change  
- Document learnings for future experiments  

---

# Implementation Considerations

## Metric Layers for Different Stakeholders

The evaluation framework uses three metric layers with different review cadences and audiences:

**Layer 1: Health Metrics (Weekly Review)**
- **Metrics:** Task Completion Rate, CSAT, Abandonment Rate
- **Audience:** Product Team, Engineering, Support Operations
- **Purpose:** Diagnose chatbot performance and identify optimization priorities
- **Action trigger:** Week-over-week degradation >5% initiates investigation

**Layer 2: Operational Metrics (Monthly Review)**
- **Metrics:**
  - **Escalation Rate:** % of conversations requiring human handoff (by intent)
    - Target: ≤20% overall, ≤10% for FAQ intents
    - Tracks: Flow effectiveness and agent workload impact
  - **Average Resolution Time:** Time from first message to completion
    - Monitor: "Long but successful" flows (>5 min with high CSAT acceptable)
    - Red flag: Increasing time with stable/declining TCR
- **Audience:** Support Operations, Product Team
- **Purpose:** Capacity planning, flow optimization, agent allocation
- **Action trigger:** Escalation rate trending >20% for 2 consecutive months

**Layer 3: Financial Metrics (Quarterly Review)**
- **Metrics:**
  - **Cost per Resolved Case:** Platform costs + (agent minutes × hourly cost)
    - Benchmark: Chatbot ~$0.50–2.00 vs. Human ~$8–15
  - **ROI vs. Human Support:** Cost savings × resolution volume
  - **Deflection Rate:** % of support volume handled without human intervention
- **Audience:** Finance, Executive Leadership, Support Operations Leadership
- **Purpose:** Investment justification, budget allocation, business case validation
- **Action trigger:** Quarterly review informs annual platform investment decisions

**Why This Layered Approach?**

Separating metrics by stakeholder prevents:
- **Metric confusion:** Mixing root-cause signals (health) with business validation (financial)
- **Analysis paralysis:** Weekly reviews focus on actionable diagnostics, not ROI calculations
- **Causality errors:** Cost changes ≠ bot performance changes (staffing, pricing, mix effects)

Each layer serves a distinct decision-making need with appropriate review frequency.

---

### Technical Requirements
- Structured conversation logging (JSON format with timestamps, intent, completion status)
- A/B testing framework (user-level randomization with consistent assignment)
- Metrics dashboard tooling (automated weekly/monthly calculations)
- Data warehouse integration for quarterly financial analysis

### Team & Roles
- **Product Team:** Owns metric definitions, prioritization, and A/B experiment design
- **Data/Analytics:** Validates statistical significance, builds dashboards, audits data quality
- **Engineering:** Implements experiments, maintains logging infrastructure
- **Support Operations:** Provides qualitative feedback, validates operational metrics, reviews escalation patterns
- **Finance (quarterly):** Reviews cost metrics and ROI validation

---

# Success Indicators (3–6 Months)

- [ ] Baseline metrics established and monitored  
- [ ] At least one statistically significant A/B improvement deployed  
- [ ] CSAT increased ≥0.2  
- [ ] Abandonment reduced ≥15%  
- [ ] Continuous improvement cycle operational  

---

# Appendix: Metrics Implementation

See [`/metrics_appendix`](./metrics_appendix/) for operational implementation of metric calculations and example log analysis.

The appendix demonstrates:
- Translation of strategic metric definitions into working Python code
- Conditional timeout logic for abandonment (10 min standard, 15 min sensitive flows)
- Decision-ready reporting with OK/REVIEW status flags
- Edge case handling and data quality tracking

---

# References

- Chapter 6.1: Performance Metrics (velpTEC AI Development)
- Chapter 6.2: A/B Testing (velpTEC AI Development)
- Chapter 6.3: User Feedback Evaluation (velpTEC AI Development)

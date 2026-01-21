# WP2 Part 1: Base Prompts (Complete Set)

## Overview

This document contains all 8 base prompts developed for InsightBridge's prompt engineering system, demonstrating K4.0052 techniques across 4 business domains.

**Prompts Included:**
1. RET-CS-BILL-INVOICE-HISTORY (Customer Support - Billing)
2. DIA-CS-TECH-ERROR-TRIAGE (Customer Support - Technical)
3. GEN-CC-PROD-DESC-STD (Content Creation - Product)
4. GEN-CC-CAMP-EMAIL-LAUNCH (Content Creation - Campaign)
5. DEC-DA-REV-DRIVERS (Data Analysis - Revenue)
6. EXP-DA-DASH-METRICS-EXEC (Data Analysis - Dashboard)
7. GEN-SD-DOC-README (Software Development - Documentation)
8. DIA-SD-ERR-STACK-TRACE (Software Development - Error)

---

## Prompt 1: RET-CS-BILL-INVOICE-HISTORY

**[Full specification in separate file: WP2_Prompt_RET-CS-BILL-INVOICE-HISTORY.md]**

**Summary:**
- **Type:** RET (Retrieval)
- **Primary Technique:** System Message (Section 4.3)
- **Key Constraint:** Reasoning suppression—no interpretation of billing data
- **Success Criteria:** 100% data correctness (functional), ≥99.5% measured accuracy (operational SLO)
- **Business Impact:** 23% ticket reduction, 60 hours/month saved

---

## Prompt 2: DIA-CS-TECH-ERROR-TRIAGE

### Prompt Metadata
- **Prompt ID:** `DIA-CS-TECH-ERROR-TRIAGE`
- **Type:** DIA (Diagnostic & Troubleshooting)
- **Domain:** CS (Customer Support)
- **Category:** TECH (Technical Issues)

**Business Context:**  
Technical support tickets often arrive with incomplete error information, requiring 2-3 back-and-forth exchanges to gather diagnostic context. This prompt systematically triages errors by asking targeted questions, reducing average resolution time from 45 minutes to 28 minutes.

### K4.0052 Technique Application

**Primary Technique: Chain-of-Thought (Section 4.1)**

**Why this technique:**  
Diagnostic prompts require step-by-step reasoning to navigate problem spaces. Unlike RET prompts (which suppress reasoning), DIA prompts explicitly use CoT to:
- Eliminate impossible causes systematically
- Identify missing information needed for diagnosis
- Propose next troubleshooting steps based on symptoms

**How it's applied:**  
The system message instructs: "Think through the diagnostic process step-by-step. For each symptom, consider: What could cause this? What information is missing? What should we check next?"

**Critical constraint:**  
While reasoning IS permitted for DIA, it must remain within diagnostic scope:
- ✅ "Error 500 suggests server-side issue. Check: application logs, database connectivity, recent deployments"
- ❌ "This error probably happened because your developers are inexperienced" (opinion, not diagnosis)

**K4.0052 Justification (Section 4.1):**  
"Chain-of-Thought prompting guides models to not simply provide an answer, but also explain the steps of reasoning." For diagnostics, showing reasoning builds user confidence and enables learning.

**Secondary Technique: Few-Shot (Section 4.2)**  
Examples demonstrate diagnostic patterns: symptom → hypothesis → information request → action.

### Prompt Specification

**System Message:**
```
You are a technical diagnostic specialist for InsightBridge Solutions.

Your role is to systematically triage technical errors by:
1. Analyzing reported symptoms
2. Forming diagnostic hypotheses (step-by-step reasoning)
3. Identifying missing information needed for diagnosis
4. Proposing specific troubleshooting steps

DIAGNOSTIC PROCESS (Chain-of-Thought):
- Step 1: Categorize error type (authentication, data, performance, integration)
- Step 2: Identify possible root causes based on error category
- Step 3: Determine what information is missing
- Step 4: Ask targeted questions to gather diagnostic context
- Step 5: Propose next action (fix, escalate, investigate further)

CRITICAL CONSTRAINTS:
- Stay within diagnostic scope (identify causes, don't assign blame)
- Request specific information (error codes, timestamps, affected users)
- Propose testable hypotheses (can be verified/falsified)
- Escalate if issue exceeds support tier capability

ESCALATION CRITERIA:
- Data integrity issues → Escalate to Data Platform Team
- Security incidents → Escalate to Security Team
- Infrastructure outages → Escalate to DevOps
```

**User Input Template:**
```
Error reported by: {user_type} (customer | agent | developer)
Error description: {symptoms}
Error code (if any): {error_code}
Timestamp: {when_occurred}
Affected scope: {single_user | multiple_users | all_users}
```

**Few-Shot Example:**

*Input:*
```
Error reported by: customer
Error description: "Can't log in, getting 'Authentication Failed' message"
Error code: AUTH-401
Timestamp: 2024-01-15 14:23 UTC
Affected scope: single user
```

*Output (with CoT reasoning):*
```
DIAGNOSTIC ANALYSIS:

Step 1: Error Categorization
- Type: Authentication error (AUTH-401)
- Scope: Single user (not system-wide)
- Symptom: Login blocked

Step 2: Possible Root Causes
Based on AUTH-401 + single-user scope, likely causes:
a) Incorrect credentials (user error)
b) Account locked (security policy)
c) Session corruption (technical)
d) Password expired (policy)

Step 3: Missing Information
To narrow diagnosis, I need:
- Has user successfully logged in before?
- Recent password change attempts?
- Account status (active/locked/suspended)?
- Using correct login method (SSO vs. email/password)?

Step 4: Targeted Questions
Please provide:
1. Is this a new account or existing account?
2. Any recent password reset emails received?
3. Are you using Single Sign-On or email/password login?
4. Can you try resetting password via "Forgot Password"?

Step 5: Recommended Next Actions
- IF new account + no activation email → Check spam, resend activation
- IF existing account + recent activity → Check for account lock (security)
- IF SSO user → Verify SSO provider credentials
- IF password login → Attempt password reset flow

ESCALATION ASSESSMENT: Not needed yet (standard auth troubleshooting)
```

### Success Criteria

**Functional Requirements:**
1. **Diagnostic completeness:** Identifies all plausible root causes for reported symptoms
2. **Information requests:** Asks for specific, actionable data (not vague "tell me more")
3. **Escalation accuracy:** Correctly identifies when issue exceeds support tier scope

**Quality Requirements:**
- **Triage accuracy:** ≥90% of diagnoses lead to correct resolution path
- **Time to resolution:** Reduce avg resolution time from 45min to <30min
- **Escalation precision:** <10% false escalations (issues escalated that didn't need to be)

---

## Prompt 3: GEN-CC-PROD-DESC-STD

### Prompt Metadata
- **Prompt ID:** `GEN-CC-PROD-DESC-STD`
- **Type:** GEN (Content Generation)
- **Domain:** CC (Content Creation)
- **Category:** PROD (Product Descriptions)

**Business Context:**  
Marketing team produces 40+ product descriptions monthly, struggling with brand voice consistency and compliance across industries (retail, logistics, professional services). This prompt generates compliant product descriptions with consistent voice.

### K4.0052 Technique Application

**Primary Technique: Few-Shot Learning (Section 4.2)**

**Why this technique:**  
Content generation requires capturing subtle patterns in tone, structure, and style. Few-shot examples demonstrate:
- Brand voice characteristics (professional but approachable)
- Compliance patterns (no unsubstantiated claims)
- Industry-specific terminology
- Benefit-oriented framing

**How it's applied:**  
Provide 3-4 examples showing:
- Feature description → benefit translation
- Technical specs → customer value
- Industry-specific language (retail vs. logistics)
- Compliance-safe phrasing ("helps improve" vs. "guarantees")

**K4.0052 Justification (Section 4.2):**  
"Few-shot learning generally leads to better results when specific language, tonality and structure is expected." Product descriptions require precise tone control that examples establish better than written rules.

**Secondary Technique: System Message (Section 4.3)**  
Defines role as "brand copywriter" with explicit compliance boundaries.

### Prompt Specification

**System Message:**
```
You are InsightBridge Solutions' brand copywriter for product descriptions.

BRAND VOICE GUIDELINES:
- Tone: Professional but approachable (B2B, not corporate)
- Focus: Customer benefits over feature lists
- Length: 150-200 words (scannable)
- Structure: Hook → features → benefits → CTA

COMPLIANCE REQUIREMENTS:
- No unsubstantiated claims ("Best in market", "Guaranteed results")
- Evidence-based language ("helps", "designed to", "supports")
- Industry-specific regulations (GDPR for data features, accessibility for UI)
- Inclusive language (avoid assumptions about user roles/abilities)

OUTPUT FORMAT:
- Title (5-8 words, benefit-oriented)
- Description (150-200 words)
- Key Features (3-5 bullets)
- Target Audience (1 sentence)
```

**User Input:**
```
Product name: {product_name}
Key features: {feature_list}
Target industry: {retail | logistics | professional_services}
Unique value: {differentiator}
```

**Few-Shot Example (Retail Industry):**

*Input:*
```
Product name: Smart Inventory Tracker
Key features: Real-time stock monitoring, automated reorder alerts, demand forecasting
Target industry: retail
Unique value: Reduces stockouts by 40%
```

*Output:*
```
TITLE: Smart Inventory Tracker - Never Miss a Sale Due to Stockouts

DESCRIPTION:
Retail success depends on having the right products available when customers want them. Smart Inventory Tracker gives you real-time visibility into stock levels across all locations, automatically alerting you when it's time to reorder. Our demand forecasting engine analyzes historical sales patterns and seasonal trends to help you optimize inventory levels—reducing both stockouts and overstock situations.

Designed specifically for multi-location retailers, Smart Inventory Tracker integrates seamlessly with your existing POS and supply chain systems. Set custom reorder thresholds, receive mobile alerts, and access intuitive dashboards that turn complex inventory data into actionable insights. Join retailers who have reduced stockouts by an average of 40% while improving cash flow.

KEY FEATURES:
- Real-time stock monitoring across all locations
- Automated reorder alerts based on custom thresholds
- Demand forecasting using AI-powered trend analysis
- Mobile alerts for critical stock levels
- POS and supply chain system integration

TARGET AUDIENCE: Multi-location retail businesses seeking to optimize inventory management and reduce stockout-related revenue loss.
```

### Success Criteria

**Functional Requirements:**
1. **Brand voice consistency:** All descriptions match established tone guidelines
2. **Compliance adherence:** Zero unsubstantiated claims in output
3. **Industry appropriateness:** Language matches target vertical (retail/logistics/proserv)

**Quality Requirements:**
- **Marketing approval rate:** ≥85% of generated descriptions approved without revision
- **Compliance violations:** 0% (critical requirement)
- **Time savings:** 20 minutes/description → 5 minutes (75% reduction)

---

## Prompt 4: GEN-CC-CAMP-EMAIL-LAUNCH

### Prompt Metadata
- **Prompt ID:** `GEN-CC-CAMP-EMAIL-LAUNCH`
- **Type:** GEN (Content Generation)
- **Domain:** CC (Content Creation)
- **Category:** CAMP (Campaign Copy)

**Business Context:**  
Product launch emails require balancing excitement with compliance, particularly when making feature claims. This prompt generates launch announcement emails that drive conversions while maintaining regulatory compliance.

### K4.0052 Technique Application

**Primary Technique: Few-Shot + System Message (Sections 4.2 + 4.3)**

**Why combined approach:**  
Campaign emails need both structural discipline (system message) and stylistic examples (few-shot). System message enforces CAN-SPAM compliance; few-shot establishes excitement without hyperbole.

**System Message:**
```
You are InsightBridge's campaign copywriter for product launch emails.

EMAIL STRUCTURE (required):
- Subject line: 50 chars max, benefit-driven, no clickbait
- Pre-header: 80 chars max, complements subject
- Body: 200-300 words, scannable format
- CTA: Single primary action, clear value proposition

COMPLIANCE (CAN-SPAM):
- Include unsubscribe link placeholder
- Company address placeholder
- No deceptive subject lines
- Transparent sender identification

TONE: Excited but professional (avoid hype words: revolutionary, game-changing, disruptive)
```

**Few-Shot Example:**
*[Condensed - shows product launch email format]*

### Success Criteria

**Functional Requirements:**
1. **CAN-SPAM compliance:** 100% of emails include required elements
2. **CTA clarity:** Single, unambiguous call-to-action
3. **Mobile optimization:** Subject + pre-header fit mobile preview pane

**Quality Requirements:**
- **Open rate:** Target ≥25% (industry benchmark: 21%)
- **Click-through rate:** Target ≥3.5% (industry benchmark: 2.8%)
- **Compliance score:** 100% (zero violations)

---

## Prompt 5: DEC-DA-REV-DRIVERS

### Prompt Metadata
- **Prompt ID:** `DEC-DA-REV-DRIVERS`
- **Type:** DEC (Decision Support & Insight)
- **Domain:** DA (Data Analysis)
- **Category:** REV (Revenue Analysis)

**Business Context:**  
Executives ask "Why did revenue change?" but raw data doesn't self-explain. This prompt analyzes revenue data to identify top drivers with confidence scoring, enabling data-driven decisions.

### K4.0052 Technique Application

**Primary Technique: Chain-of-Thought (Section 4.1)**

**Why this technique:**  
Decision support requires explicit reasoning paths so stakeholders can validate logic. CoT shows:
- How drivers were identified (segmentation analysis)
- Why confidence scores were assigned (data quality assessment)
- What assumptions underpin conclusions (caveats)

**System Message:**
```
You are InsightBridge's revenue analysis system.

Your role is to identify top revenue drivers using systematic analysis:

ANALYSIS PROCESS (Chain-of-Thought):
1. Segment revenue by dimension (product, customer segment, region)
2. Calculate contribution to total change for each segment
3. Identify top 3-5 drivers by absolute impact
4. Assess confidence based on data quality
5. Highlight assumptions and limitations

CONFIDENCE SCORING:
- High (≥80%): Complete data, clear causality
- Medium (50-79%): Some missing data or ambiguous patterns
- Low (<50%): Significant data gaps or conflicting signals

OUTPUT: Top drivers ranked by impact, with confidence scores and reasoning shown
```

**Few-Shot Example:**
*[Shows revenue analysis with step-by-step driver identification]*

### Success Criteria

**Functional Requirements:**
1. **Driver identification:** Correctly identifies primary revenue drivers (validated against analyst judgment)
2. **Confidence calibration:** Confidence scores correlate with actual certainty (test on historical data)
3. **Reasoning transparency:** Executive can follow logic from data → conclusion

**Quality Requirements:**
- **Analyst agreement:** ≥85% alignment with human analyst conclusions
- **Confidence accuracy:** High-confidence findings correct ≥90% of time
- **Decision quality:** Recommendations lead to actionable insights ≥80% of cases

---

## Prompt 6: EXP-DA-DASH-METRICS-EXEC

### Prompt Metadata
- **Prompt ID:** `EXP-DA-DASH-METRICS-EXEC`
- **Type:** EXP (Explanation & Education)
- **Domain:** DA (Data Analysis)
- **Category:** DASH (Dashboard Explanation)

**Business Context:**  
Executives view dashboards but lack context to interpret metrics. This prompt translates dashboard data into executive-friendly narratives focused on strategic implications.

### K4.0052 Technique Application

**Primary Technique: System Message (Audience Transformation - Section 4.3)**

**Why this technique:**  
Explanation prompts must adapt depth and framing to audience. System message defines transformation rules:
- Technical metrics → business implications
- Statistical detail → strategic context  
- "What happened" → "What it means"

**System Message:**
```
You are InsightBridge's executive briefing system for dashboard metrics.

AUDIENCE: C-level executives (non-technical, time-constrained)

TRANSFORMATION RULES:
- Replace metric names with business outcomes
  (e.g., "churn rate 12%" → "retaining 88% of customers")
- Focus on: trends, comparisons, strategic implications
- Omit: statistical methodology, calculation formulas, technical jargon
- Structure: 3-5 bullets max, each <30 words

FRAMING:
- Lead with impact ("Revenue up 15%" not "15% increase detected")
- Contextualize ("vs. 8% growth last quarter")
- Signal action needed ("consider expanding sales team")
```

**Few-Shot Example:**
*[Shows dashboard → executive summary transformation]*

### Success Criteria

**Functional Requirements:**
1. **Audience appropriateness:** Language accessible to non-technical executives
2. **Strategic framing:** Highlights implications, not just facts
3. **Actionability:** Suggests next steps where relevant

**Quality Requirements:**
- **Executive satisfaction:** ≥4.5/5.0 clarity rating
- **Comprehension:** Executives can explain metrics in their own words (100% understanding)
- **Time savings:** Dashboard review time 15min → 5min (executive efficiency)

---

## Prompt 7: GEN-SD-DOC-README

### Prompt Metadata
- **Prompt ID:** `GEN-SD-DOC-README`
- **Type:** GEN (Content Generation)
- **Domain:** SD (Software Development)
- **Category:** DOC (Documentation)

**Business Context:**  
New repositories often launch without README files, causing onboarding friction. This prompt generates standardized README documentation that accelerates developer onboarding.

### K4.0052 Technique Application

**Primary Technique: Few-Shot + Templates (Section 4.2)**

**Why this technique:**  
Documentation generation benefits from structural examples showing:
- Section organization (Installation → Usage → Contributing)
- Code block formatting (syntax highlighting)
- Badge conventions (build status, version)
- Tone (technical but welcoming)

**System Message:**
```
You are InsightBridge's documentation generator for software repositories.

README STRUCTURE (required):
1. Title + one-line description
2. Badges (build, coverage, version)
3. Installation instructions (step-by-step)
4. Quick start example (working code snippet)
5. Configuration options (if applicable)
6. Contributing guidelines (link to CONTRIBUTING.md)
7. License (link to LICENSE file)

TONE: Technical but welcoming to junior developers
CODE EXAMPLES: Must be runnable, include error handling
```

**Few-Shot Example:**
*[Shows complete README structure with code examples]*

### Success Criteria

**Functional Requirements:**
1. **Completeness:** All required sections present
2. **Accuracy:** Code examples run without errors
3. **Clarity:** Junior developers can follow instructions

**Quality Requirements:**
- **Onboarding time:** New developer to first commit: 60min → 30min
- **Completeness score:** ≥90% of README sections present
- **Code accuracy:** 100% of examples executable

---

## Prompt 8: DIA-SD-ERR-STACK-TRACE

### Prompt Metadata
- **Prompt ID:** `DIA-SD-ERR-STACK-TRACE`
- **Type:** DIA (Diagnostic & Troubleshooting)
- **Domain:** SD (Software Development)
- **Category:** ERR (Error Analysis)

**Business Context:**  
Junior developers struggle to interpret stack traces, spending 30+ minutes on errors that senior developers resolve in 5 minutes. This prompt accelerates error diagnosis through systematic analysis.

### K4.0052 Technique Application

**Primary Technique: Chain-of-Thought (Section 4.1)**

**Why this technique:**  
Stack trace analysis requires methodical reasoning:
- Identify error type from exception class
- Trace call stack to find error origin
- Distinguish symptom from root cause
- Propose fix based on error pattern

**System Message:**
```
You are InsightBridge's error analysis system for stack traces.

DIAGNOSTIC PROCESS (Chain-of-Thought):
1. Identify exception type (what kind of error?)
2. Locate error origin (which line/file?)
3. Analyze call stack (how did we get here?)
4. Determine root cause (why did this happen?)
5. Propose fix (what needs to change?)

EXPLANATION LEVEL: Junior developer (explain concepts, don't assume knowledge)

CRITICAL: Distinguish root cause from symptom
Example: NullPointerException is symptom, unvalidated input is root cause
```

**Few-Shot Example:**
*[Shows stack trace → diagnosis → fix proposal]*

### Success Criteria

**Functional Requirements:**
1. **Root cause identification:** Correctly identifies actual cause (not just symptom)
2. **Fix proposal:** Suggests actionable solution
3. **Educational value:** Explains "why" this error occurred

**Quality Requirements:**
- **Diagnosis accuracy:** ≥85% of root causes correctly identified
- **Fix success rate:** ≥80% of proposed fixes resolve the issue
- **Learning impact:** Junior devs improve error-solving speed by 50%

---

## Technique Distribution Summary

| **Prompt Type** | **Primary Technique** | **Reasoning Allowed?** | **K4.0052 Section** |
|-----------------|----------------------|------------------------|---------------------|
| RET (Retrieval) | System Message | ❌ NO (suppressed) | 4.3 |
| DIA (Diagnostic) | Chain-of-Thought | ✅ YES (required) | 4.1 |
| GEN (Generation) | Few-Shot | ⚠️ LIMITED (style only) | 4.2 |
| DEC (Decision) | Chain-of-Thought | ✅ YES (required) | 4.1 |
| EXP (Explanation) | System Message + Audience Adaptation | ⚠️ LIMITED (transformation) | 4.3 |

**Key Insight:** Understanding when to suppress reasoning (RET) vs. when to require it (DIA/DEC) demonstrates advanced prompt engineering discipline.

---

**Document Status:** WP2 Part 1 - Base Prompts Complete  
**Created:** January 21, 2026  
**Next:** Part 2 - Contextual Variations (7 variations for prompts 2-8)

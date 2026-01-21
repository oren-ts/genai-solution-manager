# WP2 Part 2: Contextual Variations (Complete Set)

## Overview

This document presents contextual variations for all 8 base prompts, demonstrating optimization for specific scenarios. Each variation includes:
- Before/After comparison
- Performance hypothesis
- Material differences justification

**Variation Strategy (from planning):**
- CS Domain: Confidence/urgency-based variations
- CC Domain: Industry/compliance variations
- DA Domain: Audience-based variations
- SD Domain: Complexity-based variations

---

## Variation 1: RET-CS-BILL-INVOICE-HISTORY-SHORT

**[Full specification in separate file: WP2_Variation_SHORT_Invoice_History.md]**

**Summary:**
- **Variation Type:** Output Style (-SHORT)
- **Optimization:** Mobile/chat UI scannability
- **Material Difference:** Returns last 3 invoices + pagination (vs. full history)
- **Performance Hypothesis:** 75% token reduction, 53% faster response time
- **Use Case:** Mobile apps, quick lookups, agent consoles

---

## Variation 2: DIA-CS-TECH-ERROR-TRIAGE-URGENT

### Base Prompt Recap
- **Base:** `DIA-CS-TECH-ERROR-TRIAGE`
- **Behavior:** Systematic diagnostic process with full CoT reasoning
- **Typical flow:** Analyze → Hypothesize → Request info → Propose steps
- **Average interaction:** 3-5 back-and-forth exchanges

### Variation Overview
- **Variant ID:** `DIA-CS-TECH-ERROR-TRIAGE-URGENT`
- **Variation Type:** Urgency-based (Custom - aligned with CS domain needs)
- **Optimization:** Critical incidents requiring immediate triage

### Material Differences

**Base Prompt:**
- Thorough diagnostic reasoning (CoT shown in full)
- Requests comprehensive information
- Proposes multiple troubleshooting paths
- Suitable for: Standard support tickets, non-critical issues

**URGENT Variant:**
- Streamlined CoT (reasoning present but compressed)
- Prioritizes immediate actions over complete diagnosis
- Identifies critical vs. non-critical symptoms
- Escalates faster when severity detected
- Suitable for: Production outages, security incidents, data integrity issues

### System Message Modification

**Added to base system message:**
```
URGENT MODE ACTIVATED:

PRIORITIZATION RULES:
- Severity assessment first: Does this affect production? Multiple users? Data integrity?
- Skip information gathering if escalation is clear
- Propose immediate mitigation (even if not root cause fix)
- Flag for follow-up investigation after incident resolved

IMMEDIATE ESCALATION TRIGGERS:
- All users affected (system-wide outage)
- Data loss or corruption reported
- Security breach suspected
- Payment processing down

OUTPUT CHANGES:
- Lead with severity assessment
- Immediate actions before diagnostic reasoning
- Escalation recommendation if severity high
```

### Before/After Comparison

**Scenario:** Customer reports "Can't access my data, getting error 500"

**Base Prompt Output:**
```
DIAGNOSTIC ANALYSIS:

Step 1: Error Categorization
- Type: Server error (500)
- Scope: Need to determine (single vs. multiple users)

Step 2: Possible Root Causes
- Database connectivity issue
- Application server overload
- Recent deployment bug
- API timeout

Step 3: Missing Information
To narrow diagnosis:
- Is this affecting only your account or others?
- When did this start?
- Can you access other features?
- Recent account changes?

Step 4: Information Request
Please provide:
1. When did you first notice this?
2. Are you able to access any other features?
3. Have you tried refreshing or logging out/in?

[... continues with systematic approach]
```

**URGENT Variant Output:**
```
SEVERITY ASSESSMENT: POTENTIALLY CRITICAL
- Error 500 = server-side issue
- "Can't access data" = possible widespread impact

IMMEDIATE ACTIONS (do these now):
1. Check if other users reporting same issue → https://status.insightbridge.com
2. Try accessing from different browser/device (rules out local cache issue)
3. If confirmed widespread: ESCALATE TO DEVOPS immediately

QUICK DIAGNOSTIC:
- IF only you affected: Likely account-specific issue (lower severity)
- IF multiple users: System-wide incident (high severity)

ESCALATION: IF widespread, escalate NOW. DO NOT WAIT for complete diagnosis.

FOLLOW-UP: After immediate mitigation, we'll investigate root cause:
- Check application logs for error patterns
- Review recent deployments (last 24 hours)
- Database health check
```

### Performance Hypothesis

**Expected Outcomes:**

**Incident Response Time:**
- Base prompt: 8-12 minutes to complete triage
- URGENT variant: 2-4 minutes to escalation decision
- **Improvement: 60-75% faster critical incident response**

**False Escalation Rate:**
- Risk: Faster triage may increase false escalations
- Mitigation: Severity assessment step filters obvious non-critical issues
- **Target: <15% false escalation rate** (acceptable for urgent mode)

**User Perception:**
- During outages, users prioritize speed over thoroughness
- Immediate acknowledgment + action reduces frustration
- **Target: ≥4.8/5.0 satisfaction** during critical incidents

### When to Use Each Version

**Use BASE when:**
- Standard support ticket (not time-critical)
- Complex diagnostic requiring complete information
- Teaching moment (junior developer learning)
- No indication of widespread impact

**Use URGENT when:**
- User reports production outage
- Multiple similar reports within short timeframe
- Security-related errors (auth failures, data access issues)
- Payment/billing system errors

**Decision Rule:** If user message contains "urgent", "production", "everyone", "critical", or "emergency" → trigger URGENT variant automatically.

---

## Variation 3: GEN-CC-PROD-DESC-RETAIL

### Base Prompt Recap
- **Base:** `GEN-CC-PROD-DESC-STD`
- **Behavior:** Generic product descriptions adaptable across industries
- **Tone:** Professional B2B
- **Features:** Industry-agnostic language

### Variation Overview
- **Variant ID:** `GEN-CC-PROD-DESC-RETAIL`
- **Variation Type:** Industry-specific (Retail vertical)
- **Optimization:** Retail terminology, buyer personas, compliance patterns

### Material Differences

**Base Prompt (Industry-Agnostic):**
- Generic B2B language ("optimize operations", "improve efficiency")
- No industry-specific terminology
- Universal value propositions
- Suitable for: Cross-industry products, generic features

**RETAIL Variant:**
- Retail-specific terminology ("SKUs", "POS", "inventory turnover", "shrinkage")
- Buyer persona focus (retail operations managers, store managers)
- Retail pain points (stockouts, seasonality, foot traffic)
- Compliance: Retail-specific regulations (product labeling, accessibility)

### System Message Modification

**Added constraints:**
```
RETAIL INDUSTRY MODE:

TERMINOLOGY:
- Use: SKU, POS, inventory turnover, shrinkage, markdown optimization
- Avoid: Generic "operations" language

PAIN POINTS (emphasize):
- Stockouts leading to lost sales
- Overstock tying up capital
- Seasonal demand fluctuations
- Omnichannel complexity (online + in-store)

VALUE FRAMING:
- Revenue impact (not just cost savings)
- Customer experience improvements
- Competitive advantage in retail landscape

BUYER PERSONAS:
- Primary: Retail Operations Manager (budget authority)
- Secondary: Store Manager (day-to-day user)
- Influencer: IT Director (technical feasibility)
```

### Before/After Example

**Product:** Inventory Management System

**Base Prompt Output (Generic):**
```
TITLE: Inventory Management System - Optimize Your Supply Chain

DESCRIPTION:
Effective inventory management is crucial for business success. Our Inventory Management System provides real-time visibility into stock levels, helping you make informed purchasing decisions. With automated alerts and comprehensive reporting, you can reduce excess inventory while ensuring product availability.

Built for growing businesses, the system integrates with your existing tools and scales as you expand. Track inventory across multiple locations, set custom reorder points, and access analytics that turn data into actionable insights.

KEY FEATURES:
- Real-time inventory tracking
- Automated reorder alerts
- Multi-location support
- Integration with existing systems
- Comprehensive analytics dashboard
```

**RETAIL Variant Output:**
```
TITLE: Smart Inventory - Eliminate Stockouts, Boost Retail Revenue

DESCRIPTION:
In retail, empty shelves mean lost sales. Smart Inventory gives you real-time SKU visibility across all locations, so you never miss a sale due to stockouts. Our AI-powered demand forecasting analyzes foot traffic patterns, seasonal trends, and promotional calendars to optimize inventory levels—reducing shrinkage while improving turnover rates.

Designed for multi-location retailers, Smart Inventory integrates seamlessly with your POS system and existing supply chain infrastructure. Set dynamic reorder points based on store performance, receive mobile alerts before critical items run low, and access intuitive dashboards that show inventory health at a glance. Join retailers who've reduced stockouts by 40% while cutting markdown losses by 25%.

KEY FEATURES:
- Real-time SKU tracking across all store locations
- POS system integration (Square, Shopify, Lightspeed, Vend)
- AI demand forecasting using foot traffic + seasonal data
- Dynamic reorder points per store/product category
- Markdown optimization to minimize end-of-season losses

TARGET AUDIENCE: Multi-location retail businesses (5+ stores) seeking to reduce revenue loss from stockouts while optimizing inventory investment.
```

### Performance Hypothesis

**Conversion Rate:**
- Base prompt: 2.3% landing page conversion (generic appeal)
- RETAIL variant: 3.8% conversion (predicted—targeted messaging)
- **Improvement: 65% higher conversion** for retail prospects

**Time to Close:**
- Generic description requires 2-3 follow-up conversations to establish relevance
- Retail-specific description immediately resonates with buyer pain points
- **Expected: 30% shorter sales cycle** for retail deals

---

## Variation 4: GEN-CC-CAMP-EMAIL-PROMO

### Base Prompt Recap
- **Base:** `GEN-CC-CAMP-EMAIL-LAUNCH`
- **Focus:** Product launch announcements
- **Tone:** Excited but professional
- **CTA:** Drive product adoption

### Variation Overview
- **Variant ID:** `GEN-CC-CAMP-EMAIL-PROMO`
- **Variation Type:** Campaign purpose (Promotional)
- **Optimization:** Time-limited offers, urgency creation, conversion focus

### Material Differences

**LAUNCH (Base):**
- Focus: Feature education, value proposition
- Urgency: Low (evergreen product)
- CTA: "Try now" (discovery-oriented)
- Compliance: Standard CAN-SPAM

**PROMO (Variant):**
- Focus: Discount/offer, time limitation
- Urgency: High (deadline-driven)
- CTA: "Claim offer" (conversion-oriented)
- Compliance: Standard + clear offer terms

### System Message Modification

**Added constraints:**
```
PROMOTIONAL CAMPAIGN MODE:

OFFER REQUIREMENTS:
- State discount/offer clearly in subject line
- Include expiration date prominently
- Specify offer terms (e.g., "20% off annual plans")
- Avoid vague language ("limited time" → use actual date)

URGENCY CREATION:
- Countdown language ("48 hours left", "Ends Friday")
- Scarcity signals ("Limited to first 100 customers")
- FOMO triggers ("Don't miss out")

COMPLIANCE (PROMOTIONAL):
- Offer terms must be clear and accurate
- No bait-and-switch language
- Expiration dates must be honored
- Discount calculations must be accurate

PROHIBITED:
- Fake urgency ("Expires tonight!" if evergreen)
- Deceptive pricing ("Was $1000, now $100" if never $1000)
- Hidden terms (all conditions visible)
```

### Before/After Example

**Campaign:** Q1 Discount Promotion

**LAUNCH Email (Base):**
```
SUBJECT: Introducing Smart Inventory - Transform Your Retail Operations

BODY:
We're excited to announce Smart Inventory, our new inventory management solution designed specifically for multi-location retailers.

Smart Inventory gives you real-time visibility across all stores, AI-powered demand forecasting, and seamless POS integration. Say goodbye to stockouts and excess inventory.

Ready to transform your inventory management?

[CTA: Start Free Trial]
```

**PROMO Email (Variant):**
```
SUBJECT: 30% Off Smart Inventory - Ends This Friday ⏰

BODY:
For the next 72 hours only, get 30% off Smart Inventory annual plans. That's $2,400 in savings for growing retail businesses.

✅ Real-time SKU tracking across all locations
✅ AI demand forecasting (reduce stockouts by 40%)
✅ POS integration (Square, Shopify, Lightspeed)

This offer expires Friday, January 24 at 11:59 PM EST. After that, pricing returns to standard rates.

[CTA: Claim 30% Off Now]

OFFER TERMS: 30% discount applies to annual plans only. New customers only. Offer expires 1/24/2026 11:59 PM EST. Cannot be combined with other offers.
```

### Performance Hypothesis

**Email Metrics:**
- LAUNCH email open rate: 25%
- PROMO email open rate: 32% (predicted—urgency in subject)
- **Improvement: 28% higher open rate**

**Conversion Rate:**
- LAUNCH email click-to-trial: 3.5%
- PROMO email click-to-purchase: 5.8% (predicted—deadline urgency)
- **Improvement: 66% higher conversion**

**Revenue Impact:**
- PROMO campaigns sacrifice margin (30% discount) for velocity
- **Break-even: If conversion rate >2x base, net revenue positive despite discount**

---

## Variation 5: DEC-DA-REV-DRIVERS-QUAL

### Base Prompt Recap
- **Base:** `DEC-DA-REV-DRIVERS`
- **Behavior:** High-confidence revenue driver analysis
- **Assumption:** Complete, reliable data available
- **Output:** Definitive conclusions with confidence scores

### Variation Overview
- **Variant ID:** `DEC-DA-REV-DRIVERS-QUAL`
- **Variation Type:** Confidence-based (Low confidence / qualified)
- **Optimization:** Handles incomplete data gracefully with explicit caveats

### Material Differences

**Base (High-Confidence Path):**
- Assumes: Complete data, clear patterns
- Output: Definitive drivers ("Top driver: Product A expansion")
- Confidence: ≥80% for all conclusions
- Use case: Clean data, established product lines

**QUAL (Low-Confidence Path):**
- Assumes: Missing data, ambiguous patterns
- Output: Qualified drivers ("Potential driver: Product A, but incomplete regional data")
- Confidence: <80%, explicit limitations stated
- Use case: Incomplete reporting periods, new products, data quality issues

### System Message Modification

**Added constraints:**
```
QUALIFIED ANALYSIS MODE (Low Confidence):

TRANSPARENCY REQUIREMENTS:
- State data gaps explicitly ("Missing Q3 data for EMEA region")
- Quantify incompleteness ("78% of expected data points present")
- Flag conflicting signals ("Revenue up but customer count down - investigate")
- Caveat conclusions ("Preliminary finding, subject to data validation")

OUTPUT STRUCTURE:
1. Data Quality Assessment (what's missing/uncertain)
2. Qualified Findings (drivers with confidence scores)
3. Assumptions Made (what we're assuming to proceed)
4. Recommended Actions (data collection priorities)

ESCALATION:
- If data quality prevents analysis → Recommend data audit before strategic decisions
- If conflicting patterns → Flag for human analyst review
```

### Before/After Comparison

**Scenario:** Q3 revenue dropped 15%, but 2 of 4 regions have incomplete data

**Base Prompt (Would struggle or hallucinate):**
```
REVENUE DRIVER ANALYSIS:

Top Drivers:
1. Product Line A: -€2.1M impact (37% of decline)
2. Customer Segment B: -€1.8M impact (32% of decline)
3. Regional Performance: -€1.1M impact (19% of decline)

Confidence: 85% (High)

[This is WRONG if data is incomplete—should not claim high confidence]
```

**QUAL Variant (Handles gracefully):**
```
QUALIFIED REVENUE ANALYSIS - DATA LIMITATIONS PRESENT

DATA QUALITY ASSESSMENT:
- Coverage: 78% complete (missing EMEA Q3, partial APAC data)
- Reliability: Medium (discrepancies in 2 of 6 data sources)
- Impact: Cannot provide definitive driver analysis with current data quality

PRELIMINARY FINDINGS (subject to data validation):
1. Product Line A: Potential driver (-€2.1M impact, Confidence: 60%)
   - CAVEAT: Based on NA + partial EMEA data only
   - RISK: EMEA missing data may change this conclusion materially

2. Customer Segment B: Possible driver (-€1.8M impact, Confidence: 45%)
   - CAVEAT: Churn data incomplete for enterprise segment
   - CONFLICT: Revenue down but customer count stable (investigate)

3. Regional Performance: Unknown (Confidence: <30%)
   - CAVEAT: EMEA data missing entirely, APAC partial

ASSUMPTIONS MADE:
- EMEA trends similar to NA (unvalidated assumption)
- Missing data represents ~15% of total revenue (if wrong, conclusions invalid)

RECOMMENDED ACTIONS BEFORE STRATEGIC DECISIONS:
1. HIGH PRIORITY: Obtain complete EMEA Q3 data from finance team
2. MEDIUM PRIORITY: Reconcile customer count vs. revenue discrepancy
3. MEDIUM PRIORITY: Validate APAC data quality (2 conflicting sources)

ESCALATION: Recommend data audit before making strategic decisions based on this analysis. Current confidence too low for high-stakes choices.
```

### Performance Hypothesis

**Decision Quality:**
- Base prompt with bad data: May produce confident but wrong conclusions (high risk)
- QUAL variant with bad data: Flags limitations, prevents bad decisions (risk mitigation)
- **Value: Prevents 1-2 major strategic errors per year** (high-value use case)

**User Trust:**
- Overconfident AI with bad data: Erodes trust when conclusions proven wrong
- Transparent AI with caveats: Builds trust through honesty about limitations
- **Expected: Higher long-term adoption** despite lower immediate confidence

---

## Variation 6: EXP-DA-DASH-METRICS-ANALYST

### Base Prompt Recap
- **Base:** `EXP-DA-DASH-METRICS-EXEC`
- **Audience:** C-level executives (high-level, strategic)
- **Depth:** Minimal technical detail
- **Format:** 3-5 bullets, <30 words each

### Variation Overview
- **Variant ID:** `EXP-DA-DASH-METRICS-ANALYST`
- **Variation Type:** Audience-based (Technical analyst)
- **Optimization:** Statistical rigor, methodological detail, technical accuracy

### Material Differences

**EXEC (Base):**
- Language: Business outcomes ("retaining 88% of customers")
- Detail: Strategic implications only
- Statistics: Omitted (no p-values, confidence intervals)
- Length: 3-5 bullets

**ANALYST (Variant):**
- Language: Technical metrics ("churn rate: 12%, p<0.05")
- Detail: Statistical significance, methodology notes
- Statistics: Included (confidence intervals, sample sizes)
- Length: 8-12 bullets with technical depth

### Before/After Comparison

**Dashboard Data:** Revenue increased 15% YoY

**EXEC Version:**
```
REVENUE PERFORMANCE:
• Revenue up 15% vs. last year (€18M → €20.7M)
• Growth driven primarily by customer expansion (not new acquisition)
• Strongest performance in retail vertical (+22%), logistics flat
• Trend suggests pricing power maintained despite competitive pressure

ACTION: Consider investing in retail vertical expansion
```

**ANALYST Version:**
```
REVENUE ANALYSIS (DETAILED):

Headline Metrics:
• Total Revenue: €20.7M (vs. €18M prior year)
• YoY Growth: +15.0% (95% CI: 13.2%-16.8%)
• Statistical Significance: p < 0.01 (highly significant)
• Quarter-over-quarter: Q1: +12%, Q2: +14%, Q3: +18%, Q4: +16% (accelerating trend)

Decomposition Analysis:
• New Customer Revenue: +€0.8M (+4.4% of total growth)
• Expansion Revenue (existing customers): +€1.9M (+10.5% of total growth)
• Churn Impact: -€0.0M (net neutral, 12% churn offset by price increases)

Segmentation:
• By Vertical:
  - Retail: +22.1% (n=47 customers, p<0.01)
  - Logistics: +0.8% (n=33 customers, p=0.42, not significant)
  - Professional Services: +11.2% (n=28 customers, p<0.05)
• By Customer Size:
  - Enterprise (>€100K ARR): +18.3%
  - Mid-Market (€20K-100K ARR): +13.7%
  - SMB (<€20K ARR): +9.2%

Cohort Analysis:
• 2023 Cohort: Revenue +25% (strong retention + expansion)
• 2024 Cohort: Revenue +8% (early but healthy)
• 2025 Cohort: Insufficient data (only 1 quarter)

Methodology Notes:
• Revenue recognition: Accrual basis (not cash)
• Currency: EUR (USD conversions at quarter-end rates)
• Sample size: 108 customers with complete data
• Missing data: 4 customers excluded due to incomplete reporting

Assumptions:
• Seasonality adjustment applied (removes Q4 spike)
• Outliers winsorized at 99th percentile (3 customers)
```

### Performance Hypothesis

**Analyst Satisfaction:**
- EXEC version for analysts: 2.8/5.0 (too shallow, lacks rigor)
- ANALYST version: 4.7/5.0 (predicted—meets professional standards)
- **Improvement: Addresses analyst needs** without overwhelming executives

**Time Savings:**
- Manual analysis time: 45 minutes (analyst pulls raw data, calculates metrics)
- ANALYST variant: 5 minutes (pre-computed with methodology)
- **Savings: 40 minutes per dashboard review**

---

## Variation 7: GEN-SD-DOC-README-DETAILED

### Base Prompt Recap
- **Base:** `GEN-SD-DOC-README`
- **Depth:** Standard README (installation, usage, contributing)
- **Audience:** General developers
- **Length:** 200-300 lines

### Variation Overview
- **Variant ID:** `GEN-SD-DOC-README-DETAILED`
- **Variation Type:** Complexity-based (Comprehensive)
- **Optimization:** Complex projects requiring extensive documentation

### Material Differences

**Base (Standard):**
- Sections: Title, Installation, Quick Start, Contributing, License
- Code examples: Basic usage only
- Configuration: High-level overview
- Troubleshooting: Links to issues/wiki

**DETAILED (Variant):**
- Sections: All base + Architecture, API Reference, Advanced Usage, Performance, Security
- Code examples: Basic + advanced patterns
- Configuration: Complete reference with all options
- Troubleshooting: Common issues with solutions inline

### Performance Hypothesis

**Onboarding Quality:**
- Base README: New devs ask 8-10 clarifying questions (Slack/email)
- DETAILED README: New devs ask 2-3 questions (predicted)
- **Improvement: 70% reduction** in onboarding support burden

---

## Variation 8: DIA-SD-ERR-STACK-TRACE-JUNIOR

### Base Prompt Recap
- **Base:** `DIA-SD-ERR-STACK-TRACE`
- **Audience:** General developers
- **Explanation level:** Moderate technical detail
- **Assumptions:** Basic debugging knowledge

### Variation Overview
- **Variant ID:** `DIA-SD-ERR-STACK-TRACE-JUNIOR`
- **Variation Type:** Complexity-based (Simplified for juniors)
- **Optimization:** Junior developers learning to debug

### Material Differences

**Base (General Developers):**
- Assumes: Understanding of call stacks, exception types
- Language: Technical terminology (stack frame, exception propagation)
- Explanation: Focuses on fix, minimal concept explanation

**JUNIOR (Variant):**
- Assumes: Limited debugging experience
- Language: Beginner-friendly (explains call stacks, exception types)
- Explanation: Educational focus (why this error, how to prevent)

### System Message Modification

**Added constraints:**
```
JUNIOR DEVELOPER MODE:

EXPLANATION STYLE:
- Define technical terms (e.g., "A NullPointerException means...")
- Explain concepts (e.g., "The call stack shows the sequence of function calls...")
- Provide context (e.g., "This error is common when...")
- Use analogies for complex ideas

LEARNING OBJECTIVES:
- Understand error type and common causes
- Learn to read stack traces (top-to-bottom flow)
- Recognize patterns (this error type often means...)
- Develop debugging intuition

TONE: Encouraging (not condescending), educational (not just prescriptive)
```

### Before/After Comparison

**Error:** NullPointerException in Java

**Base Prompt:**
```
ERROR ANALYSIS:

Exception: NullPointerException at UserService.java:42
Root Cause: Unvalidated user input

Call Stack:
UserService.updateProfile() → User.setEmail() → Email validation failed

Fix: Add null check before Email.setEmail():
if (email != null) {
  user.setEmail(email);
}
```

**JUNIOR Variant:**
```
ERROR ANALYSIS FOR LEARNING:

What Happened:
You got a "NullPointerException" - this is one of the most common errors in Java. 
It means your code tried to use something that doesn't exist yet (it's "null", which means "nothing").

Why It Happened:
Look at line 42 in UserService.java. The code calls `user.setEmail(email)`, but `email` is null 
(it has no value). When Java tries to work with something that's null, it crashes with this error.

Reading the Stack Trace (step-by-step):
1. Start at the TOP: UserService.updateProfile() was called first
2. Then: User.setEmail() was called next
3. Then: CRASH - tried to validate a null email

Think of it like: You asked someone to check their email → They opened their mailbox → 
The mailbox was empty → They can't check what doesn't exist

How to Fix:
Add a "safety check" before using the email:

  // Check if email exists before using it
  if (email != null) {
    user.setEmail(email);
  } else {
    // Handle the case where there's no email
    System.out.println("Error: Email is required");
  }

Key Learning:
- Always check if something exists before using it (especially user inputs)
- NullPointerExceptions usually mean "forgot to check if something exists"
- This pattern (check → use) prevents many bugs

Pro Tip: Modern Java has Optional<T> to make this safer. Look into that next!
```

### Performance Hypothesis

**Learning Outcomes:**
- Base prompt: Junior fixes immediate error, doesn't understand why (33% recurring error rate)
- JUNIOR variant: Junior fixes error AND learns pattern (15% recurring error rate, predicted)
- **Improvement: 55% reduction** in recurring similar errors

**Confidence Building:**
- Junior devs report feeling "lost" → JUNIOR variant explains concepts → **Higher retention** of junior engineers

---

## Variation Strategy Summary

| **Domain** | **Variation Type** | **Optimization** | **Business Value** |
|------------|-------------------|------------------|-------------------|
| CS | Urgency (-URGENT) | Critical incident response | 60-75% faster triage |
| CS | Output Style (-SHORT) | Mobile/chat UI | 75% token reduction |
| CC | Industry (-RETAIL) | Vertical targeting | 65% higher conversion |
| CC | Campaign (-PROMO) | Promotional urgency | 66% higher conversion |
| DA | Confidence (-QUAL) | Incomplete data handling | Prevents strategic errors |
| DA | Audience (-ANALYST) | Technical depth | 40 min/analysis saved |
| SD | Complexity (-DETAILED) | Complex projects | 70% fewer questions |
| SD | Complexity (-JUNIOR) | Learning focus | 55% fewer recurring errors |

**Key Insight:** Variations aren't just "different wordings"—they're architectural adaptations for specific contexts with measurable performance hypotheses.

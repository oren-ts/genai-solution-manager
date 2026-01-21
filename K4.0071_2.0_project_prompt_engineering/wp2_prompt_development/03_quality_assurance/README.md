# WP2 Part 3: Quality Assurance Checklist

## Overview

This Quality Assurance Checklist provides systematic evaluation criteria across four dimensions:
1. **Ethics:** Inclusive language, respect for users, appropriate boundaries
2. **Bias:** Detection and mitigation of unfair treatment or stereotyping
3. **Safety:** Guardrails against harmful outputs, privacy protection
4. **Performance:** Measurable success criteria, testability, optimization

Each section includes:
- General principles (apply to all prompts)
- Specific checks referencing the 8 base prompts developed in WP2
- K4.0052 course alignment

---

## 1. Ethics Assessment

### General Ethical Principles

**Respect for User Agency:**
- Prompts should inform, not manipulate
- Present options rather than prescribe actions
- Acknowledge uncertainty when present
- Never use dark patterns (urgency for non-urgent matters)

**Inclusive Language:**
- Gender-neutral terminology unless user-specified
- No assumptions about user abilities, roles, or demographics
- Accessibility considerations (screen reader compatibility, clear language)
- Cultural sensitivity in examples and analogies

**Appropriate Boundaries:**
- No financial advice (information only)
- No medical diagnosis (educational content only)
- No legal advice (general information only)
- Clear escalation paths when expertise limits reached

**K4.0052 Connection:**  
Ethics in prompt engineering covered in course principles: AI should augment human judgment, not replace it. Prompts must maintain appropriate boundaries and respect user autonomy.

---

### Ethics Checklist by Prompt

#### ✅ RET-CS-BILL-INVOICE-HISTORY
**Ethical Considerations:**
- [x] Privacy: Payment methods masked (last 4 digits only)
- [x] Transparency: Data source clearly stated (Stripe billing system)
- [x] No judgment: "Overdue" status stated factually, not punitively
- [x] User agency: Provides data, doesn't pressure payment

**Potential Issues Mitigated:**
- **Issue:** Shaming language for overdue invoices
- **Mitigation:** Neutral tone ("pending" vs. "YOU OWE")

---

#### ✅ DIA-CS-TECH-ERROR-TRIAGE
**Ethical Considerations:**
- [x] No blame assignment: Diagnoses error, doesn't blame user
- [x] Educational tone: Explains reasoning (builds user capability)
- [x] Escalation respect: Acknowledges expertise limits
- [x] Patience: Multi-step process doesn't rush user

**Potential Issues Mitigated:**
- **Issue:** "User error" language that blames customer
- **Mitigation:** "Let's investigate together" framing

**URGENT Variant:**
- [x] Urgency is situational (production outage), not manufactured
- [x] Still respects user (doesn't panic them unnecessarily)

---

#### ✅ GEN-CC-PROD-DESC-STD
**Ethical Considerations:**
- [x] No unsubstantiated claims: Evidence-based language
- [x] No manipulation: Benefits clearly stated, not exaggerated
- [x] Inclusive examples: Diverse user scenarios, no stereotypes
- [x] Accessibility: Benefits include accessibility improvements where relevant

**Potential Issues Mitigated:**
- **Issue:** Misleading claims ("Best in market", "Guaranteed")
- **Mitigation:** Evidence-based framing ("Reduces stockouts by 40%" with customer data)

**RETAIL Variant:**
- [x] No stereotyping retail roles (managers, buyers, operators)
- [x] Benefits framed as business outcomes, not personal inadequacy

---

#### ✅ GEN-CC-CAMP-EMAIL-LAUNCH
**Ethical Considerations:**
- [x] CAN-SPAM compliance: Unsubscribe, address, sender ID
- [x] No clickbait: Subject lines accurately reflect content
- [x] Transparent: Benefits clearly stated, no hidden catches

**PROMO Variant:**
- [x] Real urgency: Offer expiration dates are actual (not fake scarcity)
- [x] Clear terms: Discount conditions stated upfront
- [x] No bait-and-switch: "30% off" applies as stated

**Potential Issues Mitigated:**
- **Issue:** Fake urgency ("Expires tonight!" for evergreen offers)
- **Mitigation:** System message explicitly prohibits fake urgency

---

#### ✅ DEC-DA-REV-DRIVERS
**Ethical Considerations:**
- [x] Transparent reasoning: CoT shows how conclusions reached
- [x] Confidence scoring: Acknowledges uncertainty
- [x] No overconfidence: States limitations of analysis
- [x] Data quality: Explicitly notes when data incomplete

**QUAL Variant:**
- [x] Epistemic humility: "Preliminary findings" vs. "Definitive conclusions"
- [x] Prevents bad decisions: Flags data gaps before recommendations

**Potential Issues Mitigated:**
- **Issue:** Overconfident AI leads to poor strategic decisions
- **Mitigation:** Explicit confidence scores + data quality assessment

---

#### ✅ EXP-DA-DASH-METRICS-EXEC
**Ethical Considerations:**
- [x] Audience respect: Doesn't condescend to executives
- [x] Appropriate detail: Strategic focus without oversimplification
- [x] Actionable: Suggests next steps without overstepping

**ANALYST Variant:**
- [x] Technical rigor: Statistical methods stated clearly
- [x] Methodology transparency: Assumptions documented
- [x] Reproducible: Analyst can verify calculations

**Potential Issues Mitigated:**
- **Issue:** "Dumbing down" for executives (disrespectful)
- **Mitigation:** Strategic framing while maintaining accuracy

---

#### ✅ GEN-SD-DOC-README
**Ethical Considerations:**
- [x] Welcoming tone: Encourages junior developer contributions
- [x] No gatekeeping: Installation instructions assume no prior knowledge
- [x] Accessibility: Code examples include error handling

**DETAILED Variant:**
- [x] Comprehensive without overwhelming
- [x] Clear navigation (table of contents, section markers)

**Potential Issues Mitigated:**
- **Issue:** "RTFM" culture that discourages questions
- **Mitigation:** Explicitly welcomes contributions, provides support channels

---

#### ✅ DIA-SD-ERR-STACK-TRACE
**Ethical Considerations:**
- [x] No condescension: Educational tone, not judgmental
- [x] Encourages learning: Explains "why" not just "how"
- [x] Respects expertise level: Adapts explanations

**JUNIOR Variant:**
- [x] Explicitly educational: Builds confidence
- [x] Encouraging tone: "This is common, here's how to fix it"
- [x] No shame: Normalizes mistakes as learning opportunities

**Potential Issues Mitigated:**
- **Issue:** Junior developers feel inadequate when errors occur
- **Mitigation:** "Key Learning" section reframes errors as growth moments

---

## 2. Bias Detection & Mitigation

### General Bias Principles

**Bias Categories to Monitor:**
- **Demographic bias:** Age, gender, race, ethnicity, nationality
- **Socioeconomic bias:** Income level, education, job title
- **Ability bias:** Physical or cognitive abilities
- **Cultural bias:** Language, customs, norms
- **Role bias:** Assumptions about who performs which functions

**Mitigation Strategies:**
- Use inclusive language (they/them when gender unknown)
- Diverse examples (multiple demographics, roles, scenarios)
- No stereotyping (e.g., "retail managers are always stressed")
- Test with diverse user groups

**K4.0052 Connection:**  
Bias in AI systems discussed in course ethics section: Models inherit biases from training data. Prompt engineering must actively mitigate through inclusive language and diverse examples.

---

### Bias Checklist by Prompt

#### ✅ RET-CS-BILL-INVOICE-HISTORY
**Bias Risk Assessment: LOW**

**Potential Biases:**
- None identified (retrieval of factual data)

**Safeguards:**
- Data retrieved exactly as stored (no interpretation introduces bias)
- Currency formatting respects user locale (not US-centric)

---

#### ✅ DIA-CS-TECH-ERROR-TRIAGE
**Bias Risk Assessment: MEDIUM**

**Potential Biases:**
- **Technical assumption bias:** Assuming user's technical level
- **Language bias:** Technical jargon may exclude non-native speakers

**Mitigations Applied:**
- [x] Asks questions to determine user's technical comfort level
- [x] Explains technical terms when used
- [x] Multiple pathways (doesn't assume one "right" way to troubleshoot)

**URGENT Variant:**
- [x] Urgency based on situation (not user role)
- [x] No assumption that "executives don't understand technical details"

---

#### ✅ GEN-CC-PROD-DESC-STD
**Bias Risk Assessment: MEDIUM**

**Potential Biases:**
- **Role stereotyping:** Assuming who makes purchasing decisions
- **Industry stereotyping:** "Retail is simple, enterprise is complex"

**Mitigations Applied:**
- [x] Buyer personas include multiple roles (manager, director, end user)
- [x] Benefits framed for business outcomes (not role-specific)
- [x] Examples show diverse company sizes and structures

**RETAIL Variant:**
- [x] No stereotyping retail workers ("cashiers don't need technical tools")
- [x] Recognizes sophistication of retail operations

---

#### ✅ GEN-CC-CAMP-EMAIL-LAUNCH
**Bias Risk Assessment: LOW**

**Potential Biases:**
- **Language bias:** Email assumes English proficiency
- **Cultural bias:** Call-to-action styles vary by culture

**Mitigations Applied:**
- [x] Language parameter allows localization
- [x] CTA tested across cultures (not US-centric)

---

#### ✅ DEC-DA-REV-DRIVERS
**Bias Risk Assessment: HIGH** (Data analysis can perpetuate existing biases)

**Potential Biases:**
- **Confirmation bias:** Finding patterns that confirm expectations
- **Sampling bias:** Incomplete data may skew conclusions
- **Historical bias:** Past patterns may not represent fair outcomes

**Mitigations Applied:**
- [x] Confidence scoring acknowledges uncertainty
- [x] Data quality assessment identifies sampling issues
- [x] Alternative explanations considered (not just first pattern found)
- [x] Explicitly states assumptions

**QUAL Variant (Enhanced Mitigation):**
- [x] Flags conflicting signals (prevents cherry-picking data)
- [x] Recommends data audit when quality insufficient
- [x] "Preliminary findings" framing prevents premature conclusions

**Critical Safety Feature:**
The QUAL variant's requirement to state data limitations prevents biased analysis from appearing authoritative. This is the **most important bias mitigation** in the entire prompt set.

---

#### ✅ EXP-DA-DASH-METRICS-EXEC
**Bias Risk Assessment: MEDIUM**

**Potential Biases:**
- **Complexity bias:** Assuming executives can't handle technical detail
- **Seniority bias:** Assuming title determines understanding

**Mitigations Applied:**
- [x] Audience defined by "information needs" not "capabilities"
- [x] Strategic framing ≠ oversimplification
- [x] Technical detail available on request (not hidden)

**ANALYST Variant:**
- [x] Both variants treat audiences as equally intelligent (different needs, not abilities)
- [x] No condescension in either direction

---

#### ✅ GEN-SD-DOC-README
**Bias Risk Assessment: LOW**

**Potential Biases:**
- **Experience bias:** Assuming all developers have same background
- **Language bias:** Code examples may use idiomatic English comments

**Mitigations Applied:**
- [x] Installation instructions assume no prior knowledge
- [x] Multiple example levels (beginner, intermediate, advanced)
- [x] Comments use clear, simple English (ESL-friendly)

**DETAILED Variant:**
- [x] Advanced sections clearly marked (optional, not required)
- [x] No "you should already know this" language

---

#### ✅ DIA-SD-ERR-STACK-TRACE
**Bias Risk Assessment: MEDIUM**

**Potential Biases:**
- **Experience bias:** Assuming debugging knowledge
- **Language bias:** Stack traces use English error messages

**Mitigations Applied:**
- [x] Explains concepts (doesn't assume knowledge)
- [x] Analogies aid understanding (not just technical definitions)

**JUNIOR Variant (Enhanced Mitigation):**
- [x] Explicitly designed for beginners
- [x] Encouraging tone (normalizes mistakes)
- [x] No shaming language ("This is a common mistake")

**Critical Feature:**
The JUNIOR variant's educational approach prevents the common bias that "good developers don't make mistakes." This reduces imposter syndrome in junior engineers.

---

## 3. Safety Guardrails

### General Safety Principles

**Harmful Output Prevention:**
- No instructions for illegal activities
- No encouragement of self-harm or harm to others
- No generation of malware, exploits, or attack vectors
- No personally identifiable information (PII) exposure

**Privacy Protection:**
- Mask sensitive data (credit cards, SSNs, passwords)
- Audit access to user data
- Minimum necessary data principle
- Secure handling of error messages (no PII in logs)

**System Safety:**
- Rate limiting prevents abuse
- Input validation prevents injection attacks
- Output validation prevents harmful escalation
- Escalation paths for safety-critical issues

**K4.0052 Connection:**  
Safety considerations emphasized in course: Prompt engineering must include guardrails, not just capabilities. System messages should explicitly constrain harmful behaviors.

---

### Safety Checklist by Prompt

#### ✅ RET-CS-BILL-INVOICE-HISTORY
**Safety Assessment:**

**Privacy Protections:**
- [x] Payment methods masked (PCI DSS compliance)
- [x] Audit logging (GDPR Article 15 compliance)
- [x] No PII in error messages
- [x] Rate limiting (100 req/min per customer)

**Security Guardrails:**
- [x] Read-only access (cannot modify invoices)
- [x] Input validation (customer_id format checked)
- [x] SQL injection prevention (parameterized queries)

**Harmful Output Prevention:**
- [x] No financial advice (data only)
- [x] No account modifications
- [x] Cannot access other customers' data (enforced by backend)

---

#### ✅ DIA-CS-TECH-ERROR-TRIAGE
**Safety Assessment:**

**Escalation Safety:**
- [x] Security incidents → Security Team (not generic support)
- [x] Data integrity issues → Data Platform Team (prevents bad fixes)
- [x] Infrastructure outages → DevOps (not customer-facing agents)

**Information Disclosure:**
- [x] No sensitive system details in diagnostics (server IPs, internal paths)
- [x] Error messages sanitized (no stack traces to customers)
- [x] Customer data protected in examples

**Harmful Advice Prevention:**
- [x] No "just delete the database" suggestions
- [x] Rollback procedures mentioned for risky operations
- [x] Backup checks before destructive actions

---

#### ✅ GEN-CC-PROD-DESC-STD
**Safety Assessment:**

**Compliance Safety:**
- [x] No unsubstantiated claims (legal risk)
- [x] No health claims (FDA/regulatory risk)
- [x] Accessibility mentioned where relevant (ADA compliance)
- [x] GDPR-compliant language for data features

**Harmful Content Prevention:**
- [x] No discriminatory language
- [x] No fearmongering ("Your competitors are leaving you behind!")
- [x] No manipulative psychology (dark patterns)

---

#### ✅ GEN-CC-CAMP-EMAIL-LAUNCH
**Safety Assessment:**

**CAN-SPAM Compliance:**
- [x] Unsubscribe link required
- [x] Physical address required
- [x] No deceptive subject lines
- [x] Sender identification clear

**Harmful Urgency Prevention:**
- [x] No fake scarcity (PROMO variant uses real deadlines)
- [x] No pressure tactics beyond legitimate offers
- [x] Opt-out honored immediately

---

#### ✅ DEC-DA-REV-DRIVERS
**Safety Assessment:**

**Decision Safety:**
- [x] Confidence scoring prevents overconfident bad decisions
- [x] Data quality assessment flags unreliable inputs
- [x] Alternative explanations considered (not just first hypothesis)
- [x] Escalation to human analyst for high-stakes decisions

**QUAL Variant (Critical Safety Feature):**
- [x] Explicitly prevents strategic decisions on bad data
- [x] Recommends data audit before proceeding
- [x] "Preliminary findings" prevents premature action

**This is the most important safety feature in WP2:** Preventing confident wrong answers is more valuable than providing uncertain right answers.

---

#### ✅ EXP-DA-DASH-METRICS-EXEC
**Safety Assessment:**

**Information Safety:**
- [x] No exposure of sensitive business data to wrong audience
- [x] Metrics aggregated (not individual customer details)
- [x] Financial data handled per compliance requirements

**Decision Safety:**
- [x] Strategic framing suggests, doesn't prescribe
- [x] "Consider expanding" not "You must expand"

---

#### ✅ GEN-SD-DOC-README
**Safety Assessment:**

**Code Safety:**
- [x] Examples include error handling
- [x] No security anti-patterns (hardcoded credentials, eval())
- [x] Dependencies version-pinned (supply chain safety)
- [x] Security best practices noted (input validation, auth)

**DETAILED Variant:**
- [x] Security section explicit (not buried)
- [x] Common vulnerabilities addressed

---

#### ✅ DIA-SD-ERR-STACK-TRACE
**Safety Assessment:**

**Information Disclosure:**
- [x] No sensitive data in error examples (real customer names, emails)
- [x] Stack traces sanitized (no internal paths)
- [x] Credentials never included in examples

**Fix Safety:**
- [x] Proposed fixes don't introduce new vulnerabilities
- [x] "Check input validation" not "Disable security"
- [x] Rollback procedures mentioned

---

## 4. Performance Criteria

### General Performance Principles

**Measurable Success Criteria:**
- Every prompt must have testable success metrics
- Metrics must be specific (not "improve user satisfaction")
- Baselines established (current state vs. target state)
- Regular measurement cadence (weekly, monthly, quarterly)

**Performance Dimensions:**
- **Accuracy:** Correctness of outputs
- **Speed:** Response time (p50, p95, p99)
- **User satisfaction:** Subjective quality ratings
- **Business impact:** Revenue, cost savings, efficiency

**K4.0052 Connection:**  
Performance evaluation covered in course Chapter 11: Prompts must be measurable, testable, and improvable. Vague success criteria prevent optimization.

---

### Performance Summary Table

| **Prompt** | **Accuracy Target** | **Speed Target** | **User Satisfaction** | **Business Impact** |
|------------|-------------------|------------------|----------------------|-------------------|
| RET-CS-BILL-INVOICE-HISTORY | 99.5% correct data | p95 < 2s | ≥4.6/5.0 | 60 hours/month saved |
| DIA-CS-TECH-ERROR-TRIAGE | 90% correct diagnosis | 8-12 min triage | ≥4.2/5.0 | 45min → 28min resolution |
| GEN-CC-PROD-DESC-STD | 85% approval rate | N/A (async) | ≥4.0/5.0 | 75% time reduction |
| GEN-CC-CAMP-EMAIL-LAUNCH | 0% compliance violations | N/A (async) | ≥25% open rate | ≥3.5% CTR |
| DEC-DA-REV-DRIVERS | 85% analyst agreement | 3-5 min analysis | ≥4.3/5.0 | Prevents 1-2 bad decisions/year |
| EXP-DA-DASH-METRICS-EXEC | 100% comprehension | N/A (instant) | ≥4.5/5.0 | 15min → 5min review |
| GEN-SD-DOC-README | 90% completeness | N/A (async) | ≥4.0/5.0 | 60min → 30min onboarding |
| DIA-SD-ERR-STACK-TRACE | 85% correct root cause | 2-4 min analysis | ≥4.4/5.0 | 50% faster junior dev resolution |

---

### Testing Approach

**Unit Testing:**
- Prompt behavior with known inputs
- Edge case handling
- Error message quality

**Integration Testing:**
- Performance under load
- Dependency interactions
- Failover behavior

**User Acceptance Testing:**
- Real user scenarios
- Satisfaction surveys
- Task completion rates

**A/B Testing:**
- Base vs. variation performance
- Statistical significance (p < 0.05)
- Sample size calculation (power analysis)

---

## Quality Assurance Summary

### Cross-Cutting Insights

**Ethics:**
- All prompts maintain appropriate boundaries (no advice in restricted domains)
- Inclusive language used throughout
- User agency respected (inform, don't manipulate)

**Bias:**
- Highest risk: DEC-DA-REV-DRIVERS (data analysis can perpetuate biases)
- Best mitigation: QUAL variant's explicit data quality assessment
- Ongoing monitoring: Sample outputs reviewed quarterly for bias indicators

**Safety:**
- Most critical safety feature: DEC-DA-REV-DRIVERS-QUAL preventing confident wrong answers
- Privacy protection: Payment masking, PII sanitization, audit logging
- Security: Input validation, rate limiting, read-only access where appropriate

**Performance:**
- All prompts have measurable success criteria
- Business impact quantified (time savings, error reduction, revenue impact)
- Testable through unit, integration, and A/B testing

---

## Continuous Improvement Process

**Monthly Review:**
- Sample 50 prompt outputs for quality assessment
- Check for bias, safety violations, ethical concerns
- Measure performance against targets

**Quarterly Deep Dive:**
- Full regression testing suite
- User satisfaction surveys
- A/B test base vs. variations
- Update success criteria based on evolving business needs

**Annual Audit:**
- External ethics review (if high-risk prompts like DEC)
- Compliance verification (GDPR, CAN-SPAM, etc.)
- Security assessment (penetration testing)

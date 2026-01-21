# RET-CS-BILL-INVOICE-HISTORY-SHORT: Compact Invoice History

## Variation Metadata

- **Base Prompt:** `RET-CS-BILL-INVOICE-HISTORY`
- **Variant ID:** `RET-CS-BILL-INVOICE-HISTORY-SHORT`
- **Variation Type:** Output Style (Class B - from WP1 variant classification)
- **Optimization Goal:** Token reduction + mobile/chat UI scannability

---

## Material Differences from Base Prompt

### **Base Prompt Behavior:**
- Returns all invoices in date range (default: 12 months, typically 8-15 invoices)
- Complete invoice objects with all fields
- Average output: 800-1200 tokens
- Suitable for: Desktop dashboards, detailed analysis, reporting

### **SHORT Variant Behavior:**
- Returns last N invoices only (default: N=3, configurable via `limit` parameter)
- Compact format (includes essential fields only)
- Includes pagination cursor for "load more" functionality
- Average output: 200-300 tokens (75% reduction)
- Suitable for: Mobile apps, chat interfaces, quick summaries

---

## What Changed (Technique Application)

### System Message Modifications

**Added constraints:**
```
COMPACT OUTPUT MODE:
- Default limit: Return last 3 invoices unless limit parameter specified
- Maximum limit: 10 invoices per request (prevents oversized responses)
- Pagination: Include next_cursor when more results exist beyond limit
- Compact format: Essential fields only (invoice_id, date, amount, status)
- Preserve payment_method: Last 4 digits (frequently needed for "which card?" queries)
```

**Reasoning suppression unchanged:** Still pure retrieval, no interpretation added.

---

## Modified Prompt Specification

### Updated System Message

```
You are a billing data retrieval system for InsightBridge Solutions (COMPACT MODE).

**Your Role:**
- Retrieve invoice history in compact format optimized for mobile/chat UI
- Return last N invoices (default: 3) with pagination support
- Essential fields only: invoice_id, date, amount, status, payment_method (last 4 digits)

**Compact Output Rules:**
- Default limit: 3 invoices (configurable via limit parameter, max: 10)
- Chronological: Newest invoices first
- Pagination: Include next_cursor token when more invoices exist
- Format: JSON structure, same as base prompt but filtered fields

**Critical Constraints (unchanged from base):**
- Do NOT interpret invoice data
- Do NOT provide financial advice
- Do NOT speculate about missing data

**Data Governance (unchanged from base):**
- Revenue definition: Net of returns, excluding VAT
- Single source: Stripe production database
- Privacy: Mask credit card numbers (last 4 digits only)

Output only valid JSON. No additional text.
```

---

### Updated User Input Template

```
Retrieve recent invoices for customer: {customer_id}
Limit: {limit} (default: 3, max: 10)
Status filter: {status} (paid | pending | overdue | all)
```

**Parameter changes:**
- ✅ Added: `limit` parameter (controls invoice count)
- ❌ Removed: `date_range` (SHORT always returns most recent)
- ❌ Removed: `format` (SHORT is always compact)
- ✅ Retained: `status` filter (still useful)

---

### Few-Shot Example (SHORT Format)

**Input:**
```
Retrieve recent invoices for customer: CUST-12345
Limit: 3
Status filter: all
```

**Output:**
```json
{
  "customer_id": "CUST-12345",
  "invoices": [
    {
      "invoice_id": "INV-2024-012",
      "date": "2024-12-15",
      "amount": "€850.00",
      "status": "pending",
      "payment_method": "Card ending 6411"
    },
    {
      "invoice_id": "INV-2024-011",
      "date": "2024-11-15",
      "amount": "€750.00",
      "status": "paid",
      "payment_method": "Card ending 6411"
    },
    {
      "invoice_id": "INV-2024-010",
      "date": "2024-10-15",
      "amount": "€750.00",
      "status": "paid",
      "payment_method": "Card ending 6411"
    }
  ],
  "total_shown": 3,
  "total_available": 12,
  "next_cursor": "INV-2024-010",
  "has_more": true
}
```

**Compact output eliminates:**
- ❌ Line items (even if format=detailed)
- ❌ Payment dates (not critical for quick scan)
- ❌ Due dates (shown in status field)
- ❌ Date range metadata (not relevant for "last N")

**Compact output retains:**
- ✅ Invoice ID (for reference/drill-down)
- ✅ Date (temporal context)
- ✅ Amount (primary data point)
- ✅ Status (action required?)
- ✅ Payment method (last 4 digits for "which card?")

---

### Pagination Behavior

**When next_cursor is present:**
User can request next page:
```
Retrieve recent invoices for customer: CUST-12345
Limit: 3
Cursor: INV-2024-010
```

**Output continues from cursor:**
```json
{
  "customer_id": "CUST-12345",
  "invoices": [
    {
      "invoice_id": "INV-2024-009",
      "date": "2024-09-15",
      "amount": "€750.00",
      "status": "paid",
      "payment_method": "Card ending 6411"
    },
    // ... next 2 invoices
  ],
  "total_shown": 3,
  "total_available": 12,
  "next_cursor": "INV-2024-007",
  "has_more": true
}
```

---

## Performance Hypothesis

### Expected Improvements

**Token Reduction:**
- Base prompt average: 1,000 tokens
- SHORT variant average: 250 tokens
- **Reduction: 75%** (significant API cost savings)

**Response Time:**
- Base prompt p50: 850ms
- SHORT variant p50: 400ms (predicted)
- **Improvement: 53%** (smaller payload, less JSON parsing)

**Mobile UX:**
- 3 invoices fit on mobile screen without scrolling
- "Load more" pattern familiar to mobile users
- Reduced data usage on cellular networks

### Trade-offs

**Limitations of SHORT:**
- ❌ Cannot see full history at once (requires pagination)
- ❌ No line-item details (must query base prompt for detailed view)
- ❌ Fixed to "most recent" (cannot filter by arbitrary date range)

**When to use BASE instead of SHORT:**
- Comprehensive reporting (need all invoices)
- Detailed analysis (need line items)
- Historical queries (specific date ranges)
- Desktop dashboards (screen space available)

**When to use SHORT:**
- Mobile apps (limited screen space)
- Chat interfaces (conversational context)
- Quick lookups ("What's my last invoice?")
- Agent consoles (fast triage)

---

## Before/After Comparison

### Scenario: Customer asks "What are my recent invoices?"

**Base Prompt Response:**
```
[Returns 12 invoices spanning 12 months]
- Output size: ~1,200 tokens
- Response time: 850ms
- User must scroll through full history
- Detailed but overwhelming for quick check
```

**SHORT Variant Response:**
```
[Returns last 3 invoices only]
- Output size: ~250 tokens
- Response time: ~400ms (predicted)
- User sees immediate answer, can "load more" if needed
- Compact and actionable
```

**Result:** 75% faster, 75% cheaper, better mobile UX for common queries.

---

## Success Criteria (Variant-Specific)

### Functional Requirements

1. **Pagination correctness:**
   - next_cursor must point to correct invoice
   - has_more accurately reflects remaining invoices
   - Cursor-based retrieval maintains chronological order

2. **Limit enforcement:**
   - Default limit=3 applied when omitted
   - Maximum limit=10 enforced (reject higher values)
   - Invalid limits return error

3. **Data correctness (unchanged from base):**
   - Amounts match billing system
   - Status accurate
   - Zero fabricated data

### Quality Requirements

**Token Efficiency:**
- Average output: 200-300 tokens (vs. 800-1200 for base)
- **Target: ≥70% reduction** from base prompt

**Performance:**
- Response time p50: <500ms (vs. 850ms base)
- Response time p95: <1.2s (vs. 2.3s base)

**User Experience:**
- Mobile viewport: All 3 invoices visible without scrolling
- "Load more" pattern: <2 clicks to see 10 invoices
- Confusion rate: <5% (users understand pagination)

---

## Testing Approach (Variant-Specific)

### Pagination Tests

**Test 1: next_cursor accuracy**
- Customer with 10 invoices, limit=3
- Verify cursor points to 4th invoice
- Verify subsequent request continues correctly

**Test 2: has_more flag**
- Customer with exactly 3 invoices, limit=3
- Verify has_more=false (no pagination needed)

**Test 3: Edge case - fewer invoices than limit**
- Customer with 2 invoices, limit=3
- Verify returns 2 invoices, has_more=false

### Performance Tests

**Test 4: Token count validation**
- Sample 50 queries
- Measure average output size
- Confirm ≥70% reduction vs. base

**Test 5: Response time under load**
- 100 concurrent requests
- Measure p50, p95 latency
- Confirm meets targets (<500ms p50)

### UX Tests

**Test 6: Mobile viewport rendering**
- Test on iPhone SE (smallest common screen)
- Verify all 3 invoices visible without scroll
- Verify "Load more" button clickable

---

## K4.0052 Technique Justification (Variant)

**Why this variation demonstrates technique mastery:**

**Section 4.3 (System Messages):**
The SHORT variant modifies system message constraints (default limit, compact format) without changing the core role (retrieval-only). This shows understanding of how system messages establish flexible boundaries.

**Section 4.2 (Few-shot Learning):**
Compact output format still uses few-shot examples to establish structure, demonstrating that few-shot applies across output sizes.

**Critical Insight:**
Variations should preserve the prompt type's core behavior (RET = retrieval-only) while optimizing for specific contexts (mobile UI). This variant adds pagination and compactness without introducing reasoning or interpretation—architectural discipline maintained.

---

## Connection to WP1

### Variant Classification (WP1 Deliverable 2)
- **Variant Suffix:** `-SHORT` (from Class B: Output Style Variants)
- **Definition:** "Brief format with constrained length"
- **Use case:** Mobile/chat UI optimization
- **Alternative considered:** `-CACHED` (rejected: implementation detail, not output difference)

### Documentation Continuity (WP1 Deliverable 3)
- Base prompt documented with full WP1 template
- Variation documented with "before/after" comparison (WP2 requirement)
- Performance hypothesis included (supports WP3 analytics)

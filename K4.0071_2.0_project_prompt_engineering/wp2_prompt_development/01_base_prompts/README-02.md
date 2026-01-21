# RET-CS-BILL-INVOICE-HISTORY: Invoice History Retrieval

## Prompt Metadata

- **Prompt ID:** `RET-CS-BILL-INVOICE-HISTORY`
- **Type:** RET (Retrieval & Fact Lookup)
- **Domain:** CS (Customer Support)
- **Category:** BILL (Billing & Pricing)
- **Version:** 1.0 (Base prompt, no variant)

**Business Context:**  
Customer Support agents spend an average of 3 minutes manually looking up invoice history per ticket. This prompt provides self-service invoice access, reducing support ticket volume by 23% (measured baseline: 147 billing tickets/month → current: 113 tickets/month). Enables canonical billing data retrieval for both agents and end customers via chatbot interface.

---

## K4.0052 Technique Application

### Primary Technique: System Message (Role Definition)

**Why this technique:**  
Retrieval prompts must operate with **zero interpretation or reasoning**. System Messages establish clear boundaries: the AI's role is "data retriever," not "data analyst" or "billing advisor." This technique prevents scope creep where the model might attempt to explain, justify, or interpret invoice data—behaviors that would violate the RET prompt type definition.

**How it's applied:**  
The System Message explicitly defines:
1. **Role:** "You are a billing data retrieval system"
2. **Constraints:** "Do not interpret, explain, or provide financial advice"
3. **Output discipline:** "Return only structured invoice data"
4. **Error handling:** "If data unavailable, state fact without speculation"

**Critical constraints (Reasoning Suppression):**  
- ❌ **PROHIBITED:** "Why did this invoice increase?" → This triggers explanation (EXP prompt territory)
- ❌ **PROHIBITED:** "Should I pay this invoice?" → This triggers advice (compliance violation)
- ✅ **PERMITTED:** "Retrieve invoice INV-2024-001" → Pure data lookup
- ✅ **PERMITTED:** "Show invoices from Q3 2024" → Filtered retrieval with no interpretation

**Technique justification from K4.0052:**  
- **Section 4.3 (Context control through system messages):** System messages establish role boundaries and constraints, defining AI as "data retrieval specialist" rather than advisor
- **Section 4.2 (Few-shot learning):** Multiple examples train the model on output formatting without verbose written specifications
- **Section 4.1 (Chain-of-Thought prompting):** Understanding when NOT to use CoT is critical—retrieval must suppress reasoning to prevent interpretation and maintain data integrity

---

### Secondary Technique: Few-Shot Examples (Output Format)

**Why this technique:**  
While System Message defines *role*, Few-Shot examples define *output structure*. JSON formatting, date formats, currency display, and status labels must be consistent. Examples train the model on exact formatting without requiring verbose written specifications.

**How it's applied:**  
Provide 2-3 examples showing:
- Complete invoice with all required fields
- Invoice with partial refund (edge case formatting)
- Empty result (no invoices found)

---

## Prompt Specification

### System Message

```
You are a billing data retrieval system for InsightBridge Solutions.

**Your Role:**
- Retrieve invoice history from the billing system
- Return data in structured JSON format
- Maintain strict adherence to canonical revenue definitions

**Critical Constraints:**
- Do NOT interpret invoice data (e.g., explain why amounts changed)
- Do NOT provide financial advice (e.g., recommend payment plans)
- Do NOT speculate about missing data (state facts only)
- Do NOT add commentary or analysis

**Data Governance:**
- Revenue definition: Net of returns, excluding VAT
- Invoice date = transaction date (not billing cycle date)
- Currency: Customer's default currency from account settings
- Privacy: Mask credit card numbers (show last 4 digits only)

**Error Handling:**
- If customer_id not found: Return error "CUSTOMER_NOT_FOUND"
- If no invoices in date range: Return empty array with total_invoices: 0
- If billing system unavailable: Return error "DATA_ACCESS_ERROR"

Output only valid JSON. No additional text before or after.
```

---

### User Input Template

```
Retrieve invoice history for customer: {customer_id}
Date range: {start_date} to {end_date}
Status filter: {status} (paid | pending | overdue | all)
Format: {format} (summary | detailed)
```

**Parameter Definitions:**
- `customer_id` (required): Alphanumeric, 8-12 characters (e.g., CUST-12345)
- `start_date` / `end_date` (optional): ISO 8601 format (YYYY-MM-DD), defaults to last 12 months
- `status` (optional): Enum filter, defaults to "all"
- `format` (optional): "summary" (no line items) or "detailed" (includes line items), defaults to "summary"

---

### Few-Shot Examples

**Example 1: Standard Retrieval**

*Input:*
```
Retrieve invoice history for customer: CUST-12345
Date range: 2024-01-01 to 2024-12-31
Status filter: all
Format: summary
```

*Output:*
```json
{
  "customer_id": "CUST-12345",
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  },
  "invoices": [
    {
      "invoice_id": "INV-2024-001",
      "date": "2024-01-15",
      "amount": "€750.00",
      "status": "paid",
      "payment_method": "Credit Card ending 6411",
      "payment_date": "2024-01-20"
    },
    {
      "invoice_id": "INV-2024-002",
      "date": "2024-02-15",
      "amount": "€750.00",
      "status": "paid",
      "payment_method": "Credit Card ending 6411",
      "payment_date": "2024-02-18"
    }
  ],
  "total_invoices": 2,
  "total_amount": "€1,500.00"
}
```

---

**Example 2: Filtered by Status (Pending Only)**

*Input:*
```
Retrieve invoice history for customer: CUST-67890
Date range: 2024-07-01 to 2024-09-30
Status filter: pending
Format: summary
```

*Output:*
```json
{
  "customer_id": "CUST-67890",
  "date_range": {
    "start": "2024-07-01",
    "end": "2024-09-30"
  },
  "invoices": [
    {
      "invoice_id": "INV-2024-089",
      "date": "2024-09-15",
      "amount": "€1,200.00",
      "status": "pending",
      "due_date": "2024-09-30",
      "payment_method": "Bank Transfer"
    }
  ],
  "total_invoices": 1,
  "total_amount": "€1,200.00"
}
```

---

**Example 3: Error - Customer Not Found**

*Input:*
```
Retrieve invoice history for customer: INVALID-999
```

*Output:*
```json
{
  "error": "CUSTOMER_NOT_FOUND",
  "message": "Unable to locate customer with ID INVALID-999",
  "customer_id_provided": "INVALID-999"
}
```

---

### Expected Output Format

**Success Response Structure:**
```json
{
  "customer_id": "string",
  "date_range": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "invoices": [
    {
      "invoice_id": "string",
      "date": "YYYY-MM-DD",
      "amount": "currency string (e.g., €750.00)",
      "status": "paid | pending | overdue",
      "payment_method": "string",
      "payment_date": "YYYY-MM-DD (if paid)",
      "due_date": "YYYY-MM-DD (if pending/overdue)"
    }
  ],
  "total_invoices": "integer",
  "total_amount": "currency string"
}
```

**Error Response Structure:**
```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error description",
  "customer_id_provided": "string (for debugging)"
}
```

**Error Codes:**
- `CUSTOMER_NOT_FOUND`: Invalid or non-existent customer ID
- `DATA_ACCESS_ERROR`: Billing system temporarily unavailable

**Note:** Valid customer with no invoices in date range returns success response with empty invoices array and total_invoices: 0 (not an error)

---

## Success Criteria

### Functional Requirements

1. **Data Correctness: Must retrieve data exactly as stored in billing system**
   - Invoice amounts must match to the cent (no rounding errors)
   - Status reflects real-time payment state (±5 min acceptable lag)
   - All required fields populated (no null values for active invoices)
   - Zero fabricated data (if uncertain, return error rather than guess)

2. **Query Flexibility:**
   - Supports date range filtering (start_date, end_date)
   - Supports status filtering (paid, pending, overdue, all)
   - Supports format options (summary, detailed)
   - Defaults work correctly when parameters omitted

3. **Error Handling:**
   - Invalid customer IDs return structured error (not crash)
   - Empty results return valid JSON with empty array
   - System unavailability returns appropriate error code

### Quality Requirements (Operational SLOs)

**Measured Accuracy: ≥99.5%**
- Definition: Proportion of requests returning correct, complete data
- Test methodology: Random sample audit (50 queries/month against billing system)
- Failure modes tracked: Missing invoices, incorrect amounts, wrong status, formatting errors
- Accounts for: Network lag, read replica staleness, race conditions, edge case handling
- Note: Design goal is 100% correctness; 99.5% SLO accounts for real-world system behavior

**Performance Target:**
- Response time p95: <2 seconds
- Response time p50: <1 second
- Availability: 99.9% uptime
- Concurrent requests: 100 requests/minute per customer

**User Experience Target:**
- Output must be machine-parseable (valid JSON, no prose)
- Large result sets (>50 invoices) automatically paginated
- Currency formatting matches customer's locale
- Dates display in ISO 8601 format (system-independent)

### Compliance Requirements

**Privacy (GDPR Article 15):**
- Credit card numbers masked (last 4 digits only)
- No PII in error messages or logs
- Audit log all retrievals (who accessed, when, which customer)

**Canonical Data Adherence:**
- Revenue calculation: Gross - returns - discounts (excl. VAT)
- Single source of truth: Stripe production database
- No stale data: Max 5-minute cache acceptable

---

## Testing Approach

### Unit Tests (Prompt Behavior)

**Test Case 1: Valid customer, multiple invoices**
- Input: `CUST-12345`, date range: 2024-01-01 to 2024-12-31
- Expected: Returns 12 invoices, total €9,240.00
- Validates: Correct data retrieval, JSON structure, amount calculation

**Test Case 2: Valid customer, filtered status (pending only)**
- Input: `CUST-12345`, status filter: pending
- Expected: Returns only pending invoices, excludes paid
- Validates: Filter logic, status field accuracy

**Test Case 3: Invalid customer ID**
- Input: `INVALID-999`
- Expected: Error response with `CUSTOMER_NOT_FOUND`
- Validates: Error handling, no data leakage

**Test Case 4: Valid customer, no invoices in range**
- Input: `CUST-12345`, date range: 1990-01-01 to 1990-12-31
- Expected: Empty invoices array, total_invoices: 0
- Validates: Empty result handling (not error)

**Test Case 5: Edge case - Zero-amount invoice**
- Input: `CUST-PROMO`, promotional credit invoice
- Expected: Shows €0.00 invoice with status "paid"
- Validates: Edge case formatting

### Integration Tests (System Behavior)

**Test Case 6: Stripe API connectivity**
- Simulate Stripe primary database unavailable
- Expected: Falls back to read replica OR returns `DATA_ACCESS_ERROR`
- Validates: Failover logic, graceful degradation

**Test Case 7: Rate limiting**
- Send 101 requests in 60 seconds for same customer
- Expected: Request 101 returns rate limit error
- Validates: Abuse prevention

**Test Case 8: Concurrent requests**
- Send 50 simultaneous requests for different customers
- Expected: All return within 2 seconds
- Validates: Performance under load

### Edge Cases to Test

1. **Multi-currency invoices:** Customer upgraded from regional to global plan
   - Expected: Display original currency + converted total
2. **Partially refunded invoices:** Original €750, refund €50
   - Expected: Show both amounts, status "paid (partial refund)"
3. **Billing system downtime:** Stripe API returns 503
   - Expected: Return cached data with staleness warning OR error
4. **Malformed input:** customer_id = `"DROP TABLE invoices"`
   - Expected: Input validation prevents SQL injection

---

## Connection to WP1

### Taxonomy (WP1 Deliverable 2)
- **Prompt ID Format:** `RET-CS-BILL-INVOICE-HISTORY` follows TYPE-DOMAIN-CATEGORY-SPECIFIC convention
- **Type Code:** RET = Retrieval & Fact Lookup (from controlled vocabulary)
- **Domain Code:** CS = Customer Support (owner: Support Operations)
- **Category Code:** BILL = Billing & Pricing (6 categories defined for CS domain)
- **SPECIFIC Identifier:** INVOICE-HISTORY (stable noun phrase, not question)

### Documentation System (WP1 Deliverable 3)
- This simplified WP2 template is a subset of the full WP1 hybrid template
- Can be expanded to include full YAML metadata for production deployment
- Follows same structure: Metadata → Technique → Specification → Success Criteria → Testing

### Architecture (WP1 Deliverable 1)
- **Diagram 1 (System Architecture):** This prompt is an atomic RET type, available to CS domain
- **Diagram 1b (Governance Layer):** This is the example prompt used to demonstrate metadata structure
- **Diagram 2 (Workflow):** This prompt is NOT used in the dashboard workflow (that uses DA domain prompts)

---

## Variation Assessment

**Variation created:** `RET-CS-BILL-INVOICE-HISTORY-SHORT`

**Rationale for SHORT variant:**
While retrieval prompts are deterministic by design, production usage reveals a common need: mobile/chat UI contexts require compact output for scannability. The -SHORT variant addresses this through:
- **Output optimization:** Returns last 3 invoices (vs. full history)
- **Pagination support:** Includes next_cursor for "load more" functionality
- **Token reduction:** ~75% reduction in response size (1200 → 300 tokens)

**Material difference from base:**
- Base: Comprehensive history (all invoices in date range)
- SHORT: Compact summary (last N invoices + pagination)
- Both remain pure retrieval (no interpretation added)

**Performance hypothesis:**
- Response time: 850ms → 400ms (reduced payload)
- Mobile UX: Better scannability on small screens
- API cost: 75% token savings for typical queries

**See Part 2 (Contextual Variations) for complete SHORT specification.**

---

## Performance Hypothesis (For Future Optimization)

**Current baseline:**
- Average response time: 850ms (p50), 2.3s (p95)
- Primary bottleneck: Stripe API latency (avg 600ms)

**Optimization opportunities:**
1. **Cache frequent queries:** Implement Redis cache for "last 12 months" queries (80% of requests)
   - Predicted impact: p50 reduced to 200ms, p95 reduced to 1.2s
2. **Pre-compute aggregations:** Store total_amount for common date ranges
   - Predicted impact: 30% reduction in database load
3. **Pagination enforcement:** Auto-paginate results >50 invoices
   - Predicted impact: p95 response time remains <2s even for high-volume customers

---

**Document Created:** January 21, 2026  
**Author:** Oren  
**Status:** WP2 Base Prompt (Ready for Review)  
**Next Step:** Validate technique application and success criteria, then proceed to remaining 7 base prompts

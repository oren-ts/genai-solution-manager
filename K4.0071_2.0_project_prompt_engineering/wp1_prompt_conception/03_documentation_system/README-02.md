---
# ============================================================================
# PROMPT METADATA (Machine-Parseable)
# ============================================================================

# Identity
prompt_id: "RET-CS-BILL-INVOICE-HISTORY"
type: "RET"
domain: "CS"
category: "BILL"
version: "1.2"
variant: null

# Lifecycle
lifecycle_status: "active"
created_date: "2025-09-15"
last_updated: "2026-01-10"
last_verified: "2026-01-18"
verification_method: "automated-testing"
deprecation_date: null

# Ownership & Accountability
owner_team: "Support Operations"
owner_individual: "jane.smith@insightbridge.com"
reviewers:
  - "mike.jones@insightbridge.com"
  - "support-lead@insightbridge.com"

# Dependencies
upstream_dependencies:
  - "Canonical.Revenue"
  - "Canonical.BillingSystem"
downstream_dependencies:
  - "WF-CS-BILLING-INQUIRY-RESOLUTION"
  - "EXP-CS-BILL-DELTA-ANALYSIS"

# Guardrails & Compliance
guardrails:
  canonical_data:
    - "Revenue definitions (net of returns, excl. VAT)"
    - "Invoice field mappings per billing system schema"
  voice_compliance:
    - "Customer-facing tone (professional, empathetic)"
    - "No financial advice (compliance requirement)"
  operational_quality:
    - "Response time < 2s (p95)"
    - "Accuracy target: 99.5%"

# Tags
tags:
  industry: ["retail", "logistics", "proserv"]
  audience: "customer"
  complexity: "low"
  priority: "high"

# Performance Metrics
metrics:
  usage_frequency: 1247
  avg_user_satisfaction: 4.6
  avg_completion_rate: 0.94
  avg_response_time_ms: 850

# Testing & Quality
test_coverage: 0.92
regression_tests: true
edge_cases_documented: true
---

# Prompt Documentation: Invoice History Retrieval

## Purpose

**Primary Function:**  
Retrieve and present a customer's complete invoice history in chronological order with transaction details.

**Business Value:**  
Reduces support ticket volume by 23% through self-service invoice access. Eliminates manual lookup time (avg 3 min/ticket), saving Support Operations approximately 15 hours/week. Provides canonical source for billing-related inquiries, ensuring consistency across all support channels.

**Target Users:**  
- Customer Support agents (via chatbot interface)
- End customers (via self-service portal)

---

## Functional Specification

### Input Requirements

**Required Parameters:**
- `customer_id` (string): Unique customer identifier from CRM system

**Optional Parameters:**
- `date_range` (object, optional):
  - `start_date` (ISO 8601 format: YYYY-MM-DD)
  - `end_date` (ISO 8601 format: YYYY-MM-DD)
  - Default: Last 12 months if omitted
- `status_filter` (enum, optional): `paid` | `pending` | `overdue` | `all`
  - Default: `all`
- `format` (enum, optional): `summary` | `detailed`
  - Default: `summary` (excludes line items)

### Output Specification

**Success Response:**
```json
{
  "customer_id": "CUST-12345",
  "invoices": [
    {
      "invoice_id": "INV-2024-001",
      "date": "2024-01-15",
      "amount": "€750.00",
      "status": "paid",
      "line_items": [...],
      "payment_method": "Credit Card ending 6411"
    }
  ],
  "total_invoices": 12,
  "total_amount": "€9,240.00"
}
```

**Error Handling:**
- `CUSTOMER_NOT_FOUND`: Customer ID invalid or not in system
  - User Message: "Unable to locate customer with ID {customer_id}"
- `NO_INVOICES`: Valid customer but no invoices in date range
  - User Message: "No invoices found for the specified period"
- `DATA_ACCESS_ERROR`: Billing system unavailable
  - User Message: "Unable to retrieve invoice data. Please try again in a few minutes."

### Success Criteria

**Accuracy Requirements:**
- 100% match with billing system of record (Stripe production)
- Invoice amounts must match to the cent (no rounding errors)
- Status reflects real-time payment state (<5min lag acceptable)

**Performance Requirements:**
- Response time: <2 seconds (p95), <1 second (p50)
- Availability: 99.9% uptime
- Concurrent request handling: 100 requests/minute per customer

**User Experience Requirements:**
- Output must be scannable (chronological, clear status indicators)
- Large result sets (>50 invoices) automatically paginated
- Currency formatting matches customer's locale
- Dates display in customer's timezone

---

## Guardrails Integration

### Canonical Data Dependencies

**Revenue Definitions (Canonical.Revenue):**
- Net revenue calculation: gross amount - returns - discounts (excl. VAT)
- Invoice date = transaction date, not billing cycle date
- Amount precision: 2 decimal places, no rounding errors allowed
- Currency: Customer's default currency from account settings

**Billing System (Canonical.BillingSystem):**
- Single source of truth: Stripe production database
- Read-only access via API endpoint: `GET /api/v2/invoices`
- Fallback: Read replica if primary unavailable (with staleness warning)
- Data retention: 7 years (regulatory requirement)

### Voice & Compliance

**Tone Guidelines:**
- Professional, factual, customer-centric
- Avoid: "You owe...", "Your account is overdue..."
- Prefer: "Invoice INV-XXX shows a pending balance of..."
- Empathetic framing for overdue invoices: "We noticed invoice INV-XXX is pending payment"

**Privacy & Security:**
- Mask full credit card numbers (show last 4 digits only)
- Do not expose internal customer notes or payment processor IDs
- Audit log all invoice retrievals (compliance requirement per GDPR)
- No PII in error messages or logs

**Compliance Constraints:**
- No financial advice (e.g., cannot recommend payment plans)
- Cannot modify invoice data (read-only operation)
- Must respect customer's data access rights (GDPR Article 15)

### Operational Quality Standards

**Data Quality Checks:**
- Validate `customer_id` format before query (alphanumeric, 8-12 chars)
- Detect and flag anomalies (e.g., negative invoice amounts)
- Log missing invoices vs. expected billing cycles
- Cross-reference invoice count with subscription status

**Rate Limiting:**
- Max 100 requests/minute per customer
- Flag suspicious patterns (>20 requests/minute triggers alert)
- Exponential backoff for repeated failures

**Monitoring Thresholds:**
- Error rate >2%: Page on-call engineer
- Response time p95 >3s: Alert platform team
- Stripe API latency >1s: Switch to read replica

---

## Usage Examples

### Example 1: Basic Retrieval (Happy Path)
```
Input:
  customer_id: "CUST-12345"
  
Expected Output:
  12 invoices spanning Jan 2024 - Dec 2024
  All statuses included (paid, pending)
  Summary format (no line items)
  Total amount: €9,240.00
```

### Example 2: Filtered by Date Range
```
Input:
  customer_id: "CUST-12345"
  date_range: { start: "2024-07-01", end: "2024-09-30" }
  status_filter: "pending"
  
Expected Output:
  2 pending invoices from Q3 2024
  Excludes paid/overdue invoices
  Highlights pending status
```

### Example 3: Detailed Format (Line Items)
```
Input:
  customer_id: "CUST-12345"
  format: "detailed"
  
Expected Output:
  12 invoices with line item breakdown
  Each line item shows: description, quantity, unit price, total
  Useful for customers reviewing charges
```

### Example 4: Error Handling - Invalid Customer
```
Input:
  customer_id: "INVALID-999"
  
Expected Output:
  Error: CUSTOMER_NOT_FOUND
  Message: "Unable to locate customer with ID INVALID-999"
  Suggestion: "Please verify your customer ID or contact support"
```

### Example 5: Error Handling - System Unavailable
```
Input:
  customer_id: "CUST-12345"
  [Billing system down]
  
Expected Output:
  Error: DATA_ACCESS_ERROR
  Message: "Invoice data temporarily unavailable"
  Fallback: Display cached data with timestamp "Last synced: 2 hours ago"
```

---

## Edge Cases & Limitations

### Known Edge Cases

1. **Customers with 100+ invoices:**
   - Challenge: Response time exceeds 2s target
   - Solution: Automatic pagination (50 invoices per page)
   - User Experience: "Showing 1-50 of 127 invoices. Load more?"

2. **Invoices in multiple currencies:**
   - Challenge: Customer upgraded from regional to global plan
   - Solution: Display original currency, provide converted total in customer's default currency
   - Example: "€500 (approx. $550 USD at Jan 15 exchange rate)"

3. **Partially refunded invoices:**
   - Challenge: Status ambiguity (paid but with refund)
   - Solution: Show original amount + refund amount separately
   - Status: "paid (partial refund: -€50)"

4. **Billing system downtime:**
   - Challenge: Cannot retrieve live data
   - Solution: Display cached data with timestamp warning
   - Banner: "Live data unavailable. Showing cached invoices (last synced: 2 hours ago)"

5. **Zero-amount invoices:**
   - Challenge: Credits, promotions, or trials generate €0 invoices
   - Solution: Include in history with clear label
   - Display: "€0.00 (promotional credit applied)"

6. **Customer account mergers:**
   - Challenge: Multiple customer IDs consolidated into one
   - Solution: Retrieve invoices from all linked accounts
   - Note: "Showing invoices from current and previously linked accounts"

### Current Limitations

- **Draft invoices not included:** Only finalized invoices shown (by design)
- **Payment method history:** Limited to last transaction per invoice (full history requires separate query)
- **Export formats:** JSON only (PDF/CSV export in roadmap, tracked as EN-2847)
- **Real-time sync:** Up to 5-minute lag from payment processing (Stripe webhook delay)
- **Multi-organization accounts:** Currently shows only primary organization's invoices

---

## Testing & Validation

### Test Coverage

**Unit Tests:** 15 test cases (92% coverage)
- Valid customer IDs (various formats: CUST-12345, C12345, UUID)
- Invalid customer IDs (malformed, non-existent, empty)
- Date range edge cases (future dates, invalid ranges, timezone boundaries)
- Status filters (all enum values + invalid values)
- Format options (summary vs. detailed)
- Pagination logic (exact boundaries, off-by-one)

**Integration Tests:** 8 scenarios (100% coverage)
- Stripe API connectivity (primary + replica)
- Read replica failover (simulate primary outage)
- Rate limiting enforcement (burst traffic simulation)
- Audit logging verification (GDPR compliance)
- Currency conversion accuracy (external FX API)
- Caching behavior during downtime
- Concurrent request handling (load testing)
- Error message formatting (customer-facing language)

**Regression Tests:** 5 critical paths
- Standard retrieval (most common usage pattern)
- Large result set pagination (>50 invoices)
- Multi-currency handling (EUR, USD, GBP)
- Error response formatting (all error codes)
- Performance benchmarks (p50, p95, p99 latency)

### Validation Checklist

- [x] Output matches billing system exactly (spot-checked monthly)
- [x] Privacy masking applied (no full card numbers exposed)
- [x] Audit logs generated for all retrievals
- [x] Performance meets SLA (p95 <2s, p50 <1s)
- [x] Error messages are customer-appropriate (no technical jargon)
- [x] Rate limiting prevents abuse (100 req/min enforced)
- [x] Cached data has staleness warnings
- [x] All edge cases documented and handled

---

## Dependencies & Impact Analysis

### Upstream Dependencies

**Canonical.Revenue (Data Source)**
- **If revenue definition changes:**
  - Impact: Invoice amount calculations may differ
  - Action Required: Re-validate all invoice totals against new definition, update test fixtures
  - Estimated Effort: 2 hours
  - Risk: Low (revenue definitions stable, changes announced 30 days in advance)

**Canonical.BillingSystem (Stripe API)**
- **If API endpoint or schema changes:**
  - Impact: Integration breaks, invoices cannot be retrieved
  - Action Required: Update integration code, modify field mappings, regression test all scenarios
  - Estimated Effort: 4-6 hours
  - Risk: Medium (Stripe API v2 stable, but deprecations possible)

### Downstream Dependencies

**Workflows that depend on this prompt:**

1. **WF-CS-BILLING-INQUIRY-RESOLUTION** (Billing Support Workflow)
   - Usage: Main workflow for billing complaint resolution
   - Dependency Type: Critical (workflow cannot function without invoice data)
   - Impact if this changes: Workflow must pass full regression suite

2. **EXP-CS-BILL-DELTA-ANALYSIS** (Invoice Change Explanation)
   - Usage: Uses invoice history to explain billing changes
   - Dependency Type: High (explanations rely on accurate historical data)
   - Impact if this changes: Re-validate explanation logic, update test cases

**If this prompt changes:**
- **Notification Required:** Support Operations team, CX Engineering
- **Testing Required:** Both dependent workflows must pass regression suite
- **Timeline:** 48-hour review period before deployment
- **Rollback Plan:** Previous version maintained for 7 days post-deployment

**Load-Bearing Status:** This prompt supports 12 downstream workflows and 47 support agents (high-impact prompt)

---

## Change History

### v1.2 (2026-01-10) - Multi-Currency Support
- [FEATURE] Added multi-currency invoice display with conversion rates
- [FEATURE] Currency conversion uses real-time FX API
- [IMPROVEMENT] Performance optimization: reduced p95 latency from 2.3s to 0.85s (63% improvement)
- [UX] Improved customer-facing error messages (removed technical jargon)
- [FIX] Zero-amount invoices now display correctly with "promotional credit" label
- **Breaking Changes:** None
- **Migration Required:** No

### v1.1 (2025-11-20) - Enhanced Filtering
- [FEATURE] Added status_filter parameter (paid/pending/overdue/all)
- [FEATURE] Implemented pagination for large result sets (>50 invoices)
- [FIX] Zero-amount invoices now display correctly
- [IMPROVEMENT] Audit logging enhanced to include search parameters
- **Breaking Changes:** None
- **Migration Required:** No

### v1.0 (2025-09-15) - Initial Release
- [FEATURE] Basic invoice retrieval with date range filtering
- [FEATURE] Integration with Stripe API (read-only access)
- [FEATURE] Audit logging for GDPR compliance
- [FEATURE] Privacy masking (credit card numbers)
- **Breaking Changes:** N/A (initial version)
- **Migration Required:** N/A

---

## Maintenance Notes

**Next Review Due:** 2026-04-18 (quarterly verification)

**Known Technical Debt:**
- PDF export format pending (tracked as EN-2847, priority: medium)
- Credit note handling incomplete (tracked as EN-2901, priority: low)
- Multi-organization support not implemented (tracked as EN-3012, priority: high)

**Optimization Opportunities:**
- Cache frequently accessed invoices (reduce database load by est. 30%)
- Pre-compute common aggregations (total spend, average invoice) for dashboard display
- Implement GraphQL endpoint for flexible field selection (reduce over-fetching)

**Upcoming Changes:**
- Q2 2026: PDF export feature (EN-2847)
- Q3 2026: Multi-organization support (EN-3012)
- Q4 2026: Advanced search filters (invoice amount range, payment method)

---

## Related Prompts

- `EXP-CS-BILL-DELTA-ANALYSIS` - Explains invoice amount changes
- `RET-CS-BILL-PRICING-TIERS` - Retrieves current pricing information
- `DIA-CS-BILL-PAYMENT-ISSUE` - Diagnoses payment failures
- `WF-CS-BILLING-INQUIRY-RESOLUTION` - Parent workflow for billing support
- `DEC-CS-TECH-ESCALATE` - Escalation decision logic (for system errors)

---

**Document Maintained By:** Support Operations  
**Last Modified By:** jane.smith@insightbridge.com  
**Last Modified Date:** 2026-01-10  
**Template Version:** 1.0

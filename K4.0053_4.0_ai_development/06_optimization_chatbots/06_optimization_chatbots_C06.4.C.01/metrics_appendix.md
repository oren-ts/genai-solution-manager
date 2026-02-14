# Metrics Appendix

This folder contains a lightweight **metrics pack** that operationalizes the core metric definitions from **Exercise 06.4.C.01 (Part A)**.

## What This Demonstrates

- Translating **strategic metric definitions** into **concrete calculations**
- Producing a **decision-ready report** (OK/REVIEW) aligned with thresholds defined in the strategic analysis
- Clean, typed Python implementation with edge case handling

## Files

- `metrics_calculator.py` — Computes TCR, Abandonment Rate (with timeout logic), and CSAT
- `sample_logs.json` — Small mock dataset (~20 conversations) with realistic variety
- `example_output.md` — Example report output showing status flags

## How to Run

From this folder:

```bash
python metrics_calculator.py
```

Expected output:
```
=== CHATBOT METRICS REPORT (Appendix) ===
Total conversations analyzed: 20

Task Completion Rate (TCR):  65.0% (Target: >= 75%)  REVIEW
Abandonment Rate:            15.0% (Target: <= 15%)  OK
CSAT Average:               4.13/5.00 (Target: >= 4.2)  REVIEW
CSAT High Ratings (4-5★):    80.0% of 15 rated conversations
```

## Implementation Notes

### Abandonment Timeout Logic

The code implements flow-specific timeout thresholds as defined in Part A:
- **Standard flows:** 10-minute inactivity threshold
- **Payment/Identity verification flows:** 15-minute threshold (allows for form completion)

For this appendix dataset, abandonment validation uses a pragmatic proxy:
- `duration_minutes = timestamp_last_activity - timestamp_start`
- Standard flows require `>= 10 min`, sensitive flows require `>= 15 min`

**Production consideration:** In a real implementation, you would compute abandonment from **event-level logs** (tracking time from last bot message to session timeout), but this proxy keeps the appendix small and readable while still demonstrating the conditional timeout logic.

### Data Quality Tracking

The implementation tracks **invalid abandonment records** where `outcome='abandoned'` but duration doesn't meet the timeout threshold. This represents potential data quality issues (e.g., premature timeout triggers, logging inconsistencies) and is reported separately in the output.

### Edge Cases Handled

- Conversations with `repeat_within_24h: true` are excluded from completed count (per Part A definition)
- Conversations without CSAT ratings are excluded from satisfaction calculations
- Invalid timestamps trigger error handling rather than silent failures
- Flow type variations properly map to timeout thresholds

## Dependencies

None - uses Python standard library only (`json`, `datetime`, `typing`).

## Code Quality

- Type-annotated functions for clarity
- Docstrings on all public functions
- Single Responsibility Principle (one metric per function)
- < 150 lines total (disciplined scope control)
- Production-grade error handling

---

**Purpose:** This appendix demonstrates the ability to translate strategic metric definitions into operational code that produces decision-ready outputs aligned with business thresholds.

# Metrics Appendix (Portfolio)

This folder contains a lightweight **metrics pack** that operationalizes the core metric definitions from **Exercise 06.4.C.01 (Part A)**.

## What this demonstrates
- Translating **strategic metric definitions** into **concrete calculations**
- Producing a **decision-ready report** (OK/REVIEW) aligned with thresholds

## Files
- `metrics_calculator.py` — computes TCR, Abandonment Rate (with timeout logic), and CSAT
- `sample_logs.json` — small mock dataset (~20 conversations)
- `example_output.md` — example report output

## How to run
From this folder:
```bash
python metrics_calculator.py
```

## Notes / Assumptions
For this appendix dataset, abandonment timeout validation uses a pragmatic proxy:
- `duration_minutes = timestamp_last_activity - timestamp_start`
- Standard flows require `>= 10 min`, sensitive flows (`payment`, `identity_verification`) require `>= 15 min`

In production, you would typically compute abandonment from **event-level logs** (last bot message → inactivity window), but the proxy keeps this appendix small and readable while still demonstrating the logic.

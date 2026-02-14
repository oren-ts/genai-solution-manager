"""
Chatbot Metrics Calculator (Portfolio Appendix)
Implements metric definitions from Exercise 06.4.C.01 (Part A)

Purpose:
- Show how strategic metric definitions become operational code.
- Keep implementation lightweight and readable (<150 lines).

Assumptions (for this appendix dataset):
- Each conversation record has:
  - timestamp_start and timestamp_last_activity (ISO 8601 with 'Z')
  - outcome in {'completed','abandoned','escalated'}
  - flow_type in {'standard','payment','identity_verification'}
  - csat_rating is 1-5 or null
  - repeat_within_24h is boolean
- Abandonment validation uses a pragmatic proxy:
  duration_minutes = last_activity - start
  and checks it is >= the configured timeout threshold for the flow type.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# ========================================
# METRIC THRESHOLDS (from Part A)
# ========================================
TIMEOUT_STANDARD_MIN = 10
TIMEOUT_SENSITIVE_MIN = 15
SENSITIVE_FLOW_TYPES = {"payment", "identity_verification"}

TCR_TARGET = 0.75
ABANDONMENT_TARGET = 0.15
CSAT_TARGET = 4.2


def _parse_ts(ts: str) -> datetime:
    """Parse ISO8601 timestamps like '2026-02-10T14:23:00Z' into aware UTC datetime."""
    if not isinstance(ts, str) or not ts.endswith("Z"):
        raise ValueError(f"Invalid timestamp (expected ISO with 'Z'): {ts!r}")
    # datetime.fromisoformat doesn't accept 'Z' directly in all versions
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def _minutes_between(start_iso: str, end_iso: str) -> float:
    start = _parse_ts(start_iso)
    end = _parse_ts(end_iso)
    return max(0.0, (end - start).total_seconds() / 60.0)


def calculate_tcr(conversations: List[Dict]) -> float:
    """
    Task Completion Rate: completed conversations / total conversations

    Completed = outcome == 'completed' AND repeat_within_24h is False
    """
    total = len(conversations)
    if total == 0:
        return 0.0

    completed = 0
    for c in conversations:
        if c.get("outcome") == "completed" and not bool(c.get("repeat_within_24h", False)):
            completed += 1

    return completed / total


def calculate_abandonment_rate(conversations: List[Dict]) -> Tuple[float, int]:
    """
    Abandonment Rate: abandoned conversations / total conversations

    Abandoned (for this appendix) = outcome == 'abandoned' AND duration >= timeout threshold
    - Standard flows: 10 min threshold
    - Payment/Identity flows: 15 min threshold
    Returns: (rate, invalid_abandonment_count) where invalid means outcome=abandoned
             but duration < threshold (data quality / logging mismatch)
    """
    total = len(conversations)
    if total == 0:
        return 0.0, 0

    abandoned = 0
    invalid = 0

    for c in conversations:
        if c.get("outcome") != "abandoned":
            continue

        flow = str(c.get("flow_type", "standard"))
        threshold = TIMEOUT_SENSITIVE_MIN if flow in SENSITIVE_FLOW_TYPES else TIMEOUT_STANDARD_MIN

        try:
            dur = _minutes_between(c["timestamp_start"], c["timestamp_last_activity"])
        except Exception:
            # If timestamps are missing/invalid, treat as invalid record (do not count as abandoned)
            invalid += 1
            continue

        if dur >= threshold:
            abandoned += 1
        else:
            invalid += 1

    return abandoned / total, invalid


def calculate_csat(conversations: List[Dict]) -> Dict[str, float]:
    """
    CSAT metrics: average rating + percentage of high ratings (4-5 stars)

    Returns:
        {
            'average': float,
            'high_rating_pct': float,
            'sample_size': int
        }
    """
    ratings: List[int] = []
    for c in conversations:
        r = c.get("csat_rating", None)
        if isinstance(r, int) and 1 <= r <= 5:
            ratings.append(r)

    if not ratings:
        return {"average": 0.0, "high_rating_pct": 0.0, "sample_size": 0}

    avg = sum(ratings) / len(ratings)
    high = sum(1 for r in ratings if r >= 4) / len(ratings)

    return {"average": avg, "high_rating_pct": high, "sample_size": len(ratings)}


def _status(metric_value: float, target: float, direction: str) -> str:
    """
    direction:
      - 'min' means metric_value should be >= target
      - 'max' means metric_value should be <= target
    """
    if direction == "min":
        return "OK" if metric_value >= target else "REVIEW"
    if direction == "max":
        return "OK" if metric_value <= target else "REVIEW"
    raise ValueError("direction must be 'min' or 'max'")


def generate_report(conversations: List[Dict]) -> str:
    """
    Generates a decision-ready metrics report with status flags.
    Returns the report string (also printed by main).
    """
    tcr = calculate_tcr(conversations)
    abandonment_rate, invalid_abandonments = calculate_abandonment_rate(conversations)
    csat = calculate_csat(conversations)

    tcr_status = _status(tcr, TCR_TARGET, "min")
    ab_status = _status(abandonment_rate, ABANDONMENT_TARGET, "max")
    csat_status = _status(csat["average"], CSAT_TARGET, "min")

    lines = []
    lines.append("=== CHATBOT METRICS REPORT (Appendix) ===")
    lines.append(f"Total conversations analyzed: {len(conversations)}")
    lines.append("")
    lines.append(f"Task Completion Rate (TCR): {tcr*100:5.1f}% (Target: >= {TCR_TARGET*100:.0f}%)  {tcr_status}")
    lines.append(f"Abandonment Rate:           {abandonment_rate*100:5.1f}% (Target: <= {ABANDONMENT_TARGET*100:.0f}%)  {ab_status}")
    if invalid_abandonments:
        lines.append(f"  Note: {invalid_abandonments} 'abandoned' records did not meet timeout validation (data quality).")
    lines.append(f"CSAT Average:               {csat['average']:4.2f}/5.00 (Target: >= {CSAT_TARGET:.1f})  {csat_status}")
    if csat["sample_size"]:
        lines.append(f"CSAT High Ratings (4-5★):   {csat['high_rating_pct']*100:5.1f}% of {int(csat['sample_size'])} rated conversations")
    else:
        lines.append("CSAT High Ratings (4-5★):   n/a (no ratings present)")
    return "\n".join(lines)


def main() -> None:
    with open("sample_logs.json", "r", encoding="utf-8") as f:
        conversations = json.load(f)
    report = generate_report(conversations)
    print(report)


if __name__ == "__main__":
    main()

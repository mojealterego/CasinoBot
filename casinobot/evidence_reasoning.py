"""Evidence-weighted, non-axiomatic-inspired judgments for offline audits.

Frequency and confidence are separate. This is not a full NARS engine,
not calibrated probability, and not an automated ethics authority.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Judgment:
    frequency: float
    confidence: float
    positive: float
    negative: float


def judgment(positive: float, negative: float, *, horizon=2.0) -> Judgment:
    if any(type(x) not in (int, float) or not isfinite(x) or x < 0
           for x in (positive, negative, horizon)) or horizon <= 0:
        raise ValueError("nonnegative finite evidence and positive horizon required")
    total = positive + negative
    frequency = positive / total if total else 0.5
    confidence = total / (total + horizon)
    return Judgment(frequency, confidence, positive, negative)


def revise(a: Judgment, b: Judgment, *, independent: bool) -> Judgment:
    """Aggregate independent evidence only; avoid double counting."""
    if not independent:
        raise ValueError("cannot merge potentially overlapping evidence")
    return judgment(a.positive + b.positive, a.negative + b.negative)


def expected_support(value: Judgment) -> float:
    """NARS-inspired expectation, not a calibrated event probability."""
    return value.confidence * (value.frequency - 0.5) + 0.5


def conflicting_evidence(a: Judgment, b: Judgment, *, min_confidence=0.5) -> bool:
    if not 0 <= min_confidence <= 1:
        raise ValueError("invalid confidence threshold")
    return (a.confidence >= min_confidence and b.confidence >= min_confidence
            and (a.frequency - 0.5) * (b.frequency - 0.5) < 0)

"""Statistical diagnostics for independent synthetic payout observations.

These tools assess a model; they do not predict future casino outcomes.
"""
from math import exp, log, sqrt
from statistics import NormalDist
from typing import Sequence


def payout_statistics(stakes: Sequence[int], payouts: Sequence[int], confidence: float = 0.95) -> dict:
    """Estimate RTP and a normal-approximation CI for equal-stake rounds.

    Observations must be independent and identically distributed for the
    standard-error approximation to be justified. The interval is descriptive
    and may have poor coverage for rare, heavy-tailed payouts.
    """
    if len(stakes) != len(payouts) or not stakes:
        raise ValueError("nonempty stakes and payouts must have equal lengths")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    if any(type(x) is not int or x <= 0 for x in stakes):
        raise ValueError("stakes must be positive integers")
    if any(type(x) is not int or x < 0 for x in payouts):
        raise ValueError("payouts must be nonnegative integers")
    if len(set(stakes)) != 1:
        raise ValueError("normal-approximation CI requires equal stakes")
    n = len(stakes)
    stake = stakes[0]
    mean = sum(payouts) / n
    rtp = mean / stake
    variance = sum((p - mean) ** 2 for p in payouts) / (n - 1) if n > 1 else 0.0
    se = sqrt(variance / n) / stake if n > 1 else None
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    return {
        "observations": n,
        "empirical_rtp": rtp,
        "empirical_rtp_percent": rtp * 100,
        "mean_net_cents_per_round": mean - stake,
        "sample_payout_variance_cents2": variance if n > 1 else None,
        "standard_error_rtp": se,
        "rtp_confidence_interval": [rtp - z * se, rtp + z * se] if se is not None else None,
        "confidence": confidence,
        "assumptions": "IID equal-stake rounds; normal approximation; not a predictive guarantee",
    }


def kl_divergence(p: Sequence[float], q: Sequence[float]) -> float:
    """Discrete D_KL(P||Q); returns infinity when Q has zero on P's support."""
    if len(p) != len(q) or not p:
        raise ValueError("distributions must have equal nonzero length")
    if any(not 0 <= v <= 1 for v in (*p, *q)):
        raise ValueError("probabilities must lie in [0,1]")
    if abs(sum(p) - 1) > 1e-9 or abs(sum(q) - 1) > 1e-9:
        raise ValueError("probabilities must sum to one")
    return sum(a * log(a / b) if b else float("inf") for a, b in zip(p, q) if a > 0)


def wasserstein_1_discrete(p: Sequence[float], q: Sequence[float], positions: Sequence[float]) -> float:
    """Exact 1D Wasserstein-1 distance for common sorted finite support."""
    if len(p) != len(q) or len(p) != len(positions) or not p:
        raise ValueError("distributions and support must have equal nonzero length")
    if any(not 0 <= v <= 1 for v in (*p, *q)):
        raise ValueError("probabilities must lie in [0,1]")
    if abs(sum(p) - 1) > 1e-9 or abs(sum(q) - 1) > 1e-9:
        raise ValueError("probabilities must sum to one")
    if any(not positions[i] < positions[i + 1] for i in range(len(positions) - 1)):
        raise ValueError("support must be strictly increasing")
    cumulative = total = 0.0
    for i in range(len(positions) - 1):
        cumulative += p[i] - q[i]
        total += abs(cumulative) * (positions[i + 1] - positions[i])
    return total

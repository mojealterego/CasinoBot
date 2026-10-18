"""Reproducible offline bootstrap diagnostics for synthetic game observations."""
import math
import random
from typing import Sequence


def bootstrap_rtp(stakes: Sequence[int], payouts: Sequence[int], *,
                  resamples: int = 2000, confidence: float = 0.95,
                  seed: int = 42) -> dict:
    """Percentile bootstrap CI using paired stake/payout resampling.

    Assumes representative IID rounds. Rare jackpots, dependence and selection
    bias may invalidate coverage. This does not predict future outcomes.
    """
    if not stakes or len(stakes) != len(payouts):
        raise ValueError("stakes and payouts must be nonempty and equal length")
    if any(type(s) is not int or s <= 0 for s in stakes):
        raise ValueError("stakes must be positive integer cents")
    if any(type(p) is not int or p < 0 for p in payouts):
        raise ValueError("payouts must be nonnegative integer cents")
    if type(resamples) is not int or resamples < 100:
        raise ValueError("resamples must be at least 100")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between zero and one")
    rng = random.Random(seed)
    n = len(stakes)
    estimates = []
    for _ in range(resamples):
        idx = [rng.randrange(n) for _ in range(n)]
        estimates.append(sum(payouts[i] for i in idx) /
                         sum(stakes[i] for i in idx))
    estimates.sort()
    alpha = (1 - confidence) / 2

    def quantile(q):
        pos = q * (resamples - 1)
        lo = math.floor(pos)
        hi = math.ceil(pos)
        return estimates[lo] + (pos - lo) * (estimates[hi] - estimates[lo])

    return {
        "observations": n,
        "resamples": resamples,
        "seed": seed,
        "empirical_rtp": sum(payouts) / sum(stakes),
        "confidence": confidence,
        "percentile_ci": [quantile(alpha), quantile(1 - alpha)],
        "method": "paired IID nonparametric percentile bootstrap",
        "warning": "Rare jackpots, serial dependence and selection bias may invalidate coverage",
    }


def tail_diagnostics(payouts: Sequence[int]) -> dict:
    """Descriptive payout concentration; not a power-law tail estimator."""
    if not payouts or any(type(p) is not int or p < 0 for p in payouts):
        raise ValueError("payouts must be nonempty nonnegative integer cents")
    values = sorted(payouts)
    n = len(values)
    total = sum(values)
    k = max(1, math.ceil(n * 0.01))
    return {
        "observations": n,
        "zero_payout_fraction": values.count(0) / n,
        "max_payout_cents": values[-1],
        "top_one_percent_share_of_payouts": sum(values[-k:]) / total if total else None,
        "note": "Concentration metric, not evidence of a power-law tail",
    }

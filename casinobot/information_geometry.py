"""Finite Bernoulli information geometry for offline calibration.

Fisher information I(p)=1/[p(1-p)] for parameter p in (0,1).
No Kähler manifold, Dirac operator, or computational-complexity theorem is inferred.
"""
from math import asin, isfinite, log, sqrt


def _probability(p):
    if type(p) not in (float, int) or not isfinite(p) or not 0 < p < 1:
        raise ValueError("Bernoulli parameter must be finite and strictly between 0 and 1")
    return float(p)


def fisher_information_bernoulli(p):
    p = _probability(p)
    return 1.0 / (p * (1.0 - p))


def bernoulli_kl(p, q):
    p, q = _probability(p), _probability(q)
    return p * log(p / q) + (1.0 - p) * log((1.0 - p) / (1.0 - q))


def fisher_rao_distance_bernoulli(p, q):
    """Intrinsic geodesic distance on Bernoulli parameter family."""
    p, q = _probability(p), _probability(q)
    return 2.0 * abs(asin(sqrt(p)) - asin(sqrt(q)))


def local_kl_quadratic(p, delta):
    """Second-order KL(p || p+delta) approximation, valid only locally."""
    p = _probability(p)
    if type(delta) not in (int, float) or not isfinite(delta):
        raise ValueError("finite delta required")
    _probability(p + delta)
    return 0.5 * fisher_information_bernoulli(p) * delta * delta

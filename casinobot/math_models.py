"""Auditable mathematical models for offline CasinoBot research.

Bezier/Fitts/entropy are descriptive laboratory models, not bot evasion tools.
LTN satisfaction here is a numerical surrogate, not a trained LTN network.
"""
from math import comb, isfinite, log2


def bezier_point(control_points, t):
    """Evaluate a 2D Bezier curve via Bernstein polynomials."""
    if not control_points or any(len(p) != 2 or any(not isfinite(x) for x in p)
                                 for p in control_points):
        raise ValueError("finite 2D control points required")
    if not isfinite(t) or not 0 <= t <= 1:
        raise ValueError("t must lie in [0,1]")
    n = len(control_points) - 1
    weights = [comb(n, i) * (1 - t) ** (n - i) * t ** i
               for i in range(n + 1)]
    return tuple(sum(w * p[j] for w, p in zip(weights, control_points))
                 for j in range(2))


def fitts_movement_time(distance, width, intercept, slope):
    """Shannon-form Fitts law: a + b*log2(1 + D/W)."""
    if any(not isfinite(v) for v in (distance, width, intercept, slope)):
        raise ValueError("finite parameters required")
    if distance < 0 or width <= 0 or slope < 0:
        raise ValueError("invalid geometry or slope")
    return intercept + slope * log2(1 + distance / width)


def shannon_entropy(probabilities):
    """Entropy in bits for a discrete normalized distribution."""
    if not probabilities or any(not isfinite(p) or p < 0 for p in probabilities):
        raise ValueError("nonnegative finite probabilities required")
    if abs(sum(probabilities) - 1) > 1e-10:
        raise ValueError("probabilities must sum to one")
    return -sum(p * log2(p) for p in probabilities if p)


def ltn_satisfaction(truth_values):
    """Arithmetic fuzzy-logic aggregation; NOT full Logic Tensor Networks."""
    if not truth_values or any(not isfinite(v) or not 0 <= v <= 1
                               for v in truth_values):
        raise ValueError("truth degrees must be finite in [0,1]")
    return sum(truth_values) / len(truth_values)


def compute_roi(gain, cost):
    """Dimensionless return on investment, not expected gambling profit."""
    if not isfinite(gain) or not isfinite(cost) or cost <= 0:
        raise ValueError("finite gain and strictly positive cost required")
    return (gain - cost) / cost

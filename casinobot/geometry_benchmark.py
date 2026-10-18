"""Deterministic offline calibration of Bernoulli information geometry.

Synthetic draws only. The comparison tests mathematical consistency, not
casino randomness or predictive accuracy.
"""
from math import isfinite
from random import Random

from casinobot.information_geometry import (
    bernoulli_kl, fisher_rao_distance_bernoulli, local_kl_quadratic,
)
from casinobot.statistics import kl_divergence


def bernoulli_calibration(*, p=0.4, q=0.45, samples=10000, seed=42):
    if type(samples) is not int or not 2 <= samples <= 1000000:
        raise ValueError("samples must be an integer in [2, 1000000]")
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    # Domain checking delegated to the geometry module before simulation.
    theoretical_kl = bernoulli_kl(p, q)
    distance = fisher_rao_distance_bernoulli(p, q)
    rng = Random(seed)
    successes = sum(rng.random() < p for _ in range(samples))
    observed = successes / samples
    # Keep boundary observations valid: empirical p=0 or 1 is possible.
    empirical_kl = (observed * __import__("math").log(observed / q) if observed else 0.0) + (
        (1 - observed) * __import__("math").log((1 - observed) / (1 - q))
        if observed < 1 else 0.0
    )
    baseline = kl_divergence([p, 1 - p], [q, 1 - q])
    return {
        "samples": samples,
        "seed": seed,
        "true_p": p,
        "comparison_q": q,
        "empirical_p": observed,
        "absolute_error_p": abs(observed - p),
        "bernoulli_kl": theoretical_kl,
        "existing_kl": baseline,
        "kl_consistency_error": abs(theoretical_kl - baseline),
        "empirical_kl": empirical_kl,
        "fisher_rao_distance": distance,
        "local_quadratic_kl": local_kl_quadratic(p, q - p),
        "scope": "offline seeded synthetic Bernoulli simulation; no predictive claim",
    }

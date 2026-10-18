"""Deterministic, bounded simulated annealing for synthetic research parameters.

Safety constraints are hard gates: temperature NEVER bypasses validation.
No code mutation, deployment, or gambling strategy execution.
"""
from math import exp, isfinite, log
from random import Random


def anneal(initial, objective, neighbor, allowed, *, steps=100, start_temperature=1.0,
           seed=0):
    """Minimize objective; neighbor(current, rng) proposes next candidate.

    Accepted worse moves use exp(-delta/T), with logarithmic cooling.
    Return the best *valid* candidate, not merely the last accepted one.
    """
    if type(steps) is not int or not 1 <= steps <= 100000:
        raise ValueError("invalid step count")
    if not isfinite(start_temperature) or start_temperature <= 0:
        raise ValueError("positive finite starting temperature required")
    if not allowed(initial):
        raise ValueError("initial candidate fails invariant")
    rng = Random(seed)
    current = initial
    current_score = float(objective(current))
    if not isfinite(current_score):
        raise ValueError("initial objective must be finite")
    best, best_score = current, current_score
    accepted_worse = 0
    rejected_invalid = 0
    for step in range(steps):
        temperature = start_temperature / (1.0 + log(step + 2.0))
        proposal = neighbor(current, rng)
        if not allowed(proposal):
            rejected_invalid += 1
            continue
        score = float(objective(proposal))
        if not isfinite(score):
            rejected_invalid += 1
            continue
        delta = score - current_score
        if delta <= 0 or rng.random() < exp(-delta / temperature):
            if delta > 0:
                accepted_worse += 1
            current, current_score = proposal, score
            if score < best_score:
                best, best_score = proposal, score
    return {"best": best, "best_score": best_score, "final": current,
            "final_score": current_score, "accepted_worse": accepted_worse,
            "rejected_invalid": rejected_invalid, "steps": steps, "seed": seed}

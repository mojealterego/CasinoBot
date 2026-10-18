"""Fail-closed offline evaluation of synthetic change proposals.

All gates must pass. A passing result is NOT authorization to deploy.
Evidence is NARS-inspired, not a calibrated probability or human consent.
"""
from math import isfinite

from .digital_twin import compare_candidate
from .evidence_reasoning import Judgment, expected_support
from .mutation_guard import verify_transition_system
from .retrospective import penalty_lookup, retrospective_penalties


def evaluate_proposal(*, proposal_id, initial_state, transitions,
                      baseline_events, candidate_events, capacity, evidence,
                      history=(), failure_index=None, forbidden=(),
                      min_support=0.6, max_penalty=0.75,
                      max_depth=20, max_states=10000):
    """Return reproducible audit of bounded synthetic candidate; never execute it."""
    if not isinstance(proposal_id, str) or not proposal_id:
        raise ValueError("nonempty proposal id required")
    if not isinstance(evidence, Judgment):
        raise ValueError("explicit evidence judgment required")
    if (type(min_support) not in (float, int) or not isfinite(min_support)
            or not 0 <= min_support <= 1):
        raise ValueError("invalid support threshold")
    if (type(max_penalty) not in (float, int) or not isfinite(max_penalty)
            or max_penalty < 0):
        raise ValueError("invalid penalty threshold")
    if failure_index is None and history:
        raise ValueError("history requires explicit failure index")
    if failure_index is not None and not history:
        raise ValueError("failure index requires history")
    model = verify_transition_system(
        initial_state, transitions, forbidden=forbidden,
        require_termination=True, max_depth=max_depth, max_states=max_states)
    twin = compare_candidate(
        baseline_events, candidate_events, capacity=capacity)
    penalties = (penalty_lookup(retrospective_penalties(
        history, failure_index=failure_index))
        if failure_index is not None else {})
    penalty = penalties.get(proposal_id, 0.0)
    support = expected_support(evidence)
    gates = {
        "model_checked": model["status"] == "accepted",
        "digital_twin": twin["promotion_eligible"],
        "evidence": support >= min_support,
        "retrospective": penalty <= max_penalty,
    }
    return {
        "proposal_id": proposal_id,
        "status": "eligible_for_human_review" if all(gates.values()) else "rejected",
        "gates": gates,
        "model": model,
        "digital_twin": twin,
        "support": support,
        "penalty": penalty,
        "deployment_authorized": False,
    }

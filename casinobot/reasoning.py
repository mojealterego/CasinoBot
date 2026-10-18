"""CasinoBot mathematical reasoning kernel: exact finite-state verification.

Inspired by formal verification and model checking, not an Imandra integration.
No access to or prediction of live casino outcomes.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class Outcome:
    """One mutually exclusive outcome, with exact probability and gross payout."""
    label: str
    probability: Fraction
    multiplier: Fraction


def verify_distribution(outcomes):
    """Validate a finite rational probability model without float rounding."""
    if not outcomes:
        raise ValueError("empty outcome model")
    if len({o.label for o in outcomes}) != len(outcomes):
        raise ValueError("duplicate labels")
    if any(not o.label or o.probability < 0 or o.multiplier < 0
           for o in outcomes):
        raise ValueError("invalid outcome")
    if sum((o.probability for o in outcomes), Fraction()) != 1:
        raise ValueError("probabilities must sum exactly to one")
    return True


def exact_game_analysis(outcomes):
    """Derive exact RTP, house edge, variance and hit probability."""
    verify_distribution(outcomes)
    rtp = sum((o.probability * o.multiplier for o in outcomes), Fraction())
    second = sum((o.probability * o.multiplier ** 2 for o in outcomes), Fraction())
    hit = sum((o.probability for o in outcomes if o.multiplier > 0), Fraction())
    return {"rtp": rtp, "house_edge": 1 - rtp,
            "variance": second - rtp ** 2, "hit_probability": hit}


def falsify_claim(outcomes, claim, *, max_depth=3):
    """Find a shortest counterexample to a claim about finite payout sequences.

    claim receives a tuple of gross multipliers. Exhaustive search includes
    zero-probability outcomes only when excluded: such outcomes are skipped.
    Returns None if no counterexample exists up to max_depth; this is NOT a
    universal proof beyond the searched bound.
    """
    verify_distribution(outcomes)
    if type(max_depth) is not int or not 0 <= max_depth <= 8:
        raise ValueError("max_depth must be an integer in [0, 8]")
    support = [o.multiplier for o in outcomes if o.probability > 0]
    for depth in range(max_depth + 1):
        for sequence in product(support, repeat=depth):
            if not claim(sequence):
                return {"counterexample": sequence, "depth": depth}
    return None


def verify_nonpositive_expected_profit(outcomes, *, rounds):
    """Exact proof for fixed-stake IID rounds by linearity of expectation.

    This is a conditional theorem: assumes independent repetitions of the
    supplied stationary distribution, with a fixed unit stake per round.
    """
    if type(rounds) is not int or rounds < 0:
        raise ValueError("rounds must be a nonnegative integer")
    metrics = exact_game_analysis(outcomes)
    expected_net = rounds * (metrics["rtp"] - 1)
    return {"expected_net": expected_net,
            "nonpositive": expected_net <= 0,
            "assumptions": "fixed unit stake; same distribution every round"}

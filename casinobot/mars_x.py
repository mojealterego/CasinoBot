"""MARS-X: bounded, offline, auditable hypothesis exploration.

Prototype only: no integration with MARS, CWM, Imandra, LTN or AlphaEvolve.
No external actions, gambling execution, or unverified proof claims.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import log, sqrt


@dataclass(frozen=True)
class Hypothesis:
    """A rational candidate for the gross RTP of a finite synthetic model."""
    numerator: int
    denominator: int

    def __post_init__(self):
        if self.denominator <= 0 or self.numerator < 0:
            raise ValueError("invalid rational hypothesis")

    @property
    def rtp(self):
        return Fraction(self.numerator, self.denominator)


@dataclass(frozen=True)
class Evaluation:
    candidate: Hypothesis
    score: float
    admissible: bool
    reason: str


def cognitive_firewall(candidate, *, max_rtp=Fraction(10), max_denominator=10000):
    """Hard invariants, not a trained Logic Tensor Network."""
    if not isinstance(candidate, Hypothesis):
        return False, "wrong candidate type"
    if candidate.denominator > max_denominator:
        return False, "complexity bound"
    if candidate.rtp > max_rtp:
        return False, "model RTP bound"
    return True, "admissible synthetic hypothesis"


def evaluate(candidate, stakes, payouts):
    """Held-out squared error; observations never imply RNG predictability."""
    allowed, reason = cognitive_firewall(candidate)
    if not allowed:
        return Evaluation(candidate, float("-inf"), False, reason)
    if not stakes or len(stakes) != len(payouts):
        raise ValueError("nonempty matched observations required")
    if any(type(s) is not int or s <= 0 for s in stakes):
        raise ValueError("invalid stakes")
    if any(type(p) is not int or p < 0 for p in payouts):
        raise ValueError("invalid payouts")
    observed = sum(payouts) / sum(stakes)
    error = float(candidate.rtp) - observed
    return Evaluation(candidate, -error * error, True, reason)


def evolve_hypotheses(initial, stakes, payouts, *, generations=3, beam_width=8):
    """Deterministic beam search over bounded rational mutations.

    Inspired by evolutionary search and MCTS-style candidate ranking; this
    is NOT an MCTS implementation or AlphaEvolve integration.
    """
    if type(generations) is not int or not 0 <= generations <= 100:
        raise ValueError("invalid generations")
    if type(beam_width) is not int or not 1 <= beam_width <= 1000:
        raise ValueError("invalid beam width")
    pool = {initial}
    history = []
    for step in range(generations + 1):
        ranked = sorted(
            (evaluate(h, stakes, payouts) for h in pool),
            key=lambda e: (-e.score, e.candidate.denominator, e.candidate.numerator),
        )
        admissible = [e for e in ranked if e.admissible][:beam_width]
        if not admissible:
            raise ValueError("no admissible hypotheses")
        best = admissible[0]
        history.append({"generation": step, "best_rtp": str(best.candidate.rtp),
                        "score": best.score, "evaluated": len(pool)})
        if step == generations:
            return {"best": best.candidate, "history": history,
                    "status": "empirical fit only; not a mathematical proof"}
        pool = set()
        for item in admissible:
            h = item.candidate
            for n, d in ((h.numerator + 1, h.denominator),
                         (h.numerator - 1, h.denominator),
                         (h.numerator, h.denominator + 1),
                         (h.numerator, h.denominator - 1)):
                if n >= 0 and d > 0:
                    pool.add(Hypothesis(n, d))
            pool.add(h)
    raise AssertionError("unreachable")

"""Offline exposure analysis of the photographed 'Sekwencja na Monety'.

This is not a strategy recommendation or an RNG prediction model.
"""
from math import isfinite

BASES = {
    "I": (1, 2, 3, 15, 50, 150, 500),
    "II": (1, 3, 15, 50, 150, 500, 2500),
    "III": (1, 15, 50, 150, 500, 2500, 8000),
}


def exposure(base, *, unit=1.0, rounds_per_level=3, bankroll=None):
    """Return worst-case outlay if every scheduled stake is lost.

    The photographed rules are ambiguous; this deliberately models only
    three consecutive spins at each level, with no wins, bonuses or resets.
    """
    if base not in BASES:
        raise ValueError("base must be I, II or III")
    if type(rounds_per_level) is not int or not 1 <= rounds_per_level <= 100:
        raise ValueError("rounds_per_level must be an integer in [1, 100]")
    if type(unit) not in (int, float) or not isfinite(unit) or unit <= 0:
        raise ValueError("unit must be finite and positive")
    if bankroll is not None and (
        type(bankroll) not in (int, float)
        or not isfinite(bankroll) or bankroll < 0
    ):
        raise ValueError("bankroll must be finite and nonnegative")
    levels = BASES[base]
    total = sum(levels) * rounds_per_level * unit
    highest_spin = max(levels) * unit
    affordable = bankroll is None or bankroll >= total
    return {
        "base": base,
        "stakes": levels,
        "unit": unit,
        "rounds_per_level": rounds_per_level,
        "spins": len(levels) * rounds_per_level,
        "worst_case_loss": total,
        "maximum_single_stake": highest_spin,
        "bankroll_sufficient_for_all_losses": affordable,
        "assumptions": "all spins lose; no resets, bonuses, or changes to the sequence",
    }


def expected_net_for_fixed_stakes(base, *, rtp, unit=1.0, rounds_per_level=3):
    """Linearity-of-expectation illustration for a fixed schedule only.

    RTP is a hypothetical constant return per unit wagered, not an estimate
    of a particular machine; conditional stake selection is not modeled.
    """
    if type(rtp) not in (int, float) or not isfinite(rtp) or not 0 <= rtp <= 1:
        raise ValueError("rtp must be finite in [0, 1]")
    report = exposure(base, unit=unit, rounds_per_level=rounds_per_level)
    return report["worst_case_loss"] * (rtp - 1)

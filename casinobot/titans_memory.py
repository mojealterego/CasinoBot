"""Bounded surprise-weighted hypothesis memory inspired by Titans.

This is an interpretable scalar prototype, NOT a neural Titans implementation.
It stores model-diagnostic surprise, not evidence of RNG predictability.
"""
from dataclasses import dataclass
from math import isfinite, log


@dataclass(frozen=True)
class MemoryState:
    surprise_ema: float = 0.0
    evidence: float = 0.0
    observations: int = 0


class SurpriseMemory:
    """Surprisal + adaptive decay gate, with explicit finite numeric bounds."""

    def __init__(self, *, decay: float = 0.95, surprise_scale: float = 5.0):
        if not isfinite(decay) or not 0 <= decay <= 1:
            raise ValueError("decay must be finite in [0,1]")
        if not isfinite(surprise_scale) or surprise_scale <= 0:
            raise ValueError("surprise_scale must be finite and positive")
        self.decay = decay
        self.surprise_scale = surprise_scale
        self.state = MemoryState()

    def observe(self, probability: float, *, signal: float = 1.0) -> dict:
        """Observe probability assigned BEFORE the outcome was seen.

        signal is a bounded diagnostic feature in [-1,1]. A high surprise
        changes retention, not the inferred probability of future outcomes.
        """
        if not isfinite(probability) or not 0 < probability <= 1:
            raise ValueError("probability must be finite in (0,1]")
        if not isfinite(signal) or not -1 <= signal <= 1:
            raise ValueError("signal must be finite in [-1,1]")
        surprise = -log(probability)
        novelty = surprise / (surprise + self.surprise_scale)
        retention = self.decay + (1 - self.decay) * novelty
        previous = self.state
        evidence = retention * previous.evidence + (1 - retention) * signal
        surprise_ema = self.decay * previous.surprise_ema + (1 - self.decay) * surprise
        self.state = MemoryState(surprise_ema, evidence, previous.observations + 1)
        return {
            "surprise": surprise,
            "weight_decay_gate": retention,
            "surprise_ema": surprise_ema,
            "memory_signal": evidence,
            "observations": self.state.observations,
        }

    def reset(self):
        self.state = MemoryState()

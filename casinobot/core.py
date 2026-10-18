"""Deterministic offline educational simulator."""
from dataclasses import dataclass
from decimal import Decimal
import random

@dataclass(frozen=True)
class Config:
    starting_credits: Decimal = Decimal("200")
    stake: Decimal = Decimal("1")
    max_rounds: int = 1000
    payout_probability: float = 0.3
    payout_multiplier: Decimal = Decimal("3")
    seed: int = 42

    def __post_init__(self):
        if (not self.starting_credits.is_finite() or not self.stake.is_finite()
                or self.starting_credits <= 0 or self.stake <= 0 or self.max_rounds <= 0):
            raise ValueError("Invalid credits, stake or max_rounds")
        if not 0 <= self.payout_probability <= 1 or not self.payout_multiplier.is_finite() or self.payout_multiplier < 0:
            raise ValueError("Invalid payout distribution")

@dataclass(frozen=True)
class Result:
    rounds: int
    final_credits: Decimal
    total_staked: Decimal
    total_paid: Decimal
    stopped_reason: str

    @property
    def observed_rtp(self) -> float:
        return float(self.total_paid / self.total_staked) if self.total_staked else 0.0

def simulate(cfg: Config) -> Result:
    rng = random.Random(cfg.seed)
    balance = cfg.starting_credits
    wagered = Decimal(0)
    paid = Decimal(0)
    rounds = 0
    while rounds < cfg.max_rounds and balance >= cfg.stake:
        balance -= cfg.stake
        wagered += cfg.stake
        payout = cfg.stake * cfg.payout_multiplier if rng.random() < cfg.payout_probability else Decimal(0)
        paid += payout
        balance += payout
        rounds += 1
    return Result(rounds, balance, wagered, paid,
                  "round_limit" if rounds == cfg.max_rounds else "insufficient_credits")

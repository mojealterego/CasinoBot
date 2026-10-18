"""Synthetic payout model. RTP is an expectation, not a promise."""
from dataclasses import dataclass
import random

@dataclass(frozen=True)
class PayoutModel:
    rtp_basis_points: int = 9659
    hit_probability_basis_points: int = 3000

    def __post_init__(self) -> None:
        if not 0 <= self.rtp_basis_points <= 10000:
            raise ValueError("RTP must be between 0 and 10000 basis points")
        if not 1 <= self.hit_probability_basis_points <= 10000:
            raise ValueError("hit probability must be between 1 and 10000 basis points")

    def payout_cents(self, stake_cents: int, rng: random.Random) -> int:
        if stake_cents <= 0:
            raise ValueError("stake must be positive")
        if rng.randrange(10000) >= self.hit_probability_basis_points:
            return 0
        # Unbiased stochastic rounding of the conditional payout.
        numerator = stake_cents * self.rtp_basis_points
        quotient, remainder = divmod(numerator, self.hit_probability_basis_points)
        return quotient + (rng.randrange(self.hit_probability_basis_points) < remainder)

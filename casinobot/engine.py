"""Risk-bounded offline simulation with integer accounting."""
from dataclasses import dataclass
import random
from .model import PayoutModel

@dataclass(frozen=True)
class SessionConfig:
    initial_cents: int = 20000
    stake_cents: int = 100
    max_rounds: int = 100
    max_loss_cents: int = 4000

    def __post_init__(self) -> None:
        if self.initial_cents <= 0 or self.stake_cents <= 0:
            raise ValueError("initial balance and stake must be positive")
        if self.max_rounds < 0 or not 0 <= self.max_loss_cents <= self.initial_cents:
            raise ValueError("invalid round or loss limit")

@dataclass(frozen=True)
class SessionResult:
    initial_cents: int
    final_cents: int
    wagered_cents: int
    paid_cents: int
    rounds: int
    reason: str

    @property
    def net_cents(self) -> int:
        return self.final_cents - self.initial_cents


def run_session(config: SessionConfig, model: PayoutModel, seed: int) -> SessionResult:
    rng = random.Random(seed)
    balance = config.initial_cents
    wagered = paid = rounds = 0
    floor = config.initial_cents - config.max_loss_cents
    reason = "round_limit"
    for _ in range(config.max_rounds):
        if balance - config.stake_cents < floor:
            reason = "risk_limit"
            break
        balance -= config.stake_cents
        payout = model.payout_cents(config.stake_cents, rng)
        balance += payout
        wagered += config.stake_cents
        paid += payout
        rounds += 1
    return SessionResult(config.initial_cents, balance, wagered, paid, rounds, reason)


def run_experiment(config: SessionConfig, model: PayoutModel, sessions: int, seed: int) -> dict:
    if sessions <= 0:
        raise ValueError("sessions must be positive")
    results = [run_session(config, model, seed + i) for i in range(sessions)]
    wagered = sum(r.wagered_cents for r in results)
    paid = sum(r.paid_cents for r in results)
    return {
        "sessions": sessions,
        "rounds": sum(r.rounds for r in results),
        "wagered_cents": wagered,
        "paid_cents": paid,
        "empirical_rtp_percent": round(100 * paid / wagered, 4) if wagered else None,
        "theoretical_rtp_percent": model.rtp_basis_points / 100,
        "mean_net_cents": sum(r.net_cents for r in results) / sessions,
        "risk_stops": sum(r.reason == "risk_limit" for r in results),
    }

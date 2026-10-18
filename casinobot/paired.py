"""Deterministic offline paired experiments with common random numbers.

All scenarios are synthetic; sharing outcomes reduces Monte Carlo noise but
cannot establish a profitable real-world strategy.
"""
from dataclasses import dataclass
from math import sqrt
from random import Random
from statistics import NormalDist


@dataclass(frozen=True)
class Policy:
    name: str
    stake_cents: int
    max_rounds: int = 100

    def __post_init__(self):
        if not self.name or self.stake_cents <= 0 or self.max_rounds < 0:
            raise ValueError("invalid policy")


def compare_policies(
    a: Policy, b: Policy, *,
    initial_cents: int = 20000,
    max_loss_cents: int = 4000,
    sessions: int = 1000,
    seed: int = 42,
    hit_bps: int = 3000,
    rtp_bps: int = 9659,
) -> dict:
    """Paired comparison using the same uniform variates per potential round.

    Payouts use stochastic integer rounding and are generated as a function of
    the shared uniforms. Policies can stop at different rounds; the potential
    outcome stream is generated before either policy is evaluated.
    """
    if sessions < 2 or initial_cents <= 0 or not 0 <= max_loss_cents <= initial_cents:
        raise ValueError("invalid experiment size or bankroll")
    if not 1 <= hit_bps <= 10000 or not 0 <= rtp_bps <= 10000:
        raise ValueError("invalid model")
    rng = Random(seed)
    differences = []
    results_a = []
    results_b = []
    for _ in range(sessions):
        stream = [(rng.randrange(10000), rng.randrange(hit_bps))
                  for _ in range(max(a.max_rounds, b.max_rounds))]

        def evaluate(policy):
            balance = initial_cents
            floor = initial_cents - max_loss_cents
            for hit, rounding in stream[:policy.max_rounds]:
                if balance - policy.stake_cents < floor:
                    break
                balance -= policy.stake_cents
                if hit < hit_bps:
                    quotient, remainder = divmod(policy.stake_cents * rtp_bps, hit_bps)
                    balance += quotient + (rounding < remainder)
            return balance - initial_cents

        net_a, net_b = evaluate(a), evaluate(b)
        results_a.append(net_a)
        results_b.append(net_b)
        differences.append(net_a - net_b)
    n = len(differences)
    mean = sum(differences) / n
    sample_variance = sum((x - mean) ** 2 for x in differences) / (n - 1)
    se = sqrt(sample_variance / n)
    z = NormalDist().inv_cdf(0.975)
    return {
        "sessions": n, "seed": seed, "policy_a": a.name, "policy_b": b.name,
        "mean_net_a_cents": sum(results_a) / n,
        "mean_net_b_cents": sum(results_b) / n,
        "paired_mean_difference_cents": mean,
        "paired_difference_ci95_cents": [mean - z * se, mean + z * se],
        "standard_error_difference_cents": se,
        "assumptions": "synthetic IID shared potential outcomes; approximate normal CI",
    }

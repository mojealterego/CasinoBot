"""Discrete active-inference laboratory for synthetic observations.

Finite Bayesian state inference and expected free-energy policy ranking.
Actions are symbolic experiment labels only: no real-world execution.
This is not JEPA training or a full Friston-style agent.
"""
from math import exp, isfinite, log


def _distribution(values, label):
    xs = tuple(values)
    if not xs or any(type(x) not in (int, float) or not isfinite(x) or x < 0 for x in xs):
        raise ValueError(f"{label}: finite nonnegative probabilities required")
    if abs(sum(xs) - 1.0) > 1e-9:
        raise ValueError(f"{label}: probabilities must sum to one")
    return xs


def _kl(p, q):
    return sum(x * log(x / y) if y > 0 else float("inf")
               for x, y in zip(p, q) if x > 0)


def _entropy(p):
    return -sum(x * log(x) for x in p if x > 0)


def posterior(prior, likelihoods, observation):
    """Bayes update P(state | observation), given P(observation | state).

    Rows of likelihoods correspond to latent states, columns to observations.
    """
    prior = _distribution(prior, "prior")
    rows = tuple(_distribution(row, "likelihood row") for row in likelihoods)
    if len(rows) != len(prior) or len({len(row) for row in rows}) != 1:
        raise ValueError("likelihood matrix shape mismatch")
    if type(observation) is not int or not 0 <= observation < len(rows[0]):
        raise ValueError("observation out of range")
    weights = [p * row[observation] for p, row in zip(prior, rows)]
    evidence = sum(weights)
    if evidence <= 0:
        raise ValueError("observation has zero evidence under model")
    return tuple(w / evidence for w in weights)


def evaluate_experiment(prior, likelihoods, preferences):
    """Expected free energy: outcome risk + conditional outcome ambiguity.

    Risk = KL(Q(o|action) || P_preferred(o)).
    Ambiguity = E_Q(s)[H(P(o|s,action))].
    Also reports mutual information I(S;O), without counting it twice.
    """
    prior = _distribution(prior, "prior")
    rows = tuple(_distribution(row, "likelihood row") for row in likelihoods)
    pref = _distribution(preferences, "preferences")
    if len(rows) != len(prior) or any(len(row) != len(pref) for row in rows):
        raise ValueError("likelihood matrix shape mismatch")
    predicted = tuple(sum(prior[i] * rows[i][j] for i in range(len(prior)))
                      for j in range(len(pref)))
    risk = _kl(predicted, pref)
    ambiguity = sum(p * _entropy(row) for p, row in zip(prior, rows))
    information_gain = max(0.0, _entropy(predicted) - ambiguity)
    return {
        "predicted_observations": predicted,
        "risk_kl": risk,
        "ambiguity": ambiguity,
        "information_gain": information_gain,
        "expected_free_energy": risk + ambiguity,
        "units": "nats",
    }


def rank_experiments(prior, experiments, preferences):
    """Sort offline experimental models by expected free energy (lower first).

    experiments maps experiment names to state-conditional likelihood matrices.
    """
    if not experiments:
        raise ValueError("at least one experiment required")
    results = []
    for name, likelihoods in experiments.items():
        if not isinstance(name, str) or not name:
            raise ValueError("nonempty experiment name required")
        result = evaluate_experiment(prior, likelihoods, preferences)
        results.append({"experiment": name, **result})
    return sorted(results, key=lambda x: (x["expected_free_energy"], x["experiment"]))

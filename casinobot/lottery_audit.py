"""Combinatorial and statistical diagnostics for offline synthetic draws."""
from math import comb, isfinite, sqrt

def hypergeometric_probability(population: int, winners: int, picks: int, matches: int) -> float:
    if any(type(x) is not int for x in (population, winners, picks, matches)):
        raise ValueError("integer parameters required")
    if population < 1 or not 0 <= winners <= population or not 0 <= picks <= population:
        raise ValueError("invalid population")
    if not max(0, picks + winners - population) <= matches <= min(picks, winners):
        return 0.0
    return comb(winners, matches) * comb(population-winners, picks-matches) / comb(population, picks)

def exact_combination_count(population: int, picks: int) -> int:
    if type(population) is not int or type(picks) is not int or not 0 <= picks <= population:
        raise ValueError("invalid combination")
    return comb(population, picks)

def uniformity_statistic(samples, categories: int) -> dict:
    if type(categories) is not int or categories < 2:
        raise ValueError("invalid categories")
    xs = list(samples)
    if not xs or any(type(x) is not int or not 0 <= x < categories for x in xs):
        raise ValueError("invalid samples")
    expected = len(xs) / categories
    counts = [xs.count(i) for i in range(categories)]
    return {"chi_square": sum((x-expected)**2/expected for x in counts),
            "degrees_of_freedom": categories-1, "expected_per_bin": expected,
            "asymptotic_reliable": expected >= 5}

def lag_one_correlation(values) -> float | None:
    xs = list(values)
    if len(xs) < 3 or any(type(x) not in (int, float) or not isfinite(x) for x in xs):
        raise ValueError("invalid observations")
    a, b = xs[:-1], xs[1:]
    am, bm = sum(a)/len(a), sum(b)/len(b)
    denominator = sqrt(sum((x-am)**2 for x in a)*sum((x-bm)**2 for x in b))
    return sum((x-am)*(y-bm) for x,y in zip(a,b))/denominator if denominator else None

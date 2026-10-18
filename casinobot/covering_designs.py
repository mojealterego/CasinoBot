"""Exact bounded covering-design verification for offline lottery studies.

A guarantee (v,k,t) means every t-subset of the v selected positions is
contained in at least one k-position ticket. This does not predict a draw.
"""
from itertools import combinations
from math import comb


def verify_covering(v, k, t, blocks, *, max_subsets=250000):
    if any(type(x) is not int for x in (v, k, t, max_subsets)):
        raise ValueError("integer parameters required")
    if not (1 <= t <= k <= v <= 49) or max_subsets < 1:
        raise ValueError("invalid covering parameters")
    total = comb(v, t)
    if total > max_subsets:
        raise ValueError("verification limit exceeded")
    if not isinstance(blocks, (list, tuple)) or not blocks:
        raise ValueError("nonempty blocks required")
    if len(blocks) > 10000:
        raise ValueError("too many blocks")
    canonical = []
    for block in blocks:
        if not isinstance(block, (list, tuple)) or len(block) != k:
            raise ValueError("invalid block length")
        if any(type(n) is not int or n < 1 or n > v for n in block):
            raise ValueError("invalid block position")
        if len(set(block)) != k:
            raise ValueError("duplicate position in block")
        canonical.append(frozenset(block))
    if len(set(canonical)) != len(canonical):
        raise ValueError("duplicate blocks")
    covered = set()
    for block in canonical:
        covered.update(combinations(sorted(block), t))
    missing = [subset for subset in combinations(range(1, v + 1), t)
               if subset not in covered]
    return {
        "v": v, "k": k, "t": t, "blocks": len(canonical),
        "total_subsets": total, "covered_subsets": total - len(missing),
        "coverage_fraction": (total - len(missing)) / total,
        "guaranteed": not missing,
        "first_uncovered": list(missing[0]) if missing else None,
        "lower_bound_blocks": (total + comb(k, t) - 1) // comb(k, t),
        "scope": "conditional coverage of selected positions, not draw prediction",
    }

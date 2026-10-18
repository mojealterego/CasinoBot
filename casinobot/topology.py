"""Bounded Vietoris-Rips topology for offline concept-space experiments.

Computes Betti numbers over F2 at one radius. Not persistent homology,
not proof of missing knowledge, and not an autonomous agent.
"""
from itertools import combinations
from math import dist, isfinite


def _rank_mod2(columns):
    """Rank of a binary matrix represented by integer bitset columns."""
    pivots = {}
    for value in columns:
        x = value
        while x:
            pivot = x.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = x
                break
            x ^= pivots[pivot]
    return len(pivots)


def vietoris_rips_betti(points, radius: float, max_points: int = 16) -> dict:
    """Betti 0, 1, 2 for the full VR complex up to tetrahedra.

    The boundary of tetrahedra is required for correct beta_2.
    Complexity is combinatorial; strict size limit protects runtime.
    """
    points = tuple(tuple(p) for p in points)
    if not points or len(points) > max_points or max_points > 16:
        raise ValueError("point count outside bounded laboratory range")
    if not isfinite(radius) or radius < 0:
        raise ValueError("radius must be finite and nonnegative")
    dimensions = {len(p) for p in points}
    if len(dimensions) != 1 or next(iter(dimensions)) < 1:
        raise ValueError("points must have the same positive dimension")
    if any(not isfinite(x) for p in points for x in p):
        raise ValueError("coordinates must be finite")
    edges = {(i, j) for i, j in combinations(range(len(points)), 2)
             if dist(points[i], points[j]) <= radius}
    simplices = {0: [(i,) for i in range(len(points))]}
    for degree in (1, 2, 3):
        simplices[degree] = [
            face for face in combinations(range(len(points)), degree + 1)
            if all(pair in edges for pair in combinations(face, 2))
        ]
    ranks = {}
    for degree in (1, 2, 3):
        index = {face: i for i, face in enumerate(simplices[degree - 1])}
        columns = []
        for simplex in simplices[degree]:
            column = 0
            for face in combinations(simplex, degree):
                column ^= 1 << index[face]
            columns.append(column)
        ranks[degree] = _rank_mod2(columns)
    betti = [
        len(simplices[0]) - ranks[1],
        len(simplices[1]) - ranks[1] - ranks[2],
        len(simplices[2]) - ranks[2] - ranks[3],
    ]
    return {"radius": radius, "betti": betti,
            "simplices": {str(k): len(v) for k, v in simplices.items()},
            "field": "F2", "interpretation": "topological features, not verified knowledge gaps"}


def radius_scan(points, radii):
    """Compute Betti snapshots across increasing radii; not persistence barcodes."""
    rs = tuple(radii)
    if not rs or any(not isfinite(r) or r < 0 for r in rs):
        raise ValueError("finite nonnegative radii required")
    if any(a >= b for a, b in zip(rs, rs[1:])):
        raise ValueError("radii must increase strictly")
    return [vietoris_rips_betti(points, radius) for radius in rs]

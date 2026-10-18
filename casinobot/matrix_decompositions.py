"""Finite matrix diagnostics for synthetic research data; no external dependencies."""
from math import isfinite, sqrt

def _matrix(a):
    if not isinstance(a, (tuple, list)) or not 1 <= len(a) <= 64:
        raise ValueError("invalid matrix size")
    n = len(a)
    if any(not isinstance(r, (tuple, list)) or len(r) != n for r in a):
        raise ValueError("square matrix required")
    if any(type(v) not in (int, float) or not isfinite(v) for r in a for v in r):
        raise ValueError("finite real entries required")
    return [[float(v) for v in r] for r in a]

def cholesky(a, *, tolerance=1e-12):
    """Factor symmetric positive definite A into L L^T."""
    a = _matrix(a)
    if type(tolerance) not in (float, int) or not isfinite(tolerance) or tolerance < 0:
        raise ValueError("invalid tolerance")
    n = len(a)
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            if abs(a[i][j] - a[j][i]) > tolerance * max(1, abs(a[i][j]), abs(a[j][i])):
                raise ValueError("not symmetric")
            residual = a[i][j] - sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                if residual <= 0 or not isfinite(residual):
                    raise ValueError("not positive definite")
                l[i][j] = sqrt(residual)
            else:
                l[i][j] = residual / l[j][j]
    return l

def covariance(samples):
    """Unbiased covariance: observations are rows."""
    if not isinstance(samples, (list, tuple)) or len(samples) < 2:
        raise ValueError("two samples required")
    if not isinstance(samples[0], (list, tuple)) or not 1 <= len(samples[0]) <= 64:
        raise ValueError("invalid dimensions")
    d, n = len(samples[0]), len(samples)
    if any(not isinstance(r, (list, tuple)) or len(r) != d for r in samples):
        raise ValueError("ragged samples")
    if any(type(v) not in (int, float) or not isfinite(v) for r in samples for v in r):
        raise ValueError("non-finite sample")
    means = [sum(r[j] for r in samples) / n for j in range(d)]
    return [[sum((r[i] - means[i]) * (r[j] - means[j]) for r in samples) / (n - 1)
             for j in range(d)] for i in range(d)]

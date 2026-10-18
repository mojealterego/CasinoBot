"""Bounded symmetric eigendecomposition via Jacobi rotations (standard library only)."""
from math import atan2, cos, sin, sqrt, isfinite
from .matrix_decompositions import _matrix

def symmetric_eigen(a, *, tolerance=1e-10, max_sweeps=100):
    """Eigenvalues descending and orthonormal eigenvectors as columns.

    Raises ValueError if convergence or input validation fails.
    """
    a = _matrix(a)
    if type(tolerance) not in (float, int) or not isfinite(tolerance) or tolerance <= 0:
        raise ValueError("invalid tolerance")
    if type(max_sweeps) is not int or not 1 <= max_sweeps <= 10000:
        raise ValueError("invalid max_sweeps")
    n = len(a)
    for i in range(n):
        for j in range(i):
            if abs(a[i][j] - a[j][i]) > tolerance * max(1.0, abs(a[i][j]), abs(a[j][i])):
                raise ValueError("matrix must be symmetric")
            avg = (a[i][j] + a[j][i]) / 2
            a[i][j] = a[j][i] = avg
    v = [[float(i == j) for j in range(n)] for i in range(n)]
    scale = max(1.0, max(abs(x) for row in a for x in row))
    for _ in range(max_sweeps):
        p, q = 0, 0
        off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > off:
                    p, q, off = i, j, abs(a[i][j])
        if off <= tolerance * scale:
            break
        theta = 0.5 * atan2(2 * a[p][q], a[q][q] - a[p][p])
        c, s = cos(theta), sin(theta)
        # Columns: new p = c*p - s*q, new q = s*p + c*q.
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        a[p][p] = c*c*app - 2*c*s*apq + s*s*aqq
        a[q][q] = s*s*app + 2*c*s*apq + c*c*aqq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k != p and k != q:
                x, y = a[k][p], a[k][q]
                a[k][p] = a[p][k] = c*x - s*y
                a[k][q] = a[q][k] = s*x + c*y
            x, y = v[k][p], v[k][q]
            v[k][p], v[k][q] = c*x - s*y, s*x + c*y
    else:
        raise ValueError("Jacobi method did not converge")
    order = sorted(range(n), key=lambda i: a[i][i], reverse=True)
    return [a[i][i] for i in order], [[v[row][i] for i in order] for row in range(n)]

def symmetric_rank_k(a, rank, *, tolerance=1e-10):
    """Truncated spectral reconstruction of a symmetric matrix; not general SVD."""
    original = _matrix(a)
    if type(rank) is not int or not 0 <= rank <= len(original):
        raise ValueError("invalid rank")
    values, vectors = symmetric_eigen(original, tolerance=tolerance)
    n = len(values)
    result = [[sum(values[k] * vectors[i][k] * vectors[j][k] for k in range(rank))
               for j in range(n)] for i in range(n)]
    error = sqrt(sum((original[i][j] - result[i][j]) ** 2
                     for i in range(n) for j in range(n)))
    return {"eigenvalues": values, "approximation": result, "frobenius_error": error}

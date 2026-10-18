"""Bounded real rectangular SVD via Gram eigenproblem; offline diagnostics only."""
from math import isfinite, sqrt
from .spectral_diagnostics import symmetric_eigen

def truncated_svd(matrix, rank=None, *, tolerance=1e-10):
    """Return descending singular values, rank-k reconstruction and Frobenius error."""
    if not isinstance(matrix, (list, tuple)) or not 1 <= len(matrix) <= 64:
        raise ValueError("invalid row count")
    if not isinstance(matrix[0], (list, tuple)) or not 1 <= len(matrix[0]) <= 64:
        raise ValueError("invalid column count")
    rows, cols = len(matrix), len(matrix[0])
    if any(not isinstance(row, (list, tuple)) or len(row) != cols for row in matrix):
        raise ValueError("ragged matrix")
    if any(type(x) not in (int, float) or not isfinite(x) for row in matrix for x in row):
        raise ValueError("finite real entries required")
    if type(tolerance) not in (int, float) or not isfinite(tolerance) or tolerance <= 0:
        raise ValueError("invalid tolerance")
    if rank is None:
        rank = min(rows, cols)
    if type(rank) is not int or not 0 <= rank <= min(rows, cols):
        raise ValueError("invalid rank")
    a = [[float(x) for x in row] for row in matrix]
    gram = [[sum(a[r][i] * a[r][j] for r in range(rows))
             for j in range(cols)] for i in range(cols)]
    eigenvalues, vectors = symmetric_eigen(gram, tolerance=tolerance, max_sweeps=10000)
    scale = max(1.0, max(abs(x) for x in eigenvalues))
    if any(x < -tolerance * scale for x in eigenvalues):
        raise ValueError("negative Gram eigenvalue outside tolerance")
    singular_values = [sqrt(max(0.0, x)) for x in eigenvalues[:min(rows, cols)]]
    approximation = [[0.0] * cols for _ in range(rows)]
    for k in range(rank):
        v = [vectors[j][k] for j in range(cols)]
        av = [sum(a[i][j] * v[j] for j in range(cols)) for i in range(rows)]
        for i in range(rows):
            for j in range(cols):
                approximation[i][j] += av[i] * v[j]
    residual = sqrt(sum((a[i][j] - approximation[i][j]) ** 2
                        for i in range(rows) for j in range(cols)))
    if not isfinite(residual) or any(not isfinite(x) for x in singular_values):
        raise ValueError("numerical overflow")
    return {"singular_values": singular_values, "approximation": approximation,
            "frobenius_error": residual, "rank": rank, "shape": [rows, cols]}

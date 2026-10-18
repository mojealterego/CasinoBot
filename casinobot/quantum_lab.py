"""Offline classical QUBO laboratory and OpenQASM 2 export.

No QPU access, quantum advantage, cryptanalysis or remote execution.
The QASM circuit prepares uniform superposition and measures bits;
it does NOT solve or encode the QUBO objective in a quantum oracle.
"""
from itertools import product
from math import isfinite


def validate_qubo(matrix):
    rows = tuple(tuple(row) for row in matrix)
    n = len(rows)
    if not 1 <= n <= 16 or any(len(row) != n for row in rows):
        raise ValueError("QUBO must be square with 1..16 variables")
    if any(type(v) not in (int, float) or not isfinite(v) for row in rows for v in row):
        raise ValueError("QUBO coefficients must be finite")
    return rows


def qubo_energy(matrix, bits):
    q = validate_qubo(matrix)
    xs = tuple(bits)
    if len(xs) != len(q) or any(type(x) is not int or x not in (0, 1) for x in xs):
        raise ValueError("bits must match QUBO dimension")
    return sum(q[i][j] * xs[i] * xs[j] for i in range(len(q)) for j in range(len(q)))


def solve_qubo_classically(matrix):
    """Exact exhaustive minimization, suitable only for small instances."""
    q = validate_qubo(matrix)
    best_bits, best_energy = None, float("inf")
    for bits in product((0, 1), repeat=len(q)):
        energy = sum(q[i][j] * bits[i] * bits[j]
                     for i in range(len(q)) for j in range(len(q)))
        if energy < best_energy:
            best_bits, best_energy = bits, energy
    return {"bits": list(best_bits), "energy": best_energy,
            "method": "classical_exhaustive", "evaluated": 1 << len(q)}


def qasm_sampling_template(matrix):
    """Valid OpenQASM 2.0 sampling template, not a QUBO solver."""
    n = len(validate_qubo(matrix))
    return ("OPENQASM 2.0;\ninclude \"qelib1.inc\";\n"
            f"qreg q[{n}];\ncreg c[{n}];\n"
            + "".join(f"h q[{i}];\n" for i in range(n))
            + "".join(f"measure q[{i}] -> c[{i}];\n" for i in range(n)))


def quantum_candidate_assessment(matrix):
    """Honest dispatch recommendation; never silently send jobs to a QPU."""
    n = len(validate_qubo(matrix))
    return {"variables": n, "classical_states": 1 << n,
            "recommended_backend": "classical_exhaustive",
            "qpu_dispatch": False,
            "reason": "Small bounded problem; no verified QPU advantage or backend configured"}

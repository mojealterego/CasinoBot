"""Strict import of lottery system blocks from local CSV, no network or betting."""
import csv
from pathlib import Path
from .covering_designs import verify_covering


def import_blocks(path, *, v, k, t, max_rows=10000):
    """Read one k-number ticket per row; optionally skip a single L1..Lk header."""
    if type(max_rows) is not int or not 1 <= max_rows <= 10000:
        raise ValueError("invalid max_rows")
    blocks = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        for line, fields in enumerate(reader, 1):
            if line == 1 and fields == [f"L{i}" for i in range(1, k + 1)]:
                continue
            if len(fields) != k:
                raise ValueError(f"line {line}: expected {k} numbers")
            try:
                numbers = tuple(int(x.strip()) for x in fields)
            except ValueError as exc:
                raise ValueError(f"line {line}: non-integer field") from exc
            blocks.append(numbers)
            if len(blocks) > max_rows:
                raise ValueError("row limit exceeded")
    return verify_covering(v, k, t, blocks)


def full_system(v, k, *, max_blocks=10000):
    """Construct all k-subsets, with explicit limit to prevent excessive output."""
    from itertools import combinations
    from math import comb
    if any(type(x) is not int for x in (v, k, max_blocks)):
        raise ValueError("integer parameters required")
    if not 1 <= k <= v <= 49 or not 1 <= max_blocks <= 10000:
        raise ValueError("invalid parameters")
    if comb(v, k) > max_blocks:
        raise ValueError("system exceeds block limit")
    return list(combinations(range(1, v + 1), k))

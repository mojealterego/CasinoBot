"""Binary hyperdimensional computing for offline synthetic concept experiments.

Bit-packed VSA with XOR binding, majority bundling, Hamming retrieval.
Not an AGI/ASI system or a lossless replacement for floating-point models.
"""
from hashlib import shake_256
from random import Random


def _check_dimension(d):
    if type(d) is not int or not 64 <= d <= 65536:
        raise ValueError("dimension must be integer in [64,65536]")


def _check_vector(v, d):
    if type(v) is not int or not 0 <= v < (1 << d):
        raise ValueError("invalid packed hypervector")


def symbol(name: str, *, dimension=10000, namespace="casinobot-vsa-v1") -> int:
    """Deterministic pseudorandom bit-vector, not a cryptographic identity."""
    _check_dimension(dimension)
    if not isinstance(name, str) or not name:
        raise ValueError("nonempty symbol required")
    data = (namespace + "\x00" + name).encode("utf-8")
    byte_count = (dimension + 7) // 8
    return int.from_bytes(shake_256(data).digest(byte_count), "big") & ((1 << dimension) - 1)


def bind(a: int, b: int, *, dimension=10000) -> int:
    _check_dimension(dimension)
    _check_vector(a, dimension)
    _check_vector(b, dimension)
    return a ^ b


def unbind(bound: int, key: int, *, dimension=10000) -> int:
    return bind(bound, key, dimension=dimension)


def hamming_distance(a: int, b: int, *, dimension=10000) -> int:
    _check_dimension(dimension)
    _check_vector(a, dimension)
    _check_vector(b, dimension)
    return (a ^ b).bit_count()


def similarity(a: int, b: int, *, dimension=10000) -> float:
    """Normalized Hamming similarity, not cosine similarity."""
    return 1.0 - hamming_distance(a, b, dimension=dimension) / dimension


def bundle(vectors, *, dimension=10000, tie_seed=0) -> int:
    """Per-bit majority vote. Deterministic random tie-break for even counts."""
    _check_dimension(dimension)
    xs = tuple(vectors)
    if not xs:
        raise ValueError("at least one vector required")
    for x in xs:
        _check_vector(x, dimension)
    rng = Random(tie_seed)
    result = 0
    threshold = len(xs) / 2
    for bit in range(dimension):
        count = sum((x >> bit) & 1 for x in xs)
        if count > threshold or (count == threshold and rng.getrandbits(1)):
            result |= 1 << bit
    return result


def nearest(query: int, memory: dict, *, dimension=10000, limit=5):
    """Return nearest named prototypes; no guarantees against collisions."""
    _check_dimension(dimension)
    _check_vector(query, dimension)
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("invalid limit")
    for name, vector in memory.items():
        if not isinstance(name, str):
            raise ValueError("memory keys must be strings")
        _check_vector(vector, dimension)
    return sorted(((name, hamming_distance(query, v, dimension=dimension))
                   for name, v in memory.items()), key=lambda x: (x[1], x[0]))[:limit]

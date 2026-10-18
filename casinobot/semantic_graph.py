"""Versioned semantic dependency graph for offline CasinoBot research.

Single-source concepts and explicit dependency references; updates are atomic
within this in-memory object. This is not quantum entanglement, GNN training,
distributed coherence, or zero-compute propagation.
"""
from copy import deepcopy
from hashlib import sha256
from json import dumps


class ConceptGraph:
    def __init__(self):
        self._nodes = {}
        self._dependencies = {}

    @staticmethod
    def _digest(value):
        encoded = dumps(value, sort_keys=True, ensure_ascii=False,
                        allow_nan=False, separators=(",", ":")).encode("utf-8")
        return sha256(encoded).hexdigest()

    def put(self, key: str, value: dict, *, expected_version: int | None = None) -> int:
        if not isinstance(key, str) or not key:
            raise ValueError("concept key required")
        if not isinstance(value, dict):
            raise ValueError("concept value must be a dictionary")
        stored = self._nodes.get(key)
        current = stored["version"] if stored else 0
        if expected_version is not None and (type(expected_version) is not int
                                             or expected_version != current):
            raise ValueError("version conflict")
        data = deepcopy(value)
        digest = self._digest(data)
        self._nodes[key] = {"version": current + 1, "value": data, "digest": digest}
        return current + 1

    def get(self, key: str) -> dict:
        if key not in self._nodes:
            raise KeyError(key)
        return deepcopy(self._nodes[key])

    def link(self, dependent: str, concept: str) -> None:
        if dependent not in self._nodes or concept not in self._nodes:
            raise KeyError("both nodes must exist")
        if dependent == concept:
            raise ValueError("self dependency prohibited")
        self._dependencies.setdefault(dependent, set()).add(concept)

    def dependencies(self, dependent: str) -> dict:
        if dependent not in self._nodes:
            raise KeyError(dependent)
        return {key: self.get(key) for key in sorted(self._dependencies.get(dependent, ()))}

    def stale(self, dependent: str, snapshot: dict[str, int]) -> list[str]:
        """Report changed dependencies relative to caller's recorded versions."""
        if dependent not in self._nodes:
            raise KeyError(dependent)
        return [key for key, node in self.dependencies(dependent).items()
                if snapshot.get(key) != node["version"]]

    def snapshot_versions(self, dependent: str) -> dict[str, int]:
        return {key: node["version"] for key, node in self.dependencies(dependent).items()}

"""Bitemporal scenario memory for offline what-if simulations.

Scenarios are hypothetical, not forecasts. Valid time and recorded time are
separate. This in-memory prototype is not JEPA, RAG, or a distributed database.
"""
from datetime import datetime, timezone
from math import isfinite


def _timestamp(value):
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError("timezone-aware datetime required")
    return value.astimezone(timezone.utc)


class ScenarioMemory:
    def __init__(self):
        self._entries = []

    def record(self, scenario_id, *, valid_from, recorded_at, features,
               response, confidence=None):
        if not isinstance(scenario_id, str) or not scenario_id:
            raise ValueError("scenario id required")
        if not isinstance(response, str) or not response:
            raise ValueError("nonempty proposed response required")
        if not isinstance(features, dict) or not features:
            raise ValueError("nonempty feature dictionary required")
        if any(not isinstance(k, str) or not k or type(v) not in (int, float)
               or not isfinite(v) for k, v in features.items()):
            raise ValueError("finite numeric features required")
        if confidence is not None and (type(confidence) not in (int, float)
                                       or not isfinite(confidence)
                                       or not 0 <= confidence <= 1):
            raise ValueError("confidence must be in [0,1]")
        entry = {"scenario_id": scenario_id, "valid_from": _timestamp(valid_from),
                 "recorded_at": _timestamp(recorded_at),
                 "features": dict(features), "response": response,
                 "confidence": confidence}
        self._entries.append(entry)

    def retrieve(self, query, *, valid_at, known_at, limit=5):
        """Find recorded scenarios valid/known by cutoff, using normalized L1 distance.

        Caller must independently verify any proposed response before action.
        """
        if not isinstance(query, dict) or not query:
            raise ValueError("query features required")
        if any(not isinstance(k, str) or type(v) not in (int, float)
               or not isfinite(v) for k, v in query.items()):
            raise ValueError("invalid query features")
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("invalid result limit")
        valid_at, known_at = _timestamp(valid_at), _timestamp(known_at)
        ranked = []
        for entry in self._entries:
            if entry["valid_from"] > valid_at or entry["recorded_at"] > known_at:
                continue
            keys = set(query) | set(entry["features"])
            distance = sum(abs(query.get(k, 0)-entry["features"].get(k, 0))
                           / max(1.0, abs(query.get(k, 0)),
                                 abs(entry["features"].get(k, 0))) for k in keys)
            ranked.append((distance, entry["scenario_id"], entry))
        ranked.sort(key=lambda item: (item[0], item[1]))
        return [{"distance": distance, "scenario_id": entry["scenario_id"],
                 "response": entry["response"], "confidence": entry["confidence"],
                 "valid_from": entry["valid_from"].isoformat(),
                 "recorded_at": entry["recorded_at"].isoformat()}
                for distance, _, entry in ranked[:limit]]

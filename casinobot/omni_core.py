"""OmniCognitiveState and reversible R3Mem episode archive.

Content-addressed tokens are pointers into an archive, not compression
themselves. Lossless recovery requires retaining the archive bytes.
"""
from __future__ import annotations
import hashlib
import json
import zlib
from typing import TypedDict


class OmniCognitiveState(TypedDict):
    session_id: str
    sasos_episode_refs: list[str]
    sasos_active_ref: str | None
    hypotheses: list[dict]
    verification_results: list[dict]
    surprise_metric: float
    weight_decay_gate: float
    daemon_status: str


class R3Mem:
    """Deterministic, in-memory, content-addressed reversible episode archive."""

    def __init__(self):
        self._archive: dict[str, bytes] = {}

    @staticmethod
    def _serialize(episode: dict) -> bytes:
        if not isinstance(episode, dict):
            raise TypeError("episode must be a dictionary")
        return json.dumps(episode, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False).encode("utf-8")

    def encode_to_virtual_token(self, episode: dict) -> str:
        raw = self._serialize(episode)
        digest = hashlib.blake2b(raw, digest_size=32).hexdigest()
        token = "r3mem:" + digest
        compressed = zlib.compress(raw, level=9)
        old = self._archive.get(token)
        if old is not None and old != compressed:
            raise ValueError("content-address collision")
        self._archive[token] = compressed
        return token

    def decode_from_virtual_token(self, token: str) -> dict:
        if token not in self._archive:
            raise KeyError("unknown token; archive may be missing")
        raw = zlib.decompress(self._archive[token])
        expected = "r3mem:" + hashlib.blake2b(raw, digest_size=32).hexdigest()
        if expected != token:
            raise ValueError("archive integrity verification failed")
        return json.loads(raw.decode("utf-8"))

    def export_archive(self) -> dict[str, str]:
        """Portable JSON-safe representation; hex encoding is not compression."""
        return {token: payload.hex() for token, payload in self._archive.items()}

    def import_archive(self, entries: dict[str, str]) -> None:
        """Verify each entry before atomically merging it into the archive."""
        validated = {}
        for token, payload_hex in entries.items():
            payload = bytes.fromhex(payload_hex)
            raw = zlib.decompress(payload)
            expected = "r3mem:" + hashlib.blake2b(raw, digest_size=32).hexdigest()
            if token != expected:
                raise ValueError("archive integrity verification failed")
            json.loads(raw.decode("utf-8"))
            validated[token] = payload
        self._archive.update(validated)


def initial_state(session_id: str) -> OmniCognitiveState:
    if not session_id:
        raise ValueError("session_id required")
    return {
        "session_id": session_id, "sasos_episode_refs": [],
        "sasos_active_ref": None, "hypotheses": [],
        "verification_results": [], "surprise_metric": 0.0,
        "weight_decay_gate": 1.0, "daemon_status": "idle",
    }

"""Proof-carrying finite computation receipts for offline research.

These receipts are SHA-256 commitments plus independently recomputed arithmetic.
They are NOT zero-knowledge proofs, SNARKs, or proofs of arbitrary agent reasoning.
"""
import hashlib
import hmac
import json


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def _validate_statement(statement):
    if not isinstance(statement, dict) or set(statement) != {"operation", "inputs", "result"}:
        raise ValueError("statement must have operation, inputs and result")
    operation = statement["operation"]
    inputs = statement["inputs"]
    if operation not in ("sum", "product", "sum_of_squares"):
        raise ValueError("unsupported arithmetic circuit")
    if not isinstance(inputs, list) or not 1 <= len(inputs) <= 256:
        raise ValueError("bounded integer inputs required")
    if any(type(x) is not int or abs(x) > 10**9 for x in inputs):
        raise ValueError("integer input outside bounds")
    if type(statement["result"]) is not int:
        raise ValueError("integer result required")


def evaluate_circuit(operation, inputs):
    if operation == "sum":
        return sum(inputs)
    if operation == "product":
        result = 1
        for value in inputs:
            result *= value
        return result
    if operation == "sum_of_squares":
        return sum(value * value for value in inputs)
    raise ValueError("unsupported arithmetic circuit")


def make_receipt(operation: str, inputs: list[int]) -> dict:
    statement = {"operation": operation, "inputs": list(inputs), "result": 0}
    _validate_statement(statement)
    statement["result"] = evaluate_circuit(operation, inputs)
    digest = hashlib.sha256(_canonical(statement)).hexdigest()
    return {"scheme": "casinobot-recompute-v1", "statement": statement,
            "commitment_sha256": digest}


def verify_receipt(receipt: dict) -> bool:
    if not isinstance(receipt, dict) or set(receipt) != {
        "scheme", "statement", "commitment_sha256"
    } or receipt["scheme"] != "casinobot-recompute-v1":
        return False
    try:
        statement = receipt["statement"]
        _validate_statement(statement)
        commitment = receipt["commitment_sha256"]
        if not isinstance(commitment, str) or len(commitment) != 64:
            return False
        if not hmac.compare_digest(hashlib.sha256(_canonical(statement)).hexdigest(),
                                   commitment):
            return False
        return evaluate_circuit(statement["operation"], statement["inputs"]) == statement["result"]
    except (ValueError, TypeError, OverflowError):
        return False

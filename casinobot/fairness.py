"""Verification primitives for disclosed, synthetic provably-fair rounds.

The digest authenticates a commitment to a server seed. It does not prove
that the game's payout mapping or the operator is fair.
"""
import hashlib
import hmac

def server_seed_commitment(server_seed: str) -> str:
    if not isinstance(server_seed, str) or not server_seed:
        raise ValueError("nonempty server seed required")
    return hashlib.sha256(server_seed.encode("utf-8")).hexdigest()

def verify_commitment(server_seed: str, expected_sha256: str) -> bool:
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        return False
    return hmac.compare_digest(server_seed_commitment(server_seed), expected_sha256.lower())

def derive_digest(server_seed: str, client_seed: str, nonce: int) -> str:
    """Reference HMAC-SHA512; a provider-specific protocol may differ."""
    if not isinstance(server_seed, str) or not server_seed:
        raise ValueError("server seed required")
    if not isinstance(client_seed, str) or not client_seed:
        raise ValueError("client seed required")
    if type(nonce) is not int or nonce < 0:
        raise ValueError("nonce must be a nonnegative integer")
    message = f"{client_seed}:{nonce}".encode("utf-8")
    return hmac.new(server_seed.encode("utf-8"), message, hashlib.sha512).hexdigest()

def verify_disclosed_round(server_seed: str, commitment: str,
                           client_seed: str, nonce: int, claimed_digest: str) -> bool:
    if not isinstance(claimed_digest, str) or len(claimed_digest) != 128:
        return False
    if not verify_commitment(server_seed, commitment):
        return False
    return hmac.compare_digest(derive_digest(server_seed, client_seed, nonce),
                               claimed_digest.lower())

import argparse
import json
from dataclasses import asdict
from decimal import Decimal
from .core import Config, simulate

def main():
    p = argparse.ArgumentParser(description="Offline CasinoBot simulator")
    p.add_argument("--rounds", type=int, default=1000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--stake", type=Decimal, default=Decimal("1"))
    args = p.parse_args()
    cfg = Config(max_rounds=args.rounds, seed=args.seed, stake=args.stake)
    result = simulate(cfg)
    print(json.dumps({**{k: str(v) if isinstance(v, Decimal) else v
                        for k, v in asdict(result).items()},
                      "observed_rtp": result.observed_rtp,
                      "theoretical_rtp": cfg.payout_probability * float(cfg.payout_multiplier)},
                     indent=2))

if __name__ == "__main__":
    main()

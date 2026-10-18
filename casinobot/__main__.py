"""Offline CasinoBot command-line research interface."""
import argparse
import json
from .engine import SessionConfig, run_experiment
from .model import PayoutModel

def main() -> None:
    parser = argparse.ArgumentParser(description="CasinoBot offline research")
    parser.add_argument("--sessions", type=int, default=1000)
    parser.add_argument("--rounds", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--stake-cents", type=int, default=100)
    parser.add_argument("--bankroll-cents", type=int, default=20000)
    parser.add_argument("--max-loss-cents", type=int, default=4000)
    parser.add_argument("--rtp-bps", type=int, default=9659)
    args = parser.parse_args()
    config = SessionConfig(args.bankroll_cents, args.stake_cents, args.rounds, args.max_loss_cents)
    print(json.dumps(run_experiment(config, PayoutModel(args.rtp_bps), args.sessions, args.seed), indent=2))

if __name__ == "__main__":
    main()

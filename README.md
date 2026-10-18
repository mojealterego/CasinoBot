# CasinoBot APEX — Offline Research Laboratory

Deterministic Python stochastic simulator, no real-money betting or casino connections.

## Run
```bash
python -m casinobot --rounds 1000 --seed 42
python -m unittest discover -s tests -v
```

## Roadmap
| Stage | Description | Status |
|---|---|---|
| 0.01 | PDF architecture and mathematical audit | Done |
| 0.02 | Deterministic offline simulator | Done |
| 0.03 | Validation and five unit tests | Done |
| 0.04 | Batch Monte Carlo with confidence intervals | To do |
| 0.05 | Empirically calibrated payout distributions | To do |
| 0.06 | Event sourced FSM and replay | To do |
| 0.07 | CI, fuzzing, provenance and supply chain | To do |

**Research limitations:** Synthetic probability 0.3 and multiplier 3 imply theoretical RTP 90%, not the 96.59% claimed in the supplied PDF. No live-game fidelity is claimed.

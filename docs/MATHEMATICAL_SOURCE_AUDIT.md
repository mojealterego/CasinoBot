# Mathematical source audit — CasinoBot

## Scope and provenance
Read-only reference: `mojealterego/Problemy-milenijne` (private repository, default `main`).
The source repository is **not** a code deployment target. This document does
not claim a full page-by-page verification of all three source volumes.

Located source: `materiały źródłowe/TOM I — ONTOLOGIA LICZBY I GEOMETRII (619 stron) — Markdown.md`.
Other indexed source materials include Tom II and Tom III, formal reconstruction,
and `docs/ETAP_53_VERIFICATION_MATRIX.md`.

## Extracted, independently testable tools
- Empirical RTP and mean net payout: `casinobot/statistics.py`.
- IID equal-stake normal-approximation confidence interval, explicitly labeled
  unreliable for rare heavy-tailed wins.
- Discrete KL divergence, including zero-support infinity handling.
- Exact one-dimensional discrete Wasserstein-1 distance on ordered common support.

These are established statistical techniques, **not** a validation of TRS.
All metrics characterize distributions, not future game outcomes.

## Claims excluded from the simulation engine
- `P != NP`, Riemann hypothesis, Hodge conjecture, BSD: all OPEN in
  `docs/WERDYKT_KONCOWY_REKONSTRUKCJI_TRS.md`.
- The identification Fisher–Rao = Kähler is not established globally.
- A negative covariance entry does not prove negative Ricci curvature.
- A universal golden-ratio spectral attractor is not established.
- No statistical tool here can establish a positive expectation from a game
  whose actual return is negative.

## Remaining research
1. Inventory Tom I, II and III page-by-page with source anchors.
2. Separate definitions, verified calculations, assumptions and conjectures.
3. Calibrate a game-specific payout distribution only from authorized data.
4. Evaluate bootstrap intervals and heavy-tail diagnostics.
5. Add replayable experiments and reproducibility manifests.
6. Verify all tests in GitHub Actions; writing tests is not evidence of a pass.

## Reproducibility
`python -m unittest discover -s tests -v`

The synthetic simulator is not a reverse-engineered casino model.

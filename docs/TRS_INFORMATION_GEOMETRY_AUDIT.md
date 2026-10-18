# TRS source audit — information geometry and complexity claims

Status: research notes, not accepted proofs. CasinoBot is an offline simulator, not a casino predictor.

## Documents examined
- *Definicje i Rygoryzacja Notacji* (2 pages): Fisher–Rao/Kähler postulate, Dirac operator, Weitzenböck–Lichnerowicz formula, Atiyah–Singer, golden-ratio stability.
- *Architektura Funktora Kwantyzacji Obliczeniowej* (79 pages): proposed functor, sheaves, Betti numbers, P vs NP, spectral RH arguments.
- *Obliczeniowa i Geometryczna Formalizacja TRS* (11 pages): Kähler/Fisher mapping, Ricci flow, Hodge and RH, proposed topological cryptography.
- *Teoria Rezonansu Strukturalnego: Analityczna i Spektralna Formalizacja* (6 pages).
- *Rygorystyczna Formalizacja Analityczna TRS* (12 pages; two copies in source context).
- Related earlier TRS source material indexed in project files.

## Findings and counterchecks
1. Fisher information is a legitimate statistical metric **for a specified differentiable statistical model**. It does not follow that all computations or all Kähler metrics are globally identical to physical energy or runtime. For Bernoulli(p), I(p)=1/[p(1-p)] and locally KL(p||p+d)=I(p)d²/2+O(d³). This bounded, testable part is implemented in `casinobot/information_geometry.py`.
2. An infinite-dimensional Hilbert space is not locally compact in its norm topology. Claiming an infinite-dimensional Hilbert manifold is locally compact requires a different topology and proof; neither can be silently assumed.
3. The Weitzenböck–Lichnerowicz and Atiyah–Singer formulas have hypotheses and apply to particular geometric operators. They do not imply that arbitrary algorithmic reductions preserve Betti numbers.
4. A sphere S^n (n>0) is **not contractible**. A continuous map need not be a homeomorphism and may collapse loops; polynomial-time reductions are not generally homeomorphisms. The proposed P/NP separation by sphere/torus topology is therefore unsupported.
5. A self-adjoint operator has real spectrum, but a rigorously constructed operator with spectrum matching all relevant nontrivial zeta zeros is the missing step; invoking self-adjointness alone does not prove RH.
6. Hodge theory's harmonic representatives do not imply every rational Hodge class is algebraic. The latter is precisely the unproved conjecture, not a consequence of stationary dissipation assumptions.
7. The golden ratio is relevant to some Diophantine approximation/KAM settings but not a demonstrated universal computational stability constant. No cryptographic security proof follows from these postulates.
8. Assertions about topological cryptography, automatic exponential complexity lower bounds and zero-loss computation are unverified and must not enter security-critical code.

## Engineering disposition
**Accepted:** finite-dimensional Fisher–Rao diagnostic and local KL approximation; explicit domain checks; regression tests.
**Research-only:** topology descriptors, numerical spectral experiments, benchmarking geometric representations on synthetic datasets.
**Rejected as established facts:** proofs of P≠NP/RH/Hodge, universal energy complexity, secure cryptographic protocols from TRS.

Next: benchmark information geometry on synthetic Bernoulli streams, compare with existing KL diagnostics, verify CI, and separately formalize any proposed complexity claim before adoption.

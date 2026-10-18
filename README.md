# CasinoBot APEX — Offline Research Laboratory

Deterministyczne laboratorium symulacji gier losowych. Brak integracji z kasynami, automatycznego obstawiania i maskowania botów.

## Uruchomienie

```bash
python -m casinobot --sessions 1000 --rounds 100 --seed 42
python -m unittest discover -s tests -v
```

Python 3.11+, bez zewnętrznych zależności.

## Moduły

- `casinobot/model.py`: syntetyczny rozkład wypłat o zadanej wartości oczekiwanej.
- `casinobot/engine.py`: księgowanie w groszach, ograniczenie strat, eksperymenty Monte Carlo.
- `casinobot/statistics.py`: empiryczne RTP, przedział ufności przy założeniu IID, KL i Wasserstein-1.
- `casinobot/paired.py`: sparowane porównania strategii z Common Random Numbers.
- `casinobot/bootstrap.py`: bootstrap RTP i diagnostyka koncentracji wypłat.
- `casinobot/reasoning.py`: dokładne rachunki wymierne, weryfikacja modeli skończonych i poszukiwanie kontrprzykładów.
- `casinobot/titans_memory.py`: prototyp pamięci diagnostycznej z metryką niespodzianki i bramką wygaszania.
- `casinobot/mars_x.py`: ograniczona ewolucyjna eksploracja hipotez z deterministyczną zaporą niezmienników.
- `casinobot/math_models.py`: matematyczne prymitywy Béziera, Fittsa, entropii, agregacji logiki rozmytej i ROI.
- `casinobot/omni_core.py`: typowany stan OmniCognitiveState, referencje SASOS i odwracalne archiwum R3Mem.
- `casinobot/__main__.py`: CLI JSON.
- `casinobot/core.py`: zachowany starszy interfejs API.
- `docs/MATHEMATICAL_SOURCE_AUDIT.md`: źródłowa analiza matematyczna TRS, ograniczenia i mapa dalszej pracy.

**Ograniczenia:** to nie jest model mechaniki Cube Mania Deluxe. Empiryczne RTP jest losowe. System nie przewiduje przyszłych wyników. Przedział ufności jest przybliżony i może być zawodny dla rzadkich dużych wypłat.

## Roadmapa

| Etap | Zakres | Stan |
|---|---|---|
| 0.01 | Audyt PDF | Done |
| 0.02 | Symulator offline | Done |
| 0.03 | Silnik ryzyka i księgowanie | Implemented |
| 0.04 | Testy i CI | CI pending |
| 0.05 | Przedziały ufności dla równych stawek, IID | Implemented, CI pending |
| 0.06 | Kalibracja empiryczna | To do |
| 0.07 | Event sourcing i replay | To do |
| 0.08 | KL i Wasserstein-1, testy jednostkowe | Implemented, CI pending |
| 0.09 | Inwentaryzacja matematyczna Tomów I–III TRS z odnośnikami do źródeł | In progress |
| 0.10 | Bootstrap RTP i diagnostyka koncentracji wypłat | Implemented, CI pending |
| 0.11 | Porównania sparowane CRN | Implemented, CI pending |
| 0.12 | Walidacja CI, pokrycia bootstrap i modeli ciężkoogonowych | To do |

| 0.13 | Matematyczny silnik rozumowania: rachunki dokładne, model checking i falsyfikacja | Implemented, CI pending |
| 0.14 | Formalne specyfikacje gier, automatyczne odkrywanie hipotez i integracja z zewnętrznym proverem | To do |
| 0.15 | Titans-inspired Surprise Memory i Weight Decay Gate | Prototype, CI pending |
| 0.16 | Pełna neuronowa implementacja Titans, uczenie w czasie inferencji i testy ablacyjne | To do |
| 0.17 | MARS-X: ograniczona ewolucja hipotez i hard-invariant firewall | Prototype, CI pending |
| 0.18 | CWM, pełne MCTS, LTN, ImandraX/CodeLogician i AlphaEvolve — rzeczywiste integracje | To do |
| 0.19 | Modele Béziera, Fittsa, entropii, fuzzy-LTN i ROI — prymitywy laboratoryjne | Implemented, CI pending |
| 0.20 | Integracja modeli matematycznych z orkiestracją MARS-X i walidacja | To do |
| 0.21 | OmniCognitiveState + R3Mem (BLAKE2b, zlib, integralność) | Prototype, CI pending |
| 0.22 | LangGraph + SASOS persistence + OmniDaemon orchestration | To do |
| 0.23 | Integracja pełnej neuronowej pamięci Titans ze stanem i grafem | To do |

## Silnik rozumowania matematycznego

`casinobot/reasoning.py` zapewnia weryfikację skończonych modeli na dokładnych ułamkach oraz ograniczone wyszukiwanie kontrprzykładów. Brak kontrprzykładu do zadanej głębokości **nie stanowi dowodu uniwersalnego**. Silnik nie jest połączony z Imandrą ani innym zewnętrznym systemem dowodowym; inspiracja formalną weryfikacją nie oznacza kompatybilności API. Matematyczne modele gier wymagają niezależnego potwierdzenia ich założeń.

## Integracja dokumentów z 18.10.2026

Nowe moduły: `casinobot/lottery_audit.py` i `casinobot/fairness.py`. Audyt źródeł: `docs/SOURCE_INTEGRATION_IMDP_CASINO.md`.

Etapy 0.24–0.26: audyt źródeł, matematyka kombinatoryczna i referencyjna weryfikacja HMAC — kod zapisany, CI niepotwierdzone. Etapy 0.27–0.28: Dirichlet, walidacja i rozszerzone modele ryzyka — do wykonania.

## Active Inference — laboratorium offline

`casinobot/active_inference.py` zawiera dyskretny model Bayesowski, oczekiwaną wolną energię (ryzyko KL + niejednoznaczność), zysk informacyjny oraz ranking eksperymentów. To prototyp matematyczny, **nie** implementacja JEPA, trening sieci neuronowej ani integracja z realnym środowiskiem. Nie wykonuje działań zewnętrznych.

Etap 0.29: dyskretne Active Inference i testy — Implemented, CI pending. Etap 0.30: sprzężenie z MARS-X, pamięcią Titans i audytem hipotez — To do. Etap 0.31: JEPA i model świata z ewaluacją poza próbą — To do.

## Topological Data Analysis (TDA) — etap 0.32

`casinobot/topology.py` implementuje ograniczony kompleks Vietorisa-Ripsa i liczby Bettiego beta0-beta2 nad F2, z przekrojami po promieniu. `tests/test_topology.py` zawiera testy geometrii i danych błędnych. **Implemented, CI pending.** To nie jest pełna homologia trwała ani wyznaczanie barcode'ów. Etap 0.33: rzeczywiste barcode'y trwałości i walidacja stabilności — To do. Etap 0.34: powiązanie hipotez topologicznych z Active Inference i audytem eksperymentów — To do. Struktury topologiczne nie stanowią same w sobie dowodu brakującej wiedzy.

## Interpretowalność reprezentacji — etap 0.35

`casinobot/sparse_features.py` zawiera eksperymentalne nieujemne kodowanie rzadkie przy stałym słowniku i karze L1; `tests/test_sparse_features.py` testuje rekonstrukcję, regularizację i walidację. **Implemented, CI pending.** Etap 0.36: uczenie słownika SAE na danych syntetycznych i walidacja na zbiorze testowym — To do. Etap 0.37: analiza aktywacji modelu za zgodą operatora i ewaluacja interpretowalności — To do. Samo L1 nie dowodzi monosemantyczności i nie eliminuje halucynacji.

## Graf semantyczny — etap 0.38

`casinobot/semantic_graph.py`: kanoniczne definicje pojęć, zależności, wersjonowanie optymistyczne, skróty SHA-256 i wykrywanie nieaktualnych referencji. `tests/test_semantic_graph.py`: testy referencji, aktualizacji, konfliktów i izolacji kopii. **Implemented, CI pending.** Etap 0.39: integracja grafu z OmniCognitiveState, Active Inference i MARS-X — To do. Etap 0.40: trwałe transakcje, audyt zdarzeń i rozproszona spójność — To do. Etap 0.41: ewaluacja GNN i uwagi grafowej na danych badawczych — To do. Nie jest to splątanie kwantowe ani automatyczna propagacja bez kosztu obliczeń.

## Weryfikacja mutacji — etap 0.42

`casinobot/mutation_guard.py`: ograniczona eksploracja skończonych systemów przejść, stany zabronione, wykrywanie cykli, trzy werdykty accepted/rejected/inconclusive. `tests/test_mutation_guard.py`: pięć testów. **Implemented, CI pending.** Etap 0.43: fail-closed gate przed wdrożeniem zmian w MARS-X — To do. Etap 0.44: TLA+/SMT (Z3), kontrprzykłady i modelowanie współbieżności — To do. Ten moduł nie dowodzi bezpieczeństwa dowolnego kodu i nie uruchamia wygenerowanych mutacji.

## Weryfikowalne potwierdzenia obliczeń — etap 0.45

`casinobot/proof_receipts.py` implementuje deterministyczne potwierdzenia SHA-256 dla ograniczonych obwodów arytmetycznych i niezależne przeliczenie wyników. `tests/test_proof_receipts.py` dodaje testy poprawności i manipulacji. **Implemented, CI pending.** To nie jest kryptografia zero-knowledge ani zk-SNARK. Etap 0.46: prototyp prawdziwego ZK dla jednego obwodu z uznanym systemem dowodowym — To do. Etap 0.47: pomiar kosztów dowodzenia/weryfikacji i integracja z bramką mutacji — To do.

## Wyżarzanie i scenariusze hipotetyczne — etapy 0.48–0.51

0.48: `casinobot/annealing.py` — powtarzalne wyżarzanie symulowane, harmonogram temperatury i twarda bramka dopuszczalności kandydatów; **Implemented, CI pending**. 0.49: `casinobot/scenario_memory.py` — pamięć hipotetycznych scenariuszy z osobnymi czasami obowiązywania i zapisu oraz rankingiem podobieństwa; **Implemented, CI pending**. `tests/test_annealing_scenarios.py` obejmuje 6 testów. 0.50: integracja z MARS-X, Mutation Guard i potwierdzeniami obliczeń — To do. 0.51: trwałe przechowywanie, ocena jakości scenariuszy, ewaluacja poza próbą i ewentualne JEPA — To do. Symulacje nie są prognozami, a sugestie reakcji wymagają niezależnej walidacji. Nie uruchamiać nieograniczonego idle compute.

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

## Obliczenia hiperwymiarowe — etapy 0.52–0.54

0.52: `casinobot/hypervectors.py` — binarne hiperwektory VSA/HDC, XOR, majority bundling, Hamming retrieval; `tests/test_hypervectors.py` (6 testów). **Implemented, CI pending.** 0.53: benchmark odporności na szum i kolizji na syntetycznych korpusach — To do. 0.54: integracja pamięci symbolicznej z grafem semantycznym i porównanie z embeddingami — To do. HDC nie gwarantuje odporności na 30% błędów dla dowolnej liczby pojęć ani nie stanowi bezstratnego zamiennika Transformerów.

## Hybrydowe obliczenia kwantowe — etapy 0.55–0.58

0.55: `casinobot/quantum_lab.py` — QUBO, dokładny klasyczny solver (n <= 16), referencyjny OpenQASM 2.0 wyłącznie do próbkowania i ocena dispatchu; `tests/test_quantum_lab.py` (6 testów). **Implemented, CI pending.** 0.56: QAOA z rzeczywistym operatorem kosztu, symulator i porównanie z optimum klasycznym — To do. 0.57: adapter QPU z limitami budżetu, kolejką, uwierzytelnieniem i audytem — To do. 0.58: benchmark jakości, kosztów, błędów i opóźnień wobec metod klasycznych — To do. Obecny QASM nie koduje funkcji celu QUBO, a kod nie komunikuje się z fizycznym QPU.

## Symulacje cyfrowych bliźniaków i FPGA — etapy 0.59–0.62

0.59: `casinobot/digital_twin.py` — deterministyczna, ograniczona symulacja zdarzeń i bramka oceny kandydatów; `tests/test_digital_twin.py` (6 testów). **Implemented, CI pending.** 0.60: zagnieżdżone scenariusze awarii, odtwarzanie syntetycznych śladów i metryki stabilności — To do. 0.61: izolowane środowiska kontenerowe, testy awarii i porównanie czasu wirtualnego z rzeczywistym — To do. 0.62: opcjonalny HLS/FPGA z walidacją równoważności i bezpiecznym rollbackiem — To do. Obecny moduł nie implementuje ROS/Gazebo, JEPA, sprzętowego FPGA ani fizycznego przyspieszania czasu.

## Dowody, intencje i analiza awarii — etapy 0.63–0.67

0.63: `casinobot/evidence_reasoning.py` — oceny częstotliwości i pewności inspirowane NARS, rozróżnienie dowodów niezależnych i wykrywanie konfliktów; **Implemented, CI pending**. 0.64: `casinobot/retrospective.py` — ograniczone przypisywanie kar do wcześniejszych decyzji po symulowanej awarii; **Implemented, CI pending**. `tests/test_evidence_retrospective.py` zawiera 8 testów. 0.65: jawne preferencje i zatwierdzanie przez operatora zamiast domniemanej CEV — To do. 0.66: integracja ocen z Mutation Guard, Digital Twin i pamięcią scenariuszy — To do. 0.67: testy odporności na zatrucie dowodów i kalibracji — To do. Moduły nie są pełnym NARS, CIRL, BPTT ani retrokauzalnością; nie zastępują niezależnych zabezpieczeń.

## Zintegrowana bramka oceny propozycji — etap 0.68

0.68: `casinobot/proposal_gate.py` — integracja Mutation Guard, Digital Twin, Evidence Reasoning i retrospektywnych kar. Status **Implemented, CI pending**; `tests/test_proposal_gate.py` (9 testów). Wszystkie bramki fail-closed, a pozytywny wynik oznacza tylko `eligible_for_human_review`, nigdy automatyczne wdrożenie. Następnie: 0.69 — podpisane zatwierdzenie operatora i audyt decyzji (To do); 0.70 — testy odporności na błędne i sprzeczne dowody, pełna walidacja CI (To do).

## Etap 0.71 — audyt TRS i geometria informacji

- **0.71 — Implemented, CI pending:** `casinobot/information_geometry.py` (Fisher–Rao, Bernoulli KL, lokalne rozwinięcie KL), `tests/test_information_geometry.py` (8 testów), `docs/TRS_INFORMATION_GEOMETRY_AUDIT.md` (krytyczny audyt źródeł TRS).
- **0.72 — Implemented, CI pending:** `casinobot/geometry_benchmark.py` (deterministyczna kalibracja Bernoulliego, zgodność KL z `statistics.py`, odległość Fishera–Rao i błąd estymacji), `tests/test_geometry_benchmark.py` (7 testów). Potwierdzenie GitHub Actions nadal wymagane.
- **0.73 — To do:** formalne kontrprzykłady do nieuprawnionych uogólnień topologicznych TRS; nie traktować deklaracji P≠NP/RH/Hodge jako udowodnionych.

## Etap 0.74 — diagnostyka macierzy

- **0.74 — Implemented, CI pending:** `casinobot/matrix_decompositions.py` implementuje ograniczony rozkład Cholesky'ego dla macierzy symetrycznych dodatnio określonych oraz nieobciążoną estymację kowariancji z obserwacji syntetycznych; `tests/test_matrix_decompositions.py` zawiera 8 testów jednostkowych. Nie implementuje SVD ani PCA; testy nie zostały jeszcze potwierdzone w CI.
- **0.75 — To do:** stabilne numerycznie SVD i redukcja rzędu z walidacją błędu aproksymacji.
- **0.76 — To do:** integracja diagnostyki macierzy z modułami statystycznymi i benchmarkami na danych syntetycznych.

### Etap 0.75 — ograniczona diagnostyka spektralna

- **0.75a — Implemented, CI pending:** `casinobot/spectral_diagnostics.py` — metoda Jacobiego dla rzeczywistych macierzy symetrycznych, wartości i wektory własne, aproksymacja rzędu k, błąd Frobeniusa; `tests/test_spectral_diagnostics.py` — 8 testów. Nie jest to pełne SVD dowolnych macierzy ani certyfikowana numerycznie procedura.
- **0.75b — To do:** SVD dla macierzy prostokątnych, niezależne porównanie numeryczne i testy kondycjonowania.
- **0.76 — To do:** integracja z analizą ryzyka na syntetycznych danych, testy CI i benchmarki.

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

## Silnik rozumowania matematycznego

`casinobot/reasoning.py` zapewnia weryfikację skończonych modeli na dokładnych ułamkach oraz ograniczone wyszukiwanie kontrprzykładów. Brak kontrprzykładu do zadanej głębokości **nie stanowi dowodu uniwersalnego**. Silnik nie jest połączony z Imandrą ani innym zewnętrznym systemem dowodowym; inspiracja formalną weryfikacją nie oznacza kompatybilności API. Matematyczne modele gier wymagają niezależnego potwierdzenia ich założeń.

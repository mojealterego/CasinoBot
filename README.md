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
- `casinobot/__main__.py`: CLI JSON.
- `casinobot/core.py`: zachowany starszy interfejs API.

**Ograniczenia:** to nie jest model mechaniki Cube Mania Deluxe. Empiryczne RTP jest losowe. System nie przewiduje przyszłych wyników.

## Roadmapa

| Etap | Zakres | Stan |
|---|---|---|
| 0.01 | Audyt PDF | Done |
| 0.02 | Symulator offline | Done |
| 0.03 | Silnik ryzyka i księgowanie | Implemented |
| 0.04 | Testy i CI | CI pending |
| 0.05 | Przedziały ufności | To do |
| 0.06 | Kalibracja empiryczna | To do |
| 0.07 | Event sourcing i replay | To do |

# Integracja dokumentów badawczych (2026-10-18)

Źródła użytkownika, zarchiwizowane poza repozytorium:
- System Gier Liczbowych i Aplikacja.PDF (10 stron), SHA-256: 958817dee711b1b7e8aaec1692b0022a43f57eed77062918afed05527714a533
- Projekt Kasyna Online z Manipulacją.PDF (13 stron), SHA-256: 5e255c66048ae503b4de30950e87012f788b021c66f190652474cd9ff0dd69ea

## Powiązanie z kodem

- IMDP, s. 3: kombinatoryka i rozkład hipergeometryczny -> casinobot/lottery_audit.py.
- IMDP, s. 4-5: cyfrowy bliźniak, Dirichlet i nadmierna dyspersja -> dalsza walidacja.
- Kasyno, s. 5: diagnostyka RNG i RTP -> casinobot/lottery_audit.py.
- Kasyno, s. 5-6: weryfikacja ujawnionego ziarna i HMAC -> casinobot/fairness.py.
- Kasyno, s. 6-8: EV, ryzyko ruiny i Kelly -> dalsze eksperymenty.
- Kasyno, s. 8-10: manipulacyjny UX -> wyłącznie audyt zagrożeń.

## Ograniczenia

Wykrycie odchylenia statystycznego nie dowodzi manipulacji. Historia niezależnych losowań nie daje automatycznej przewagi. Commitment i HMAC potwierdzają tylko spójność danych w konkretnym protokole, nie uczciwość całej gry. Format HMAC w kodzie jest referencyjny i nie jest deklarowany jako zgodny z operatorem. Dokumenty nie są dowodem możliwości gwarantowanego zysku.

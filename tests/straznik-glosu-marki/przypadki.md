# Przypadki testowe: straznik-glosu-marki

Fixture: fikcyjna marka Pracownia Zielnik. `glos-marki/korpus/` = 8 tekstów, `glos-marki/brief.md` = słownik. Oczekiwany profil ≈ `skills/straznik-glosu-marki/examples/glos-przykladowy.md`.

## Ekstrakcja

| Przypadek | Wejście | Oczekiwane |
|---|---|---|
| (h) pełny korpus | 8 tekstów + brief | glos.md ze statusem "wstępny" (5-9 tekstów), per Ty, półpauza "–" jako myślnik (z liczbą), emoji 0, otwarcia sytuacją, "bez pytań" i "w dniu roboczym" firmowe, "rewolucyjny" zakazane potwierdzone przez nieobecność, "produkt" jako "z briefu, nie widziane w korpusie" |
| (i) 4 teksty | tylko 01-04 | glos.md ze statusem "za mało danych" + ostrzeżenie |
| (j) sekcja ręczna | istniejący glos.md z wpisem w sekcji 9, ponowna ekstrakcja | sekcja 9 przeniesiona znak w znak |
| (k) brief vs korpus | brief zakazuje słowa, którego korpus używa | oba fakty w profilu, decyzja zostawiona w sekcji 9 |

## Walidacja (profil = glos-przykladowy.md)

| Przypadek | Plik | Oczekiwane |
|---|---|---|
| (a) zgodny | teksty/a_zgodny.md | 8 z 8 PASS, cytat przy każdym punkcie, werdykt "do publikacji" |
| (b) pauza długa | teksty/b_pauza-dluga.md | NIE w 7a z cytatem "—" i cytatem z profilu; reszta PASS; "do poprawek" |
| (c) półpauza | teksty/a_zgodny.md | PASS w 7a (półpauza zgodna z profilem) - ten sam plik co (a) |
| (d) kontrast binarny | teksty/d_kontrast-binarny.md | NIE w 7b, wzorzec "kontrast binarny", cytat "To nie jest mniejsza sadzonka. To sadzonka..." |
| (e) słowo zakazane | teksty/e_slowo-zakazane.md | NIE w 4, dwa cytaty (tekst: "rewolucyjny", profil: wpis) |
| (f) przynęta | teksty/f_przyneta.md | 3+ NIE (co najmniej 1, 4, 5, 7a, 7b), werdykt "do przepisania od nowa" |
| (g) bez propozycji | każdy z powyższych | raport nie zawiera "lepiej byłoby", "proponuję", ani wariantu zdania |

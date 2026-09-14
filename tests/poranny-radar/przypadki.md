# Przypadki testowe: poranny-radar

Fixture: fikcyjna firma Pracownia Zielnik. `radar/zrodla/mailing.csv` = 12 kampanii o zaplanowanych cechach: tematy z liczbą mają wyraźnie wyższe kliknięcia (#13, #15, #18, #22: 4,6-5,3% wobec 2,3-2,6%), #19 ma wypisy powyżej normy (19 przy medianie 5), #23 ma załamanie otwarć (19,3% przy medianie 33,6%, wysłana w sobotę). `sprzedaz.csv` = 5 tygodni z pikiem w tygodniach wyprzedaży. `skrzynka.md` = 3 zobowiązania. `wnioski.md` = stan "tydzień później" z 3 wnioskami.

## Skrypt (deterministyczny)

| Przypadek | Wejście | Oczekiwane |
|---|---|---|
| (a) kolumny po polsku | mailing.csv | `kolumny` mapuje wszystkie 7 pól, 12 kampanii, procenty policzone z liczb (np. #13: 37,2% otwarć, 4,62% kliknięć) |
| (b) sygnały | mailing.csv | w `sygnaly`: #19 wypisy (19 przy medianie 5), #23 otwarcia (19,32% przy 33,64%), kliknięcia #13, #15, #18, #21, #22 jako "zaskoczylo" |
| (c) hipoteza liczby | mailing.csv | `temat_z_liczba.potwierdza` = true, z liczbą 6 kampanii, bez 6 |
| (d) okno | `--do 2026-09-05` | 11 kampanii, brak sygnału o #23 |
| (e) wnioski z pliku | `--wnioski wnioski.md` | 3 wpisy z licznikami 3, 1, 2 |
| (f) brak kolumn | CSV bez kolumny wysłanych | kod 2, `brak_kolumn` z listą |

## Brief (agent ze skillem)

| Przypadek | Oczekiwane |
|---|---|
| (g) trzy zadania z liczbą | dokładnie 3 punkty, każdy z liczbą ze skryptu; jedno o dniu wysyłki albo o #23, jedno o wyprzedaży albo temacie z liczbą |
| (h) traci / zaskoczyło | "Traci" o #23 (otwarcia) albo #19 (wypisy); "Zaskoczyło" o kliknięciach wyprzedaży, z kampanią, wartością i medianą |
| (i) pamięć cytowana | wszystkie 3 wnioski z `wnioski.md` dosłownie z licznikami; "Temat z liczbą klika lepiej" podniesiony do 4+ (bo #22 "Ostatnie 3 dni" potwierdza) albo uzasadnione pozostawienie |
| (j) nowy wniosek | dopisany wniosek o sobotniej wysyłce albo o #23 jako hipoteza (1-2 obserwacje), nic nie skasowane |
| (k) klocki | linia o sprzedaży (11 545 zł, 77 zamówień, pik w tygodniach wyprzedaży) i o skrzynce (3 terminy, bez nadawców) |
| (l) język | bez CTR/OR/CSV/JSON w tekście, krótki myślnik, brak adresów e-mail |

## Dwa briefy obok siebie (demo)

Brief 1 na `--do 2026-09-05` z pustym `wnioski.md`: pamięć pusta, wnioski zapisane na start. Brief 2 na pełnym oknie z `wnioski.md` z fixture: cytuje wnioski, łapie #23. Różnica między nimi = dowód, że agent się uczy.

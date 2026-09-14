# Przypadki testowe: czujka

Fixture: fikcyjna firma Pracownia Zielnik, `czujka/config.md` z 2 stronami i 1 kontem reklamowym, `czujka/snapshoty/` = stan z "poprzedniego dnia". `nowy-stan/` = to, co czujka "pobrała" dziś (w teście podkładamy pliki zamiast Firecrawl: powiedz agentowi, że pobranie ma wziąć z `nowy-stan/<etykieta>.md`). Oczekiwany raport ≈ `skills/czujka/examples/raport-przykladowy.md` w formie, nie w treści.

## Sprawdzenie

| Przypadek | Wejście | Oczekiwane |
|---|---|---|
| (a) zmiana istotna | Ogrody Jaśmin: snapshot "lista oczekujących", nowy stan "zapisy otwarte", cena 990 zł | sekcja Istotne z "było -> jest" dla statusu i ceny, po jednym zdaniu znaczenia, cena z kwotą |
| (b) sam szum | Zielnik - sklep: różni się tylko odliczanie (46 vs 45 dni) i opinia w karuzeli | Zielnik w "Bez istotnych zmian", odliczanie i opinia w Drobiazgach, zero zdań znaczenia |
| (c) nowe reklamy | Szkółka Modrzew: snapshot 3 identyfikatory, nowy stan 4 (jeden nowy, jeden zakończony) | "Nowe reklamy (1)" z datą i pierwszym zdaniem, "Zakończone: 1", w Istotne |
| (d) padnięty cel | `nowy-stan/ogrody-jasmin.md` zastąpiony plikiem z jedną linią "BŁĄD: przekroczony czas" | Ogrody Jaśmin w "Nie udało się sprawdzić", reszta raportu normalna, snapshot Ogrodów nietknięty |
| (e) baza | usunięte `snapshoty/` | raport ma "Stan wyjściowy" z linią na cel, zero zmian, zdanie "porównania zaczną się od następnego sprawdzenia" |
| (f) bez żargonu | każdy z powyższych | w raporcie brak słów scrape, diff, snapshot, DOM, brak adresów e-mail |
| (g) typografia | każdy z powyższych | krótki myślnik, "->" tylko przy było/jest, zero "—" i "–" poza cytatami ze stron |

## Dodanie

| Przypadek | Wejście | Oczekiwane |
|---|---|---|
| (h) nowa strona | "obserwuj też https://ogrody-lipa.example, ważna cena" | wpis w sekcji Strony z etykietą, adresem, "cena" w Ważne; potwierdzenie jednym zdaniem; pytanie o pierwsze pobranie |
| (i) osoba prywatna | "obserwuj też profil Jana Kowalskiego" | odmowa jednym zdaniem: czujka jest do firm i stron; brak wpisu |

## Konfiguracja

| Przypadek | Wejście | Oczekiwane |
|---|---|---|
| (j) od zera | brak folderu, `/czujka` | pytanie K1 (jedna firma czy agencja), jedno pytanie naraz, po K2 i K3 tabela config.md z wpisami |
| (k) powrót | config.md z K1-K3 gotowe, K4 do zrobienia, "wróćmy do konfiguracji czujki" | jedno zdanie podsumowania stanu i od razu K4 (baza), bez powtarzania pytań K1-K3 |

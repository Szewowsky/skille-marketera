# Przypadki testowe: grupy-fb

Fixture: fikcyjna firma Pracownia Zielnik. `grupy-fb/config.md` (1 grupa, 3 frazy marki), `grupy-fb/widziane.json` (1 post już widziany: 9002), `posty-surowe.json` = 8 syntetycznych postów w formacie aktora Apify, z pełnymi nazwiskami i identyfikatorami użytkowników. W teście skrypt uruchamiamy z `--z-pliku posty-surowe.json` zamiast Apify. `posty-duplikat.json` to ta sama fixture rozszerzona o drugą grupę: dwie kopie postów 9004 i 9005 (ten sam tekst, inny adres) i jeden post, w którym ktoś pokazuje własne rozwiązanie i tag'uje dwie osoby.

## Skrypt (deterministyczny)

| Przypadek | Oczekiwane |
|---|---|
| (a) anonimizacja | w wyjściu zero pełnych nazwisk z fixture (Wiśniewska, Kowalczyk, Lewandowska, Wójcik, Szymański, Krawczyk, Piotrowski, Zieliński, Dąbrowski, Jabłońska, Kamiński, Grabowska), zero pól `user.id`; autor "Marta W.", jednowyrazowy "Bartek" bez zmian |
| (b) widziane | post 9002 pominięty, `pominiete_widziane` = 1, `nowe` = 7 |
| (c) wzmianki | 9003 (link do kanału) i 9006 ("Pracownię Zielnik", odmiana) mają niepuste `wzmianki_marki`; `wzmianki_marki` = 2 |
| (d) brak tokena | bez `--z-pliku` i bez `APIFY_API_TOKEN` skrypt kończy się kodem 2 i JSON-em z `brak_tokena` |
| (e) oznaczanie | z `--oznacz-widziane` plik `widziane.json` ma 8 adresów, `statystyki.runy` = 2 (uruchamiaj na kopii fixture) |
| (n) krok 7 z pliku wyjściowego | run z `--z-pliku posty-surowe.json --wyjscie w.json`, potem `--z-pliku w.json --oznacz-widziane` (bez adresów grup) kończy się bez błędu, `nowe` = 7, `widziane.json` ma 8 adresów |
| (o) koszt prawdziwego runu | gdy plik z `--wyjscie` ma `run.koszt_usd` = 0.151, po oznaczeniu `statystyki.koszt_usd` rośnie o 0.151 (nie zostaje 0.0) |
| (p) drugi przebieg | ta sama fixture puszczona jeszcze raz na zapisanym `widziane.json` daje `nowe` = 0 |
| (q) dedup po treści | `posty-duplikat.json` (11 itemów: 8 z fixture, 2 kopie postów 9004 i 9005 w drugiej grupie, 1 post własny) daje `nowe` = 8, `duplikaty_tresci` = 2; posty 9004 i 9005 mają `kopie` = 2 i dwie nazwy w `takze_w_grupach`; po oznaczeniu adresy kopii też trafiają do `widziane.json` |
| (r) otagowane osoby | w `posty-duplikat.json` post własny i jego komentarz mają "@Karol Wielgus" i "@Iwona Dąbrowska" w treści, w wyjściu "@[osoba]"; fraza marki `youtube.com/@pracownia-zielnik` zostaje nietknięta |

## Raport (agent ze skillem, wejście = wyjście skryptu)

| Przypadek | Oczekiwane |
|---|---|
| (f) wzmianki na górze | sekcja "Wzmianki o marce" z dwoma wpisami: 9003 ton "poleca", 9006 ton "pyta"; każdy z adresem posta i "co zrobić"; 9006 nie wraca w "O co pytają" |
| (g) przesiew | 9002 nieobecny (widziany); 9007 (mem) w "Pominięte", nie w tematach; 9001, 9004, 9005, 9008 w "O co pytają" albo "Na co narzekają" |
| (h) narzekanie | 9005 (teksty z ChatGPT od klientów) w "Na co narzekają" z komentarzem o przycisku LinkedIn jako najlepszą odpowiedzią |
| (i) prywatność | raport nie zawiera żadnego pełnego nazwiska ani `facebook.com/profile`; autorzy jako "Imię N." |
| (j) liczby | "Nowych postów: 7 (pominięto 1)", koszt 0 USD (z pliku), zasięgi zgodne z fixture (np. 9005: 33 polubienia, 21 komentarzy) |
| (k) typografia | krótki myślnik, zero "—", zero słów scrape / dedup / JSON w raporcie |
| (s) co pokazują | z `posty-duplikat.json`: post z arkuszem liczącym marżę stoi w sekcji "Co pokazują", nie w "O co pytają" ani w "Pominiętych"; posty 9004 i 9005 mają dopisek "w 2 grupach" i liczą się jako jedna osoba |

## Dodanie

| Przypadek | Oczekiwane |
|---|---|
| (l) nowa grupa | "obserwuj też https://www.facebook.com/groups/400500600" → wiersz w tabeli Grupy, potwierdzenie, pytanie o sprawdzenie od razu |
| (m) nazwa bez adresu | "obserwuj też grupę Marketing Polska" → prośba o adres, brak wpisu |

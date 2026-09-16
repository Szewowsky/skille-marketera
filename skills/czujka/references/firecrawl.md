# Pobieranie: Firecrawl, strony i Meta Ads Library

Czujka czyta stan strony tak, jak widzi go człowiek: po wykonaniu skryptów, bez ukrytych elementów. Dlatego pobiera przez Firecrawl (wyrenderowany DOM), nie przez `curl` ani `requests`. Powód z praktyki: strony na Webflowie trzymają w kodzie przekreśloną cenę i pasek promocji z `display:none` oraz placeholdery liczników ("47d 7h 44m"), które podmienia skrypt. Czujka na surowym HTML raportuje zmiany, których nie ma, i przegapia te, które są.

## Klucz

Klucz Firecrawl w zmiennej `FIRECRAWL_API_KEY` (plik `.env` projektu albo sejf systemowy użytkownika). Sprawdzenie: `firecrawl --status` mówi "authenticated" albo nie. Bez klucza działa tryb bez logowania (rate-limit) dla `scrape`; `monitor` wymaga klucza. Gdy klucza nie ma, powiedz to użytkownikowi jednym zdaniem i zaproponuj `firecrawl login` (otwiera przeglądarkę, użytkownik loguje się sam). Nigdy nie wpisuj klucza do plików repo ani do `config.md`.

Gdy CLI nie ma: `npx -y firecrawl-cli@latest <komenda>` działa bez instalacji. Gdy w narzędziach jest MCP Firecrawl, użyj jego narzędzia scrape z tymi samymi parametrami.

## Strona: pobranie stanu

```bash
firecrawl scrape "<adres>" --only-main-content --wait-for 3000 --max-age 0 -f markdown -o czujka/snapshoty/_surowe/<etykieta>.md
```

- `--wait-for 3000`: daje skryptom czas na podmianę liczników i cen. Przy stronach z odliczaniem to jest różnica między placeholderem a prawdziwą wartością.
- `--max-age 0` wymusza świeże pobranie; bez tej flagi Firecrawl oddaje zapamiętaną wersję z poprzedniego sprawdzenia i porównanie pokazuje zero zmian, których nie ma (sygnał ostrzegawczy: odliczanie stoi na tej samej sekundzie co poprzednio).
- `--only-main-content`: bez nawigacji i stopki. Na stronach Webflow flaga często prawie nic nie ucina (sprawdzone: 118 KB z flagą vs 121 KB bez), więc drugie pobranie bez flagi rób tylko wtedy, gdy w pierwszym brakuje ceny albo statusu, nie profilaktycznie.
- Wynik to markdown widocznego tekstu. Z niego wyciągasz stan (SKILL.md, Sprawdzenie krok 3) i zapisujesz jako `snapshoty/<etykieta>.md`. Surowy markdown możesz trzymać w `snapshoty/_surowe/` do podglądu, ale porównujesz stan, nie surowy tekst: diff na surowym tekście to szum.
- Padnięcie: kod inny niż 200, pusty markdown, komunikat o blokadzie. Zapisz "nie udało się sprawdzić" i idź dalej. Jeden ponowny spróbowanie po 10 sekundach, nie więcej.

Format `changeTracking` (`-f markdown,changeTracking`) daje gotową informację, czy strona zmieniła się od poprzedniego pobrania tym samym kluczem. Możesz go użyć jako pierwszego filtra ("nic się nie zmieniło" = od razu drobiazgi), ale klasyfikację i "było -> jest" robisz na własnym stanie.

## Meta Ads Library: konto reklamowe

Meta Ads Library jest publiczna: pokazuje aktywne reklamy każdej strony na Facebooku i Instagramie, bez logowania. Strona jest ciężka i ładuje reklamy skryptem, więc pewniejsza droga to gotowy aktor Apify, a Firecrawl jest zapasem.

**Droga główna: Apify.** Aktor `igolaizola/facebook-ad-library-scraper` (REST, token w `APIFY_API_TOKEN`, plan Free wystarcza na kilka kont dziennie). Wejście: adres Ads Library z `view_all_page_id` (niżej) albo `page_id` + kraj, limit 100 reklam. Uruchomienie gotowym skryptem tego skilla `scripts/reklamy.py` (POST run, odpytywanie statusu, pobranie datasetu, grupowanie po treści kreacji): `APIFY_API_TOKEN=$(security find-generic-password -a APIFY_API_TOKEN -s <usługa> -w) python3 .claude/skills/czujka/scripts/reklamy.py --page-id <id strony> --wyjscie czujka/snapshoty/_surowe/<etykieta>-reklamy.json`. Opis wejścia do aktora jest w skrypcie i nie należy go układać od nowa: pierwsze pobranie z wejściem ułożonym z pamięci wróciło puste. Z wyniku bierzesz: identyfikator reklamy, datę startu, platformy, treść (pierwsze zdanie), wezwanie, link docelowy. Porównuj po treści kreacji (treść + wezwanie + link), nie po samych identyfikatorach: przy limicie 100 identyfikatory rotują i dają fałszywe "nowe". Aktor zwraca reklamy od najnowszych (`sortBy: mostRecent`), więc gdy wróci dokładnie tyle reklam, ile wynosi `maxItems`, lista jest ucięta od dołu i poza nią zostają NAJSTARSZE reklamy: zapisz w snapshocie ostrzeżenie "lista ucięta, najstarsza widoczna z <data>", starszych reklam z poprzedniego snapshotu nie oznaczaj jako zakończone (mogły wypaść za limit), a przy następnym sprawdzeniu podnieś limit do 200 (koszt aktora rośnie mniej więcej dwukrotnie, dziś rzędu kilku groszy). Brak tokena albo 401/403 = "nie udało się sprawdzić" z powodem, nie cisza.

**Zapas: Firecrawl na stronie Ads Library.** Adres wyszukiwania po nazwie:

```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=PL&q=<nazwa firmy>&search_type=keyword_unordered&media_type=all
```

Lepszy, stabilny adres po identyfikatorze strony (gdy go znasz albo znajdziesz w wyniku wyszukiwania jako `view_all_page_id`):

```
https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=PL&view_all_page_id=<ID>&media_type=all
```

Pobranie:

```bash
firecrawl scrape "<adres Ads Library>" --wait-for 5000 --max-age 0 -f markdown -o czujka/snapshoty/_surowe/<etykieta>-reklamy.md
```

Strona ładuje reklamy skryptem, stąd dłuższe czekanie. Ze zrzutu wyciągnij listę reklam: identyfikator z biblioteki (numer przy "Identyfikator z biblioteki" albo "Library ID"), datę startu ("Rozpoczęto wyświetlanie" albo "Started running on"), platformy, pierwsze zdanie treści. Stan konta = ta lista. Porównanie: identyfikatory nowe = nowe zestawy, identyfikatory, których nie ma = zakończone. Zmiana treści przy tym samym identyfikatorze = zmiana przekazu.

Gdy strona zwraca pustą listę, a wcześniej były reklamy, to może być blokada, nie koniec kampanii: zapisz "nie udało się sprawdzić" zamiast "wszystkie reklamy zakończone", i powiedz to użytkownikowi.

Ekstrakcja strukturalna, gdy zrzut jest długi: `--schema` z polami `ads[]: {library_id, started, platforms, first_sentence}` zwraca JSON zamiast markdownu. Użyj, gdy w zrzucie jest więcej niż 20 reklam.

## Monitor: rutyna po stronie Firecrawl

Gdy użytkownik wybierze drogę Firecrawl monitor, jedno polecenie na zestaw stron:

```bash
firecrawl monitor create --name "Czujka: <nazwa zestawu>" \
  --scrape-urls "<adres1>,<adres2>,<adres3>" \
  --schedule "every day at 7:30" --timezone "Europe/Warsaw" \
  --goal "<cel po polsku>" \
  --email "<adres użytkownika>"
```

Cel dla sędziego AI piszesz po polsku z notatek "ważne" i z reguł raportu, na przykład: "Powiadom, gdy zmieni się status zapisów, cena albo cokolwiek wokół ceny, daty startu, nagłówek główny, lista sekcji, prowadzący albo liczba absolwentów. Odliczanie czasu, rotujące opinie i data w stopce to nie są zmiany." Osobny monitor na adresy Ads Library z celem "Powiadom o nowych albo zakończonych reklamach i zmianie ich treści".

Zapisz identyfikator monitora (`mon_...`) w `config.md` w Ustawieniach. Sprawdzenie stanu: `firecrawl monitor checks <id> --limit 5`. Wstrzymanie: `firecrawl monitor update <id> --state paused`. Adres e-mail użytkownika trafia tylko do polecenia, nie do plików repo.

Monitor i gałąź Sprawdzenie mogą działać obok siebie: monitor budzi mailem, Sprawdzenie robi raport w naszym formacie i archiwum.

---
name: poranny-radar
description: "Poranny brief marketera z eksportu mailingowego i klocków (sprzedaż, skrzynka): trzy rzeczy do zrobienia dziś, co traci, co zaskoczyło, wnioski z pamięcią liczoną w obserwacjach. Use when: 'zrób brief', 'co dziś', 'poranny radar', 'co pamiętasz o kampaniach', 'skonfiguruj radar', 'dołóż klocek'."
compatibility: Claude Code i Codex. Liczby liczy skrypt w scripts/ (Python 3 bez zależności). Rutyna: zadanie cykliczne agenta.
---

# Poranny radar

Brief, nie raport. Rano czyta dane, które marketer i tak ma (eksport z narzędzia mailingowego, sprzedaż, skrzynka), i mówi, co robić dziś. Dwie rzeczy, których czat nie zrobi: odpala się sam i pamięta. Każdy wniosek żyje w pliku z licznikiem obserwacji, a kolejny brief cytuje go z powrotem.

## Folder

Jeden folder = jeden zestaw źródeł (agencja: `radar-<klient>/`).

```
radar/
├── config.md         # źródła, kadencja, stan konfiguracji
├── zrodla/           # mailing.csv (rdzeń) + klocki: sprzedaz.csv, skrzynka.md, youtube.csv ...
├── wnioski.md        # pamięć: jedna linia na wniosek, licznik obserwacji, przykład
├── policzone/        # wynik skryptu z każdego briefu (JSON)
└── briefy/           # YYYY-MM-DD_brief.md
```

## Która gałąź

- `/poranny-radar` bez treści, "skonfiguruj radar", brak folderu → **Konfiguracja** (`references/konfiguracja.md`): pięć kroków, jedno pytanie naraz, stan w `config.md`.
- "Zrób brief", "co dziś", "poranny radar" → **Brief**.
- "Dołóż klocek", "podpiąłem sklep", "dodaj skrzynkę" → **Klocek**: zapytaj, gdzie jest plik albo źródło, sprawdź, że da się go odczytać, dopisz do sekcji Źródła w `config.md` z rolą jednym zdaniem ("sprzedaż: czy po kampanii coś wpadło"). Następny brief go uwzględnia.
- "Co pamiętasz", "jakie masz wnioski" → przeczytaj `wnioski.md` i odpowiedz z liczbami obserwacji, bez liczenia od nowa.
- "Załóż rutynę", "co poniedziałek" → **Rutyna**.

## Brief

Format i reguły: `references/brief.md`. Przeczytaj przed pierwszym briefem w sesji.

1. Przeczytaj `config.md`: źródła, ich role, kadencja, data ostatniego briefu. Gdy folder ze źródłami istnieje, a `config.md` nie: wywnioskuj role z nazw plików (mailing = rdzeń, sprzedaz = sklep, skrzynka = zobowiązania), zrób brief i zaproponuj dopisanie `config.md` jednym zdaniem.
2. Uruchom skrypt na eksporcie mailingowym z klockami, które są plikami:
   ```bash
   python3 .claude/skills/poranny-radar/scripts/policz.py radar/zrodla/mailing.csv \
     --wnioski radar/wnioski.md --sprzedaz radar/zrodla/sprzedaz.csv \
     --wyjscie radar/policzone/YYYY-MM-DD.json
   ```
   Skrypt zwraca: kampanie z procentami (kropka dziesiętna, w tekście briefu zamieniasz na przecinek, w tabeli możesz zostawić), średnie i mediany, sygnały (otwarcia poniżej 80% mediany, kliknięcia powyżej 150% mediany, wypisy powyżej 250% mediany), hipotezy wbudowane (temat z liczbą, dzień wysyłki) i wnioski wczytane z pliku. Domyślnie ostatnie 12 kampanii: napisz to w nagłówku briefu ("okno: ostatnie 12 kampanii"). Ścieżka skryptu w poleceniu jest względna do projektu użytkownika; uruchamiaj z korzenia projektu albo podaj ścieżkę bezwzględną. `brak_kolumn` = powiedz użytkownikowi, których kolumn brakuje, i poproś o eksport na poziomie kampanii. W Codex ścieżka to `.agents/skills/poranny-radar/scripts/policz.py`.
3. Klocki, które nie są CSV (skrzynka jako notatka, źródło przez narzędzie w Twoim zestawie): odczytaj je osobno. Skrzynka: wyciągnij zobowiązania z terminem, bez adresów nadawców i bez cytowania treści maili. Źródło niedostępne = jedna linia "nie udało się odczytać: <klocek>" w briefie, reszta powstaje normalnie.
4. Wnioski: dla każdego wpisu z `wnioski.md` sprawdź tylko na kampaniach nowszych niż data ostatniego briefu (z `config.md`; gdy jej nie ma, nowsze niż data "od" wniosku i nieobecne w jego przykładach), czy potwierdza, zaprzecza, czy nie dotyczy. Dzięki temu ta sama kampania nie podnosi licznika dwa razy. Potwierdza = podnieś licznik obserwacji o 1 i dopisz przykład. Zaprzecza = dopisz "(zaprzeczenie: <kampania>)" i nie podnoś. Nie dotyczy = dopisz albo zaktualizuj "(sprawdzono: <data>)", żeby było widać, jak długo hipoteza czeka. Nowy wzorzec widoczny w sygnałach albo hipotezach skryptu, którego nie ma w pliku = dopisz jako nowy wniosek z obserwacjami równymi liczbie kampanii, które go pokazują. Nie kasujesz wpisów, to robi człowiek.
5. Napisz brief według szablonu: trzy rzeczy do zrobienia dziś (każda z liczbą, z której wynika), co traci i co zaskoczyło (po jednym zdaniu, z sygnałów skryptu), co pamiętam (najwyżej 5 wniosków: te, które dotyczą dzisiejszych zadań, potem najwyższe liczniki; reszta zostaje w pliku), z innych klocków (jedna linia na klocek), tabela kampanii na końcu.
6. Zapisz `briefy/YYYY-MM-DD_brief.md`, zaktualizuj `wnioski.md`, wpisz datę briefu do `config.md` ("Ostatni brief"), pokaż brief w całości. Przejdź `eval.md`.

Tryb "tydzień później" (demo, porównanie dwóch briefów): `--do <data>` w skrypcie ogranicza okno do kampanii do tej daty. Pierwszy brief na oknie starszym, drugi na pełnym, obok siebie.

## Rutyna

Po pierwszym briefie zaproponuj jednym zdaniem: "mam odpalać to sam w poniedziałek o 7:30?". Zapisz wybór w `config.md`. Claude Code: scheduled task z poleceniem "zrób brief"; Codex: cron. Jedno uczciwe zdanie: skill jest ten sam, harmonogram jest per narzędzie. Eksport mailingowy musi być odświeżony przed rutyną (ręcznie albo przez narzędzie, które użytkownik ma; skill sam nie loguje się do narzędzia mailingowego).

## Prywatność

Dane wchodzą na poziomie kampanii: nazwa, temat, data, liczby. Żadnych adresów e-mail, nazwisk subskrybentów, list odbiorców, treści maili. Gdy eksport zawiera kolumny z adresami (eksport subskrybentów zamiast kampanii), zatrzymaj się i poproś o eksport kampanii. Skrzynka: zobowiązania i terminy tak, nadawcy i treść nie.

## Po robocie

Cała odpowiedź krótkim myślnikiem "-". Brief po polsku, bez żargonu (bez CTR, OR, CSV w tekście briefu: pisz "kliknięcia", "otwarcia", "eksport"). Zawsze `eval.md` przed pokazaniem.

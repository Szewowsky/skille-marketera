# Inwentarz: gdzie każdy skill trzyma stan

Ścieżki względne do korzenia projektu użytkownika (tam, gdzie `.claude/`). W Codex skille leżą w `.agents/skills/` zamiast `.claude/skills/`, reszta bez zmian. Agencja: folder z przyrostkiem `-<klient>` per klient, tabela gotowości dostaje jeden wiersz na folder.

| Skill | Folder skilla | Plik stanu | Kroki w tabeli | Klucz | Sprawdzenie klucza |
|---|---|---|---|---|---|
| straznik-glosu-marki | `.claude/skills/straznik-glosu-marki/` | `glos-marki/config.md` | 6 (K1 Marka ... K6 Gotowe) | nie dotyczy | - |
| poranny-radar | `.claude/skills/poranny-radar/` | `radar/config.md` | 5 (K1 Zestaw ... K5 Kadencja) | nie dotyczy (eksport CSV od użytkownika) | - |
| grupy-fb | `.claude/skills/grupy-fb/` | `grupy-fb/config.md` | 6 (K1 Temat ... K6 Kadencja) | `APIFY_API_TOKEN` | `python3 -c "import os;print('jest' if os.environ.get('APIFY_API_TOKEN') else 'brak')"` |
| czujka | `.claude/skills/czujka/` | `czujka/config.md` | 5 (K1 Zestaw ... K5 Kadencja) | Firecrawl (logowanie CLI albo `FIRECRAWL_API_KEY`); Meta Ads dodatkowo `APIFY_API_TOKEN` | `firecrawl --status` (albo `npx -y firecrawl-cli@1.23.3 --status`): linia "Authenticated" = jest; plus sprawdzenie Apify jak wyżej, gdy w `config.md` jest sekcja Reklamy z wpisami |

Tabela kroków w każdym `config.md` ma trzy kolumny: Krok, Stan, Notatka. Stany: `do zrobienia`, `w toku`, `gotowe`, `pominięte` (liczy się jak gotowe). Skill jest `gotowy`, gdy każdy wiersz ma `gotowe` albo `pominięte`; `nie zaczęty`, gdy pliku stanu nie ma; `w toku`, gdy plik jest, a któryś wiersz nie ma tych stanów (pierwszy taki wiersz = następny krok; gdy ma stan `w toku` z notatką, skill czeka na to, co notatka opisuje, np. "po pierwszym porównaniu", i to idzie do zdania "następny ruch"; `w toku` bez notatki = zdanie z nazwy kroku, np. "dokończymy krok Klucz").

Gdy folder stanu istnieje, a `config.md` w nim nie ma (ktoś założył folder ręcznie): stan `nie zaczęty`, w następnym ruchu powiedz, że folder jest i konfiguracja go użyje.

## Wspólne

- Python 3: `python3 --version`. Potrzebny skryptom radaru (`policz.py`) i grup (`pobierz.py`). Brak = radar i grupy dostają w tabeli dopisek "wymaga Pythona 3".
- `.gitignore`: gdy `git rev-parse --is-inside-work-tree` odpowiada `true`, sprawdź wpisy: `/glos-marki*/**`, `/czujka*/**`, `/grupy-fb*/**`, `/radar*/**`, `.env`, `.firecrawl/` (ta sama lista co w `INSTALACJA.md` repo). Brak wpisu = jedna linia pod tabelą z propozycją dopisania; dopisz po zgodzie użytkownika.
- Przeglądarka w narzędziach agenta: potrzebna strażnikowi, gdy teksty marki mają być zebrane ze strony www (K2). Bez przeglądarki strażnik prosi o wklejenie tekstów, więc to nie blokuje, tylko wydłuża.

## Na co dzień

Zdania do pokazania, gdy wszystko jest `gotowe`:

- Strażnik: "Sprawdź ten tekst" z wklejonym tekstem; "Wyprowadź głos marki" po dołożeniu tekstów do korpusu.
- Radar: "Zrób brief" po wgraniu świeżego eksportu kampanii; "Co pamiętasz o kampaniach".
- Grupy: "Co nowego w grupach"; "Obserwuj też grupę <adres>"; "Czy ktoś o nas pisze".
- Czujka: "Co się zmieniło u obserwowanych"; "Obserwuj też <adres>"; po pierwszym porównaniu "Załóż rutynę".

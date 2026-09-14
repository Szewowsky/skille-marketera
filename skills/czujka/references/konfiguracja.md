# Konfiguracja krok po kroku

Prowadzi od zera do pierwszej bazy. Stan w `czujka/config.md`, więc można przerwać po dowolnym kroku i wrócić: skill czyta plik i idzie od pierwszego kroku bez `gotowe`.

Zasada: jedno pytanie naraz, po polsku, bez flag i ścieżek w pytaniach. Użytkownik odpowiada zdaniem, skill sam zapisuje. Po każdym kroku aktualizuj `config.md` i powiedz jednym zdaniem, co dalej.

Stany kroków: `do zrobienia`, `w toku`, `gotowe`, a K2 i K3 mogą mieć `pominięte` (liczy się jak gotowe, ale przynajmniej jedna z sekcji Strony albo Reklamy musi mieć wpisy). Powrót = pierwszy krok, który nie jest `gotowe` ani `pominięte`.

**Przerwanie.** Gdy użytkownik mówi "muszę kończyć" albo przestaje odpowiadać: zapisz bieżący krok jako `w toku` z notatką i powiedz: "Stan zapisany w czujka/config.md. Wróć słowami: wróćmy do konfiguracji czujki."

## Kroki

**K1 Zestaw.** Zapytaj, czy czujka ma pilnować jednej firmy (własne strony i rynek razem), czy kilku klientów (agencja). Jedna: folder `czujka/`. Kilka: `czujka-<klient>/` per klient. Utwórz folder w korzeniu projektu (tam, gdzie `.claude/`), z `snapshoty/`, `raporty/` i `config.md` z szablonu niżej. Gdy projekt jest w gicie, sprawdź, że `.gitignore` ma `/czujka*/**` (snapshoty i surowe zrzuty nie do historii) i `.firecrawl/` (podręczna pamięć CLI); brakujące dopisz. Folder z zawartością: nie twórz nowego, powiedz co w nim jest i idź dalej.

**K2 Strony.** Zapytaj, jakie adresy obserwować i co u każdego jest ważne (cena? status zapisów? nagłówek? nowe sekcje?). Przyjmij adresy jeden po drugim albo listą. Dla każdego: jedno pobranie, żeby potwierdzić, że strona odpowiada, etykieta (nazwa firmy albo programu), notatka "ważne". Podpowiedz, że własne strony też warto pilnować: po wdrożeniu ktoś urywa przycisk, countdown zamiera, cena rozjeżdża się między stroną i cennikiem. Gdy użytkownik podaje osobę zamiast firmy, powiedz, że czujka jest do firm i stron, i poproś o adres firmowy. "Nie mam" albo "tylko reklamy" = `pominięte`.

**K3 Reklamy.** Zapytaj, których firm reklamy w Meta Ads Library obserwować. Przyjmij nazwę firmy albo adres jej strony na Facebooku; znajdź identyfikator strony przez Ads Library (`references/firecrawl.md`, sekcja Meta Ads Library) i zapisz adres wyszukiwania w konfiguracji. Zapytaj o kraj (domyślnie PL). "Nie mam" = `pominięte`.

**K4 Baza.** Uruchom gałąź Sprawdzenie na całym `config.md`. To pierwsze pobranie, więc raport mówi tylko "stan wyjściowy zapisany", per cel, z jedną linią, co odczytano (nagłówek, cena, status). Pokaż, ile celów udało się pobrać, a ile nie. Zapytaj, czy coś dopisać do notatek "ważne".

**K5 Kadencja.** Zapytaj, czy sprawdzać codziennie rano, czy co tydzień, i którą drogą (Firecrawl monitor z mailem albo zadanie cykliczne agenta, opis w SKILL.md sekcja Rutyna). Zapisz wybór. Jeśli użytkownik chce najpierw zobaczyć jedno prawdziwe porównanie, oznacz `w toku` z notatką "po pierwszym porównaniu" i wróć do tego kroku po następnym sprawdzeniu. Zapisz datę ukończenia.

## Szablon config.md

```markdown
# Czujka: <nazwa zestawu>

Utworzono: <data>. Ostatnia zmiana: <data>. Ostatnie sprawdzenie: <data albo "jeszcze nie">.
Tryb: jedna firma / agencja (folder: <ścieżka>)

| Krok | Stan | Notatka |
|---|---|---|
| K1 Zestaw | do zrobienia | <nazwa> |
| K2 Strony | do zrobienia | <liczba> adresów |
| K3 Reklamy | do zrobienia | <liczba> kont |
| K4 Baza | do zrobienia | <data pierwszego pobrania> |
| K5 Kadencja | do zrobienia | <codziennie/co tydzień, droga> |

## Strony

| Etykieta | Adres | Ważne | Uwagi |
|---|---|---|---|
| <nazwa> | https://... | cena, status zapisów | własna strona / rynek |

## Reklamy (Meta Ads Library)

| Etykieta | Adres wyszukiwania w Ads Library | Kraj | Ważne |
|---|---|---|---|
| <nazwa> | https://www.facebook.com/ads/library/?... | PL | nowe zestawy, zmiana przekazu |

## Ustawienia
- Kadencja: <codziennie 7:30 / co tydzień pon 8:00>
- Droga: <Firecrawl monitor (e-mail: ...) / zadanie cykliczne agenta>
- Zawsze na górze raportu: status zapisów, cena, daty, nagłówek, sekcje, ludzie, liczniki, reklamy nowe i zakończone
- Zawsze w drobiazgach: odliczanie czasu, rotujące opinie, data w stopce, drobne przeredagowania
```

## Powrót

Gdy użytkownik mówi "wróćmy do konfiguracji czujki", "dokończmy", "gdzie skończyliśmy" albo wywołuje skill bez treści, a `config.md` ma krok bez `gotowe`: podsumuj tabelę w jednym zdaniu ("Strony są, reklam brak, bazy jeszcze nie ma") i idź od tego kroku. Nie pytaj o to, co już jest w tabeli.

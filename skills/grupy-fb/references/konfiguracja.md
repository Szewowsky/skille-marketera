# Konfiguracja krok po kroku

Stan w `grupy-fb/config.md`. Jedno pytanie naraz, po polsku, bez flag w pytaniach. Po każdym kroku aktualizuj tabelę i powiedz jednym zdaniem, co dalej. Stany: `do zrobienia`, `w toku`, `gotowe`, w K3 też `pominięte`.

**Przerwanie.** "Muszę kończyć" albo cisza: bieżący krok `w toku` z notatką, zdanie: "Stan zapisany w grupy-fb/config.md. Wróć słowami: wróćmy do konfiguracji grup."

## Kroki

**K1 Temat.** Zapytaj, o czym użytkownik chce czytać (jego klienci, jego branża, jego narzędzia) i czego nie chce widzieć (domyślnie: ogłoszenia o pracę, zlecenia, memy, sprzedaż). Zapisz oba zdania w sekcji Temat. Zapytaj też: jedna firma czy kilku klientów (agencja: `grupy-fb-<klient>/`). Utwórz folder z `raporty/`, `surowe/` i `config.md` z szablonu niżej.

**K2 Grupy.** Zapytaj o adresy grup (jeden po drugim albo lista). Adres musi zawierać `facebook.com/groups/`. Gdy użytkownik podaje nazwę, poproś o adres z paska przeglądarki. Zapytaj przy każdej: publiczna czy prywatna, do której należy (publiczne działają najlepiej). Zapisz w tabeli. Podpowiedz: 2-5 grup na start, więcej zawsze można dopisać zdaniem "obserwuj też".

**K3 Marka.** Zapytaj, jakie nazwy i linki pilnować: nazwa firmy, nazwa produktu, domena, kanał na YouTube, imię i nazwisko właściciela, jeśli występuje publicznie jako marka. Zapisz jedną frazę na linię. Nazwy skrypt dopasowuje z odmianą (Pracownia / Pracowni / Pracownię), linki i domeny dosłownie. "Nie chcę" = `pominięte`.

**K4 Klucz.** Powiedz, że pobieranie idzie przez Apify i że darmowy plan (kilka dolarów kredytu miesięcznie, około 1000 postów) wystarcza na kilka grup dziennie. Użytkownik zakłada konto sam na apify.com, w ustawieniach kopiuje klucz API i ustawia go jako `APIFY_API_TOKEN` (w `.env` projektu albo w profilu terminala). Ty nie zakładasz konta i nie wpisujesz klucza do żadnego pliku repo. Sprawdź: `python3 -c "import os;print('jest' if os.environ.get('APIFY_API_TOKEN') else 'brak')"`. Gdy `.env` istnieje w projekcie, dopisz `.env` do `.gitignore`, jeśli go tam nie ma.

**K5 Pierwsze sprawdzenie.** Uruchom gałąź Sprawdzenie z małym limitem (10 postów na grupę). Pokaż raport. Powiedz, ile kosztował run (pole `koszt_usd`) i ile zostało w planie (pole `budzet`). Zapytaj, czy temat trafia, czy coś zawęzić albo poszerzyć; poprawki wpisz do sekcji Temat.

**K6 Kadencja.** Zapytaj, czy codziennie rano, czy co kilka dni, i o godzinę. Zapisz. Zaproponuj założenie zadania cyklicznego (SKILL.md, Rutyna). Data ukończenia do tabeli.

## Szablon config.md

```markdown
# Grupy pod obserwacją: <nazwa>

Utworzono: <data>. Ostatnia zmiana: <data>. Ostatnie sprawdzenie: <data albo "jeszcze nie">.
Tryb: jedna firma / agencja (folder: <ścieżka>)

| Krok | Stan | Notatka |
|---|---|---|
| K1 Temat | do zrobienia | |
| K2 Grupy | do zrobienia | <liczba> grup |
| K3 Marka | do zrobienia | <liczba> fraz |
| K4 Klucz | do zrobienia | APIFY_API_TOKEN |
| K5 Pierwsze sprawdzenie | do zrobienia | <data, koszt> |
| K6 Kadencja | do zrobienia | |

## Temat
Interesuje mnie: <zdanie>. Pomijam: <zdanie>.

## Grupy

| Nazwa | Adres | Uwagi |
|---|---|---|
| <nazwa> | https://www.facebook.com/groups/<id> | publiczna |

## Marka do pilnowania
- <nazwa firmy>
- <domena albo link do kanału>

## Ustawienia
- Limit postów na grupę: 20
- Kadencja: <codziennie 7:30 / co 3 dni>
```

## Powrót

"Wróćmy do konfiguracji grup", "dokończmy", `/grupy-fb` bez treści przy istniejącym `config.md` z krokiem bez `gotowe`: jedno zdanie o stanie ("Temat i grupy są, brakuje klucza") i od tego kroku. Nie pytaj o to, co jest w tabeli.

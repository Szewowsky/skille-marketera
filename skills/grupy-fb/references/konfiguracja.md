# Konfiguracja krok po kroku

Stan w `grupy-fb/config.md`. Jedno pytanie naraz, po polsku, bez flag w pytaniach. Po każdym kroku aktualizuj tabelę i powiedz jednym zdaniem, co dalej. Stany: `do zrobienia`, `w toku`, `gotowe`, w K3 też `pominięte`.

**Przerwanie.** "Muszę kończyć" albo cisza: bieżący krok `w toku` z notatką, zdanie: "Stan zapisany w grupy-fb/config.md. Wróć słowami: wróćmy do konfiguracji grup."

## Kroki

**K1 Temat.** Zapytaj, o czym użytkownik chce czytać (jego klienci, jego branża, jego narzędzia) i czego nie chce widzieć (domyślnie: ogłoszenia o pracę, zlecenia, memy, sprzedaż). Zapisz oba zdania w sekcji Temat. Zapytaj też: jedna firma czy kilku klientów (agencja: `grupy-fb-<klient>/`). Utwórz folder z `raporty/`, `surowe/` i `config.md` z szablonu niżej.

**K2 Grupy.** Zapytaj o adresy grup (jeden po drugim albo lista). Adres musi zawierać `facebook.com/groups/`. Gdy użytkownik podaje nazwę, poproś o adres z paska przeglądarki. Zapytaj przy każdej: publiczna czy prywatna, do której należy (publiczne działają najlepiej). Zapisz w tabeli. Podpowiedz: 2-5 grup na start, więcej zawsze można dopisać zdaniem "obserwuj też".

**K3 Marka.** Zapytaj, jakie nazwy i linki pilnować: nazwa firmy, nazwa produktu, domena, kanał na YouTube, imię i nazwisko właściciela, jeśli występuje publicznie jako marka. Zapisz jedną frazę na linię. Nazwy skrypt dopasowuje z odmianą (Pracownia / Pracowni / Pracownię), linki i domeny dosłownie. "Nie chcę" = `pominięte`.

**K4 Klucz.** Powiedz, że pobieranie idzie przez Apify i że darmowy plan to 5 USD kredytu miesięcznie, czyli około 30 sprawdzeń trzech grup po 10 postów (jedno kosztuje około 0,15 USD). Użytkownik zakłada konto sam na apify.com i kopiuje klucz API z ustawień. Trzy drogi, od najbezpieczniejszej:

1. **Pęk kluczy systemu, klucz podawany w tej samej linii polecenia** (macOS, nic nie zostaje w plikach projektu). Zapis raz: `security add-generic-password -a APIFY_API_TOKEN -s grupy-fb -w` (system zapyta o wartość). Każde uruchomienie: `APIFY_API_TOKEN=$(security find-generic-password -a APIFY_API_TOKEN -s grupy-fb -w) python3 ...`. Sprawdzenie działa w tej samej linii: `APIFY_API_TOKEN=$(security find-generic-password -a APIFY_API_TOKEN -s grupy-fb -w) python3 -c "import os;print('jest' if os.environ.get('APIFY_API_TOKEN') else 'brak')"`.
2. **Profil terminala** (`export APIFY_API_TOKEN=...` w `~/.zshrc`): klucz dostępny wszędzie, także poza tym projektem.
3. **`.env` projektu**: najprostsze, ale klucz leży w pliku; dopisz `.env` do `.gitignore`, jeśli go tam nie ma.

Przy drogach 2 i 3 sprawdzenie to `python3 -c "import os;print('jest' if os.environ.get('APIFY_API_TOKEN') else 'brak')"`. Ty nie zakładasz konta i nie wpisujesz klucza do żadnego pliku repo.

**K5 Pierwsze sprawdzenie.** Uruchom gałąź Sprawdzenie z małym limitem (10 postów na grupę). Pokaż raport. Powiedz, ile kosztował run (pole `koszt_usd`, przy trzech grupach po 10 postów to około 0,15 USD) i ile zostało w planie (pole `budzet`, skrypt czyta limity po runie, więc liczba jest już po koszcie tego sprawdzenia; `budzet_przed` to stan sprzed). Zapytaj, czy temat trafia, czy coś zawęzić albo poszerzyć; poprawki wpisz do sekcji Temat.

**K6 Kadencja.** Zaproponuj co 2-3 dni rano i zapytaj o godzinę. Uzasadnij budżetem: sprawdzenie trzech grup po 10 postów to około 0,15 USD, co 2 dni wychodzi około 2,3 USD miesięcznie, co 3 dni około 1,5 USD, a darmowy plan Apify to 5 USD; codziennie po 20 postów (około 9 USD miesięcznie) wymaga już płatnego planu. Zapisz. Zaproponuj założenie zadania cyklicznego (SKILL.md, Rutyna). Data ukończenia do tabeli.

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
- Limit postów na grupę: 10 (plan Free; 20 postów to około 0,30 USD za sprawdzenie)
- Kadencja: <co 2 dni 7:30 / co 3 dni 8:00>
```

## Powrót

"Wróćmy do konfiguracji grup", "dokończmy", `/grupy-fb` bez treści przy istniejącym `config.md` z krokiem bez `gotowe`: jedno zdanie o stanie ("Temat i grupy są, brakuje klucza") i od tego kroku. Nie pytaj o to, co jest w tabeli.

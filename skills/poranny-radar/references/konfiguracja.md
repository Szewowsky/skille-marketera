# Konfiguracja krok po kroku

Stan w `radar/config.md`. Jedno pytanie naraz, po polsku, bez flag w pytaniach. Stany: `do zrobienia`, `w toku`, `gotowe`, w K3 też `pominięte`. Powrót = pierwszy krok bez `gotowe`.

**Przerwanie.** "Muszę kończyć" albo cisza: krok `w toku` z notatką, zdanie: "Stan zapisany w radar/config.md. Wróć słowami: wróćmy do konfiguracji radaru."

## Kroki

**K1 Zestaw.** Jedna firma czy kilku klientów (agencja: `radar-<klient>/`). Utwórz folder z `zrodla/`, `briefy/`, `policzone/`, pustym `wnioski.md` (nagłówek z szablonu w `brief.md`) i `config.md`.

**K2 Eksport mailingowy.** Zapytaj, z jakiego narzędzia użytkownik wysyła (MailerLite, Mailchimp, GetResponse, FreshMail, inne) i poproś o eksport kampanii jako plik CSV: lista wysłanych kampanii z nazwą, tematem, datą, liczbą wysłanych, otwarciami, kliknięciami, wypisami. Powiedz, gdzie to zwykle jest ("Kampanie" > eksport / raport zbiorczy). Gdy użytkownik przynosi eksport subskrybentów (adresy w kolumnach), poproś o eksport kampanii i nie czytaj tego pliku dalej. Skopiuj plik do `zrodla/mailing.csv`, uruchom skrypt z `--wyjscie` i powiedz jednym zdaniem, ile kampanii przeczytał i czy rozpoznał kolumny (pole `kolumny`). Gdy `brak_kolumn`: wypisz, czego brakuje, i poproś o inny eksport.

**K3 Klocki.** Zapytaj, co dołożyć: sprzedaż (plik tygodniowy albo miesięczny ze sklepu), skrzynka (notatka z zobowiązaniami albo narzędzie), YouTube, inne. Każdy klocek = plik w `zrodla/` albo źródło, które masz w narzędziach, plus rola jednym zdaniem w `config.md`. "Na razie tylko mailing" = `pominięte`.

**K4 Pierwszy brief.** Uruchom gałąź Brief. Pamięć pusta, więc brief mówi to wprost i zapisuje pierwsze wnioski z hipotez skryptu (temat z liczbą, dzień wysyłki, sygnały) z licznikami równymi liczbie kampanii, które je pokazują. Pokaż brief i zapytaj, czy któryś wniosek skreślić albo poprawić (to moment, w którym marketer mówi "to był wyjątek, nie wzorzec").

**K5 Kadencja.** Co poniedziałek rano czy codziennie, o której. Zapisz. Zaproponuj zadanie cykliczne (SKILL.md, Rutyna). Data ukończenia do tabeli.

## Szablon config.md

```markdown
# Poranny radar: <nazwa>

Utworzono: <data>. Ostatnia zmiana: <data>. Ostatni brief: <data albo "jeszcze nie">.
Tryb: jedna firma / agencja (folder: <ścieżka>)

| Krok | Stan | Notatka |
|---|---|---|
| K1 Zestaw | do zrobienia | |
| K2 Eksport mailingowy | do zrobienia | <narzędzie, liczba kampanii> |
| K3 Klocki | do zrobienia | <lista> |
| K4 Pierwszy brief | do zrobienia | <data> |
| K5 Kadencja | do zrobienia | |

## Źródła

| Klocek | Gdzie | Rola |
|---|---|---|
| Mailing (rdzeń) | zrodla/mailing.csv | kampanie: otwarcia, kliknięcia, wypisy |
| Sprzedaż | zrodla/sprzedaz.csv | czy po kampanii coś wpadło |
| Skrzynka | zrodla/skrzynka.md | zobowiązania z terminem na listę "dziś" |

## Ustawienia
- Kadencja: <poniedziałek 7:30>
- Okno: ostatnie 12 kampanii
```

## Powrót

"Wróćmy do konfiguracji radaru", "dokończmy", `/poranny-radar` bez treści przy `config.md` z krokiem bez `gotowe`: jedno zdanie o stanie i od tego kroku. Nie pytaj o to, co jest w tabeli.

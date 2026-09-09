# Konfiguracja krok po kroku

Gałąź "Konfiguracja" prowadzi użytkownika od zera do pierwszej walidacji. Stan siedzi w `glos-marki/config.md`, więc można przerwać po dowolnym kroku i wrócić: skill czyta plik i kontynuuje od pierwszego kroku bez "gotowe".

Zasada: jedno pytanie naraz, po polsku, bez flag i ścieżek w pytaniach. Użytkownik odpowiada zdaniem, skill sam zapisuje. Po każdym kroku aktualizuj `config.md` i powiedz jednym zdaniem, co dalej.

## Kroki

**K1 Marka.** Zapytaj o nazwę marki i czy to jedna marka, czy kilka (agencja). Jedna: folder `glos-marki/`. Kilka: `glos-marki-<klient>/` per marka, konfiguracja per folder. Utwórz folder z `korpus/` i `config.md`.

**K2 Teksty.** Zapytaj, gdzie są opublikowane teksty marki: folder na dysku, pliki do wklejenia, adres strony www, albo "nie mam". Strona: zbierz teksty z wyrenderowanej strony (przeglądarka, nie curl - strony ukrywają część treści w JS), po jednym pliku na sekcję (hero, o nas, dla kogo, FAQ, oferta), z adresem i nazwą sekcji w pierwszej linii jako komentarz. Pomiń opinie klientów (to nie jest głos marki), regulaminy, nazwy przycisków, liczniki. Powiedz użytkownikowi, że profil ze strony opisuje rejestr "sprzedajemy", i że posty/newslettery warto dorzucić później. Jeśli folder: skopiuj `.md`/`.txt`/`.docx` (docx przez konwersję do tekstu) do `korpus/`, jeden plik = jeden tekst. Jeśli wklejane: zapisuj każdy jako `korpus/NN_<slug>.md`. Jeśli "nie mam": powiedz, że 5 tekstów to minimum na profil wstępny i zaproponuj źródła (strona, newsletter, posty, oferty). Zapisz liczbę tekstów.

**K3 Brief.** Zapytaj, czy jest brand book, brief, słownik "tak mówimy / nie mówimy". Jeśli tak: zapisz jako `brief.md` (albo wyciągnij z pliku tylko manifest i słownik, bez liczb i cen). Jeśli nie: pomiń, profil wyjdzie z samego korpusu.

**K4 Profil.** Uruchom gałąź Ekstrakcja. Pokaż 3 reguły spoza briefu. Zapytaj, czy coś dopisać do sekcji 9 (reguły ręczne) - to moment, w którym szef mówi "u nas nigdy nie…".

**K5 Pierwszy test.** Poproś o jeden gotowy tekst (draft albo ostatnio opublikowany) i uruchom gałąź Walidacja. Pokaż raport. Wyjaśnij jednym zdaniem, jak czytać werdykt.

**K6 Gotowe.** Zapisz w `config.md` datę ukończenia. Powiedz, jak używać dalej ("Sprawdź ten tekst") i jak odświeżyć profil po dodaniu tekstów.

## Szablon config.md

```markdown
# Konfiguracja: <nazwa marki>

Utworzono: <data>. Ostatnia zmiana: <data>.
Tryb: jedna marka / agencja (folder: <ścieżka>)

| Krok | Stan | Notatka |
|---|---|---|
| K1 Marka | gotowe | <nazwa> |
| K2 Teksty | gotowe / w toku / pominięte | <liczba> tekstów w korpus/ |
| K3 Brief | gotowe / brak | <plik albo "bez briefu"> |
| K4 Profil | gotowe / do zrobienia | glos.md, status <pełny/wstępny/za mało danych> |
| K5 Pierwszy test | gotowe / do zrobienia | <werdykt> |
| K6 Gotowe | <data> | |

## Ustawienia
- Próg werdyktu: 1-2 NIE = do poprawek, 3+ = od nowa (zmień tu, jeśli chcesz ostrzej/łagodniej)
- Model walidatora: taki jak bieżący (albo wpisz nazwę)
```

## Powrót

Gdy użytkownik mówi "wróćmy do konfiguracji", "dokończmy", "gdzie skończyliśmy" albo wywołuje skill bez tekstu, a `config.md` istnieje i ma krok bez "gotowe": pokaż tabelę stanu w jednym zdaniu ("Marka i teksty są, brakuje profilu") i idź od tego kroku. Nie pytaj ponownie o to, co już jest w tabeli.

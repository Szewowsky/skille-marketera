# Konfiguracja krok po kroku

Gałąź "Konfiguracja" prowadzi użytkownika od zera do pierwszej walidacji. Stan siedzi w `glos-marki/config.md`, więc można przerwać po dowolnym kroku i wrócić: skill czyta plik i kontynuuje od pierwszego kroku bez "gotowe".

Zasada: jedno pytanie naraz, po polsku, bez flag i ścieżek w pytaniach. Użytkownik odpowiada zdaniem, skill sam zapisuje. Po każdym kroku aktualizuj `config.md` i powiedz jednym zdaniem, co dalej.

Stany kroków w `config.md` to dokładnie trzy słowa: `do zrobienia`, `w toku`, `gotowe` (K2 i K3 mogą mieć też `pominięte`, co liczy się jak gotowe). Nowy `config.md` ma wszystkie kroki `do zrobienia`. Powrót = pierwszy krok, który nie jest `gotowe` ani `pominięte`.

**Przerwanie.** Gdy użytkownik mówi "muszę kończyć", "wrócę później" albo po prostu przestaje odpowiadać: zapisz bieżący krok jako `w toku` z notatką, co już jest, i powiedz jednym zdaniem: "Stan zapisany w glos-marki/config.md. Wróć słowami: wróćmy do konfiguracji strażnika."

## Kroki

**K1 Marka.** Zapytaj o nazwę marki i czy to jedna marka, czy kilka (agencja). Jedna: folder `glos-marki/`. Kilka: `glos-marki-<klient>/` per marka, konfiguracja per folder. Utwórz folder w korzeniu projektu użytkownika (tam, gdzie leży `.claude/`), z `korpus/` i `config.md`. Jeśli folder już istnieje z zawartością, nie twórz nowego: powiedz, co w nim jest, i idź dalej.

**K2 Teksty.** Zapytaj, gdzie są opublikowane teksty marki: folder na dysku, pliki do wklejenia, adres strony www, albo "nie mam". Strona: zbierz teksty z wyrenderowanej strony przeglądarką, którą masz w narzędziach (nie curl - strony ukrywają część treści w JS); gdy nie masz przeglądarki, powiedz to i poproś użytkownika o wklejenie tekstów sekcja po sekcji, po jednym pliku na sekcję (hero, o nas, dla kogo, FAQ, oferta), z adresem i nazwą sekcji w pierwszej linii jako komentarz. Pomiń opinie klientów (to nie jest głos marki), regulaminy, nazwy przycisków, liczniki. Powiedz użytkownikowi, że profil ze strony opisuje rejestr "sprzedajemy", i że posty/newslettery warto dorzucić później. Jeśli folder: skopiuj `.md`/`.txt` do `korpus/`, jeden plik = jeden tekst; `.docx`/`.pdf` skonwertuj narzędziem, które masz (markitdown, pandoc, textutil na macOS), a gdy żadnego nie ma, poproś o wklejenie treści. Jeśli wklejane: zapisuj każdy jako `korpus/NN_<slug>.md`. Jeśli "nie mam": powiedz, że 5 tekstów to minimum na profil wstępny i zaproponuj źródła (strona, newsletter, posty, oferty). Zapisz liczbę tekstów.

**K3 Brief.** Zapytaj, czy jest brand book, brief, słownik "tak mówimy / nie mówimy". Jeśli tak: zapisz jako `brief.md` (albo wyciągnij z pliku tylko manifest i słownik, bez liczb i cen); gdy `brief.md` już istnieje, zapytaj, czy zastąpić, czy dopisać. Jeśli nie: oznacz `pominięte`, profil wyjdzie z samego korpusu.

**K4 Profil.** Uruchom gałąź Ekstrakcja. Pokaż 3 reguły spoza briefu. Zapytaj, czy coś dopisać do sekcji 9 (reguły ręczne) - to moment, w którym szef mówi "u nas nigdy nie…".

**K5 Pierwszy test.** Poproś o jeden gotowy tekst (draft albo ostatnio opublikowany). Gdy użytkownik nie ma żadnego, weź najnowszy plik z `korpus/` i powiedz, że to test na własnym korpusie, więc wynik będzie łagodny. Uruchom gałąź Walidacja. Pokaż raport. Wyjaśnij jednym zdaniem, jak czytać werdykt.

**K6 Gotowe.** Zapisz w `config.md` datę ukończenia. Powiedz, jak używać dalej ("Sprawdź ten tekst") i jak odświeżyć profil po dodaniu tekstów.

## Szablon config.md

```markdown
# Konfiguracja: <nazwa marki>

Utworzono: <data>. Ostatnia zmiana: <data>.
Tryb: jedna marka / agencja (folder: <ścieżka>)

| Krok | Stan | Notatka |
|---|---|---|
| K1 Marka | do zrobienia | <nazwa> |
| K2 Teksty | do zrobienia | <liczba> tekstów w korpus/ |
| K3 Brief | do zrobienia | <plik albo "bez briefu"> |
| K4 Profil | do zrobienia | glos.md, status <pełny/wstępny/za mało danych> |
| K5 Pierwszy test | do zrobienia | <werdykt> |
| K6 Gotowe | do zrobienia | <data ukończenia> |

## Ustawienia
- Próg werdyktu: 1-2 NIE = do poprawek, 3+ = od nowa (zmień tu, jeśli chcesz ostrzej/łagodniej)
- Model walidatora: taki jak bieżący (albo wpisz nazwę)
```

## Powrót

Gdy użytkownik mówi "wróćmy do konfiguracji", "dokończmy", "gdzie skończyliśmy" albo wywołuje skill bez tekstu, a `config.md` istnieje i ma krok bez "gotowe": pokaż tabelę stanu w jednym zdaniu ("Marka i teksty są, brakuje profilu") i idź od tego kroku. Nie pytaj ponownie o to, co już jest w tabeli.

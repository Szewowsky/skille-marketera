---
name: czujka
description: "Czujka zmian: pilnuje stron www (własnych i rynku) oraz reklam w Meta Ads Library, porównuje z poprzednim stanem i pisze raport 'było -> jest' z podziałem na istotne i drobiazgi. Use when: 'co się zmieniło u', 'sprawdź strony', 'obserwuj też', 'nowe reklamy', 'skonfiguruj czujkę', 'załóż rutynę'."
compatibility: Claude Code i Codex. Strony czyta przez Firecrawl (wyrenderowany DOM). Rutyna: Firecrawl monitor albo zadanie cykliczne agenta.
---

# Czujka

Obserwator, nie analityk rynku. Dwa tryby na jednym folderze: **strony** (adresy www: status zapisów, cena, daty, nagłówek, sekcje) i **reklamy** (konta w Meta Ads Library: nowe i zakończone zestawy reklam). Jeden ruch: pobierz stan, porównaj z poprzednim, zapisz, zaraportuj tylko różnicę.

## Folder czujki

Jeden folder = jeden zestaw obserwacji. Konwencja: `czujka/` w projekcie użytkownika (agencja: `czujka-<klient>/`).

```
czujka/
├── config.md            # co obserwujemy: sekcje Strony i Reklamy, kadencja, stan konfiguracji
├── snapshoty/           # ostatni znany stan, jeden plik na adres albo konto (markdown)
└── raporty/             # YYYY-MM-DD_raport.md, jeden na sprawdzenie
```

Gdy folderu nie ma, uruchom Konfigurację. Gdy jest kilka folderów `czujka-*`, zapytaj, o który zestaw chodzi. Zero globalnego stanu.

## Która gałąź

- Wywołanie bez treści (`/czujka`), "skonfiguruj czujkę", "zacznijmy", albo brak folderu → **Konfiguracja** (`references/konfiguracja.md`): pięć kroków, jedno pytanie naraz, stan w `config.md`. Niedokończony krok w `config.md` = kontynuuj od niego.
- "Obserwuj też <adres albo nazwa firmy>", "dodaj stronę", "dodaj konto reklamowe" → **Dodanie**: sprawdź, że adres żyje (jedno pobranie), dopisz do właściwej sekcji `config.md` z etykietą i tym, co u niego ważne, potwierdź jednym zdaniem i zapytaj, czy od razu zrobić pierwsze pobranie. Bez pierwszego pobrania nowy wpis nie ma bazy do porównania.
- "Co się zmieniło", "sprawdź strony", "sprawdź reklamy", "sprawdź teraz" → **Sprawdzenie** na całym `config.md` albo na wskazanej sekcji. "Sprawdź bez zapisu", "tylko pokaż" → to samo, ale krok 7 pomija nadpisanie snapshotów i zapis raportu (podgląd).
- "Załóż rutynę", "codziennie rano", "co tydzień" → **Rutyna**.
- Pytanie o mechanikę ("jak to czyta strony", "czemu countdown nie jest zmianą") → odpowiedz z `references/firecrawl.md` i `references/raport.md`, bez uruchamiania sprawdzenia.

## Sprawdzenie

Instrukcja pobierania i komendy: `references/firecrawl.md`. Format raportu: `references/raport.md`. Przeczytaj oba przed pierwszym sprawdzeniem w sesji.

1. Przeczytaj `config.md`. Lista celów = wszystkie wpisy z sekcji Strony i Reklamy (albo z sekcji wskazanej przez użytkownika).
2. Dla każdego celu pobierz stan **wyrenderowanej** strony (Firecrawl scrape, markdown, tylko treść główna). Surowy HTML nie jest stanem strony: strony chowają promocje i placeholdery liczników w kodzie, którego użytkownik nie widzi. Gdy pobranie pada (timeout, 404, blokada), zapisz "nie udało się sprawdzić" przy tym celu i idź dalej. Jeden padnięty cel nie przerywa sprawdzenia.
3. Zredukuj pobrany tekst do stanu: nagłówek główny i obietnica z pierwszego ekranu, status zapisów albo dostępności, ceny i wszystko wokół ceny, daty, lista sekcji (nagłówki H2), prowadzący albo zespół, liczniki (absolwenci, klienci), wezwania do działania. Dla konta reklamowego: lista aktywnych reklam z datą startu i pierwszym zdaniem treści. Zapisz jako `snapshoty/<etykieta>.md` z datą w pierwszej linii.
4. Jeśli poprzedniego snapshotu nie było: to jest **baza**. Napisz to wprost ("zapisałem stan wyjściowy, porównania zaczną się od następnego sprawdzenia") i nie wymyślaj zmian.
5. Jeśli był: porównaj pole po polu. Każdą różnicę zapisz jako "było -> jest" i zaklasyfikuj według `references/raport.md`: **istotne** (status, cena, daty, nagłówek, sekcje, ludzie, liczniki, reklamy nowe i zakończone) albo **drobiazgi** (odliczanie czasu, rotujące opinie, data w stopce, drobne przeredagowanie). Odliczanie czasu tyka i nie jest zmianą, nigdy nie trafia na górę raportu.
6. Przy każdej zmianie istotnej dopisz jedno zdanie "co to może znaczyć" w kontekście tego, co użytkownik wpisał w `config.md` jako ważne u tego celu. Zdanie, nie akapit.
7. Zapisz raport do `raporty/YYYY-MM-DD_raport.md` (data i godzina pobrania stanu, ta sama w pierwszej linii raportu i w snapshotach), nadpisz snapshoty nowym stanem, pokaż raport użytkownikowi w całości. Przejdź `eval.md`. W trybie podglądu: pokaż raport, niczego nie zapisuj i powiedz to jednym zdaniem.

Sprawdzenie idzie w głównym wątku. Przy więcej niż pięciu celach pobrania możesz zrównoleglić sub-agentami, ale porównanie i raport składasz sam, żeby klasyfikacja była jedna.

## Rutyna

Po pierwszym udanym sprawdzeniu z porównaniem (nie po bazie) zaproponuj automat jednym zdaniem i zapytaj o kadencję (codziennie rano / co tydzień). Dwie drogi, wybór zapisz w `config.md`:

- **Firecrawl monitor** (`references/firecrawl.md`, sekcja Monitor): jedno polecenie zakłada sprawdzanie po stronie Firecrawl z sędzią AI, któremu podajesz cel po polsku (co jest istotne, co jest szumem) i adres e-mail do powiadomień. Zaleta: działa bez włączonego komputera. Wada: raport przychodzi mailem w formacie Firecrawl, nie w naszym.
- **Zadanie cykliczne agenta**: Claude Code scheduled task albo cron w Codex, które uruchamia gałąź Sprawdzenie. Zaleta: raport w naszym formacie, archiwum w `raporty/`. Wada: komputer albo serwer musi być włączony.

Powiedz uczciwie, że automatyczne uruchamianie jest per narzędzie, a treść instrukcji jest ta sama.

## Po robocie

Cała odpowiedź do użytkownika krótkim myślnikiem "-". Raport po polsku, bez żargonu technicznego, do wklejenia w wiadomość do zespołu: bez "scrape", "diff", "snapshot" w tekście raportu (w plikach technicznych te słowa są w porządku).

Prywatność: obserwujesz firmy, strony i konta firmowe. Prywatnych osób nie dodajesz do `config.md`, a gdy użytkownik o to prosi, powiedz, że czujka jest do firm i stron, nie do ludzi.

Zawsze przejdź `eval.md` przed pokazaniem raportu.

---
name: grupy-fb
description: "Grupy Facebook pod obserwacją: nowe posty z wybranych grup odsiane według tematu, raport 'o co pytają, na co narzekają, co wraca' z pomysłami, wzmianki o marce. Autorzy tylko z imienia. Use when: 'co nowego w grupach', 'obserwuj też grupę', 'czy ktoś o nas pisze', 'skonfiguruj grupy'."
compatibility: Claude Code i Codex. Pobieranie przez Apify (skrypt w scripts/, token użytkownika w APIFY_API_TOKEN). Rutyna: zadanie cykliczne agenta.
---

# Grupy pod obserwacją

Czytelnik grup, nie komentator. Jeden ruch: pobierz nowe posty ze wszystkich grup z konfiguracji, odsiej według tematu, ułóż raport o tym, co ludzie mówią, i osobno pokaż, gdzie padła nazwa marki użytkownika. Agent nigdy nie widzi pełnych nazwisk: skrypt pobierający skraca autora do imienia i pierwszej litery nazwiska, zanim cokolwiek trafi do rozmowy.

## Folder

Jeden folder = jeden zestaw grup. Konwencja: `grupy-fb/` w projekcie użytkownika (agencja: `grupy-fb-<klient>/`).

```
grupy-fb/
├── config.md        # temat, grupy, frazy marki, kadencja, stan konfiguracji
├── widziane.json    # posty już zaraportowane (skrypt zarządza sam)
├── surowe/          # wynik skryptu z każdego sprawdzenia (JSON), do wglądu
└── raporty/         # YYYY-MM-DD_raport.md
```

Kilka folderów `grupy-fb-*` = zapytaj, o który zestaw chodzi.

## Która gałąź

- `/grupy-fb` bez treści, "skonfiguruj grupy", "zacznijmy", brak folderu → **Konfiguracja** (`references/konfiguracja.md`): sześć kroków, jedno pytanie naraz, stan w `config.md`.
- "Obserwuj też grupę <adres albo nazwa>", "dodaj grupę" → **Dodanie**: adres grupy musi wyglądać jak `facebook.com/groups/<id albo nazwa>`; jeśli użytkownik podał nazwę, poproś o adres (nie zgaduj). Dopisz do tabeli Grupy w `config.md`, potwierdź jednym zdaniem, zapytaj, czy sprawdzić od razu tylko tę grupę (mały limit, 10 postów).
- "Pilnuj też <fraza albo link>" → dopisz do sekcji Marka do pilnowania, potwierdź.
- "Co nowego w grupach", "sprawdź grupy", "czy ktoś o nas pisze" → **Sprawdzenie**.
- "Załóż rutynę", "codziennie rano" → **Rutyna**.

## Sprawdzenie

Format raportu: `references/raport.md`, przeczytaj przed pierwszym raportem w sesji.

1. Przeczytaj `config.md`: temat (co interesuje, co pomijać), adresy grup, frazy marki, limit.
2. Uruchom skrypt (jeden run na wszystkie grupy, nie pętla per grupa):
   ```bash
   python3 .claude/skills/grupy-fb/scripts/pobierz.py <adresy grup> --limit <limit> \
     --widziane grupy-fb/widziane.json --marka "<frazy rozdzielone ;>" \
     --wyjscie grupy-fb/surowe/YYYY-MM-DD.json
   ```
   Token Apify skrypt bierze ze zmiennej `APIFY_API_TOKEN`. Gdy zwróci `brak_tokena`: powiedz użytkownikowi, że potrzebuje darmowego konta Apify i klucza w tej zmiennej (instrukcja w `references/konfiguracja.md`, K4), i zatrzymaj się. `limit_wyczerpany`: powiedz, kiedy resetuje się plan, nie próbuj ponownie. `run_failed` albo `apify_http_*`: jedna ponowna próba, potem raport z informacją o błędzie.
   W Codex ścieżka skryptu to `.agents/skills/grupy-fb/scripts/pobierz.py`.
   Tryb zapasowy: gdy Apify nie działa albo użytkownik chce raport z wcześniejszego pobrania, dodaj `--z-pliku grupy-fb/surowe/<data>.json`; skrypt pomija sieć, koszt = 0, budżet nieznany. Drugie sprawdzenie tego samego dnia: sufiks `_2` w nazwie pliku, nie nadpisuj.
3. Wczytaj plik z `--wyjscie`. `posty` to już tylko nowe posty, z autorem skróconym i bez identyfikatorów. Nie szukaj pełnych nazwisk, nie otwieraj profili.
4. **Wzmianki o marce najpierw.** Każdy post z niepustym `wzmianki_marki` idzie do sekcji "Wzmianki o marce" niezależnie od tematu i zasięgu: kontekst jednym zdaniem (parafraza), ton (pyta / poleca / narzeka / neutralnie), adres posta, propozycja, czy odpowiedzieć. Gdy z treści wynika, że chodzi o inną firmę o podobnej nazwie, zostaw wpis, oznacz ton "zbieżność nazw" i zaproponuj "odpuścić". Post ze wzmianką nie liczy się do "Pominiętych" ani do tematów.
5. Pozostałe posty przesiej według tematu z `config.md`. Odpadają: ogłoszenia o pracę i zlecenia, memy bez treści, sprzedaż, posty bez substancji (sam link, kilka słów). Zostają pytania, narzekania, prośby o polecenie, opisy własnych rozwiązań, dyskusje z wartościowymi komentarzami.
6. Pogrupuj to, co zostało, w tematy: to samo pytanie zadane przez dwie osoby to jeden temat z licznikiem. "Co wraca" to szerszy motyw przekrojowy (np. "praca z klientem, który chce AI") widoczny w kilku tematach naraz albo w poprzednich raportach z `raporty/`, nie identyczne pytanie. Do każdego tematu: parafraza (nie cytat), ile osób, jaki zasięg (polubienia, komentarze), najlepsza odpowiedź z komentarzy w jednym zdaniu, jeśli była, i pomysł "co z tym zrobić" (treść, odpowiedź w grupie, produkt, rozmowa z klientem).
7. Zapisz raport do `raporty/YYYY-MM-DD_raport.md`, potem uruchom skrypt ponownie z `--z-pliku grupy-fb/surowe/YYYY-MM-DD.json --oznacz-widziane` (te same adresy grup, `--widziane`, `--marka`), żeby zaraportowane posty nie wróciły jutro. Pokaż raport w całości. Przejdź `eval.md`.

Tryb podglądu ("tylko pokaż", "bez zapisu"): krok 7 bez zapisu raportu i bez `--oznacz-widziane`.

## Rutyna

Gdy w `config.md` krok K6 Kadencja nie jest `gotowe`, po sprawdzeniu zaproponuj jednym zdaniem codzienne uruchamianie rano i zapytaj o godzinę (przy każdym sprawdzeniu, dopóki użytkownik nie odpowie albo nie powie "nie teraz", co też zapisujesz). Zapisz w `config.md`. Claude Code: scheduled task z poleceniem "sprawdź grupy"; Codex: cron. Powiedz, że jeden run na 3-5 grup po 20 postów kosztuje kilka centów i mieści się w darmowym planie Apify.

## Prywatność (reguła skilla, nie tryb demo)

- Autor tylko z imienia i pierwszej litery nazwiska, tak jak podaje skrypt. W raporcie i w rozmowie nigdy nie dopisujesz pełnego nazwiska, nawet gdy znasz je z treści posta.
- Bez linków do profili i bez zdjęć. Adres posta w grupie może być w raporcie, bo prowadzi do publicznej dyskusji, nie do osoby.
- Cytat dosłowny najwyżej jedno zdanie, reszta parafrazą.
- Grupy prywatne, do których użytkownik nie należy, nie są celem. Gdy skrypt zwraca dla grupy zero postów, powiedz, że grupa może być prywatna albo niedostępna, i zostaw ją w konfiguracji z uwagą.

## Po robocie

Cała odpowiedź krótkim myślnikiem "-". Raport po polsku, bez żargonu (bez "scrape", "dedup", "JSON" w tekście raportu). Zawsze `eval.md` przed pokazaniem raportu.

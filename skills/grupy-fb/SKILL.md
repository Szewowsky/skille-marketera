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
   Token możesz podać w tej samej linii polecenia, bez trzymania go w plikach (macOS, pęk kluczy): `APIFY_API_TOKEN=$(security find-generic-password -a APIFY_API_TOKEN -s <usługa> -w) python3 ...`.
   Tryb zapasowy: gdy Apify nie działa albo użytkownik chce raport z wcześniejszego pobrania, dodaj `--z-pliku grupy-fb/surowe/<data>.json`; skrypt pomija sieć i bierze z pliku to, co w nim jest (koszt i budżet z pobrania, które ten plik utworzyło). Drugie sprawdzenie tego samego dnia: sufiks `_2` w nazwie pliku, nie nadpisuj.
3. Wczytaj plik z `--wyjscie`. `posty` to już tylko nowe posty, z autorem skróconym i bez identyfikatorów. Nie szukaj pełnych nazwisk, nie otwieraj profili.
4. **Wzmianki o marce najpierw.** Każdy post z niepustym `wzmianki_marki` idzie do sekcji "Wzmianki o marce" niezależnie od tematu i zasięgu: kontekst jednym zdaniem (parafraza), ton (pyta / poleca / narzeka / neutralnie), adres posta, propozycja, czy odpowiedzieć. Gdy z treści wynika, że chodzi o inną firmę o podobnej nazwie, zostaw wpis, oznacz ton "zbieżność nazw" i zaproponuj "odpuścić". Post ze wzmianką nie liczy się do "Pominiętych" ani do tematów.
5. Pozostałe posty przesiej według tematu z `config.md`. Odpadają: ogłoszenia o pracę i zlecenia, memy bez treści, sprzedaż, posty bez substancji (sam link, kilka słów). Zostają pytania, narzekania, prośby o polecenie, opisy własnych rozwiązań, dyskusje z wartościowymi komentarzami.
6. Pogrupuj to, co zostało, w tematy: pytania idą do "O co pytają", frustracje do "Na co narzekają", a opisy własnych projektów i narzędzi do "Co pokazują". To samo pytanie zadane przez dwie osoby to jeden temat z licznikiem. Post z polem `kopie` większym niż 1 to jedno wklejenie do kilku grup: liczy się raz, z dopiskiem "w <N> grupach" (nazwy z `takze_w_grupach`), nie jako kilka osób. "Co wraca" to szerszy motyw przekrojowy (np. "praca z klientem, który chce AI") widoczny w kilku tematach naraz albo w poprzednich raportach z `raporty/`, nie identyczne pytanie. Do każdego tematu: parafraza (nie cytat), ile osób, jaki zasięg (polubienia, komentarze), najlepsza odpowiedź z komentarzy w jednym zdaniu, jeśli była, i pomysł "co z tym zrobić" (treść, odpowiedź w grupie, produkt, rozmowa z klientem).
7. Zapisz raport do `raporty/YYYY-MM-DD_raport.md`, potem oznacz zaraportowane posty jako widziane, żeby nie wróciły jutro. To drugie uruchomienie czyta gotowy plik z kroku 2, nie pobiera nic z sieci i nic nie kosztuje:
   ```bash
   python3 .claude/skills/grupy-fb/scripts/pobierz.py \
     --z-pliku grupy-fb/surowe/YYYY-MM-DD.json --oznacz-widziane \
     --widziane grupy-fb/widziane.json --marka "<te same frazy>"
   ```
   Adresów grup tu nie powtarzasz, bo skrypt bierze je z pliku. Koszt prawdziwego pobrania jedzie razem z plikiem i trafia do statystyk w `widziane.json`. Pokaż raport w całości. Przejdź `eval.md`.

Tryb podglądu ("tylko pokaż", "bez zapisu"): krok 7 bez zapisu raportu i bez `--oznacz-widziane`.

## Rutyna

Gdy w `config.md` krok K6 Kadencja nie jest `gotowe`, po sprawdzeniu zaproponuj jednym zdaniem uruchamianie co 2-3 dni rano i zapytaj o godzinę (przy każdym sprawdzeniu, dopóki użytkownik nie odpowie albo nie powie "nie teraz", co też zapisujesz). Zapisz w `config.md`. Claude Code: scheduled task z poleceniem "sprawdź grupy"; Codex: cron. Uzasadnij budżetem: jedno sprawdzenie 3 grup po 10 postów kosztuje około 0,15 USD, po 20 postów około 0,30 USD, a darmowy plan Apify to 5 USD miesięcznie. Co 2-3 dni po 10 postów mieści się w planie Free (około 1,5-2,3 USD miesięcznie); codziennie po 20 postów plan Free przekracza dwukrotnie.

## Prywatność (reguła skilla, nie tryb demo)

- Autor tylko z imienia i pierwszej litery nazwiska, tak jak podaje skrypt. W raporcie i w rozmowie nigdy nie dopisujesz pełnego nazwiska, nawet gdy znasz je z treści posta.
- Skrypt skraca podpis autora i zamienia otagowane osoby w treści ("@Anna Kowalska") na "@[osoba]", ale nazwisko wpisane zwykłym zdaniem w treści posta zostaje. Dlatego nazwisk w raporcie pilnuje agent: przepisujesz parafrazą bez nazwiska. Folder `surowe/` to lokalny plik roboczy, nie materiał do wysłania: nie wklejasz go do rozmowy w całości, nie udostępniasz i trzymasz poza gitem (przy zakładaniu folderu dopisz `grupy-fb/surowe/` do `.gitignore`).
- Bez linków do profili i bez zdjęć. Adres posta w grupie może być w raporcie, bo prowadzi do publicznej dyskusji, nie do osoby.
- Cytat dosłowny najwyżej jedno zdanie, reszta parafrazą.
- Grupy prywatne, do których użytkownik nie należy, nie są celem. Gdy skrypt zwraca dla grupy zero postów, powiedz, że grupa może być prywatna albo niedostępna, i zostaw ją w konfiguracji z uwagą.

## Po robocie

Cała odpowiedź krótkim myślnikiem "-". Raport po polsku, bez żargonu (bez "scrape", "dedup", "JSON" w tekście raportu). Zawsze `eval.md` przed pokazaniem raportu.

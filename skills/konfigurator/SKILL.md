---
name: konfigurator
description: "Konfigurator skilli marketera: co zainstalowane i skonfigurowane, czy są klucze, tabela gotowości, potem konfiguracja wybranego skilla jego własną instrukcją. Use when: 'skonfiguruj skille marketera', 'od czego zacząć', 'co mam skonfigurowane', 'czego brakuje', 'dokończmy konfigurację'."
compatibility: Claude Code i Codex. Czyta pliki config skilli i sprawdza narzędzia w terminalu. Sam nie konfiguruje: prowadzi do gałęzi Konfiguracja właściwego skilla.
---

# Konfigurator

Jedno wejście do czterech skilli. Każdy skill z tego repo trzyma własny stan konfiguracji w swoim `config.md` z tabelą kroków (K1, K2...). Konfigurator te tabele czyta, pokazuje jedną tabelę gotowości i oddaje ster gałęzi Konfiguracja tego skilla, który użytkownik wybierze. Zero własnego pliku stanu: stan żyje w skillach.

Mapa skilli (folder, plik stanu, klucz, czym sprawdzić): `references/inwentarz.md`. Przeczytaj przed pierwszym uruchomieniem w sesji.

## Przebieg

1. **Inwentarz.** Dla każdego z czterech skilli sprawdź trzy rzeczy według `references/inwentarz.md`: zainstalowany (folder skilla w `.claude/skills/` albo `.agents/skills/`), skonfigurowany (jego `config.md` istnieje; policz kroki `gotowe` albo `pominięte` przeciw wszystkim wierszom tabeli; pierwszy krok bez tych stanów = następny krok), klucz (polecenie z inwentarza; wynik "jest" albo "brak", nigdy wartość klucza). Agencja: gdy folderów jest kilka (`czujka-<klient>/`), jeden wiersz na folder. Do tego dwa sprawdzenia wspólne: `python3 --version` (skrypty radaru i grup) oraz `.gitignore` z wpisami z sekcji Wspólne w inwentarzu (tylko gdy projekt jest w gicie).
2. **Tabela gotowości.** Jedna tabela, jeden wiersz na skill (wzór: `examples/tabela-gotowosci.md`): skill, stan (`nie zainstalowany` / `nie zaczęty` / `w toku 3/6, następny: K4 Klucz` / `gotowy`), klucz (`jest` / `brak` / `nie dotyczy` / `częściowo: brak <nazwa klucza>`, gdy skill potrzebuje dwóch, jak czujka z reklamami), następny ruch jednym zdaniem po polsku, bez flag i ścieżek. Pod tabelą jedna linia o Pythonie i `.gitignore`, tylko gdy coś brakuje. Przed pokazaniem tabeli przejdź `eval.md`.
3. **Kolejność.** Zaproponuj kolejność od skilla, który potrzebuje najmniej od użytkownika: strażnik (tylko teksty marki), radar (jeden eksport CSV), grupy (konto Apify), czujka (Firecrawl i ewentualnie Apify). Skill `gotowy` pomiń. Zapytaj jednym zdaniem, od którego zacząć, albo czy zrobić po kolei.
4. **Przekazanie.** Dla wybranego skilla przeczytaj jego `references/konfiguracja.md` i prowadź dokładnie tę gałąź, od pierwszego kroku bez `gotowe` ani `pominięte`. Krok "Klucz" w skillu ma pierwszeństwo przed Twoim sprawdzeniem z kroku 1: gdy skill mówi, co zrobić z brakiem klucza, mówisz to samo. Nie streszczaj kroków skilla i nie łącz pytań z kilku skilli w jedno.
5. **Powrót.** Gdy gałąź skilla dojdzie do końca (albo użytkownik przerwie słowami "muszę kończyć"), pokaż tabelę gotowości jeszcze raz ze zmienionym wierszem i zapytaj o następny skill. Wszystkie `gotowe` = powiedz, jak używać każdego na co dzień (zdania z sekcji "Na co dzień" w inwentarzu), i zakończ.

## Klucze

Użytkownik zakłada konta i kopiuje klucze sam. Ty sprawdzasz obecność poleceniem z inwentarza i mówisz jednym zdaniem, gdzie klucz ma trafić (`.env` projektu albo profil terminala; Firecrawl: `firecrawl login`). Klucza nie wpisujesz do żadnego pliku i nie prosisz o wklejenie go na czacie. `.env` w projekcie w gicie = dopisz `.env` do `.gitignore`, jeśli brakuje.

## Po robocie

Odpowiedzi po polsku, krótkim myślnikiem "-". Tabela gotowości jest dla marketera, nie dla programisty: stany i następne ruchy zdaniem, bez nazw plików. Nazwy plików i polecenia tylko wtedy, gdy użytkownik o nie pyta.


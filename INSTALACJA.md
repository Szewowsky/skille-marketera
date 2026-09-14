# Instalacja (instrukcja dla agenta)

Ten plik czyta Claude Code albo Codex, gdy użytkownik powie np. "Zainstaluj skille z https://github.com/Szewowsky/skille-marketera" albo "zainstaluj strażnika głosu marki z tego repo". Wykonaj kroki po kolei, w projekcie użytkownika (bieżący folder). Nic nie pobieraj poza tym repo.

## Kroki

1. Źródło: jeśli użytkownik podał ścieżkę lokalną albo rozpakowany ZIP, użyj jej bez kopiowania. W przeciwnym razie `git clone --depth 1 https://github.com/Szewowsky/skille-marketera /tmp/skille-marketera` i zapamiętaj, że to folder tymczasowy.
2. Zobacz, co jest w `skills/*/` (README może wymieniać skille planowane, których jeszcze nie ma). Jeśli jest więcej niż jeden, a użytkownik nie wybrał, zapytaj. Domyślnie wszystkie.
3. Dla każdego wybranego skilla skopiuj z `skills/<nazwa>/` do `.claude/skills/<nazwa>/` w projekcie użytkownika: `SKILL.md`, `eval.md`, `references/`, `examples/`, `scripts/` (jeśli jest; skrypty są w Pythonie 3 bez zależności). Nie kopiuj katalogu `evals/` (testy autora). Jeśli użytkownik pracuje w Codex, skopiuj to samo także do `.agents/skills/<nazwa>/`; jeśli nie wiesz, w czym pracuje, zapytaj zamiast zgadywać po istniejących katalogach.
4. Skopiuj `agents/*.md` do `.claude/agents/` w projekcie użytkownika. To sub-agenci, których skille wołają (np. `walidator` z narzędziami tylko do czytania). Jeśli plik o tej nazwie już istnieje, zapytaj przed nadpisaniem.
5. Skopiuj `glos-marki/` (README + pusty `korpus/`) do projektu użytkownika, jeśli jeszcze go nie ma. Nie nadpisuj istniejącego.
   Dla skilla `czujka` nie ma szablonu folderu: folder `czujka/` tworzy sam skill w kroku Konfiguracja. Jeśli użytkownik instaluje czujkę, sprawdź `firecrawl --status` (albo `npx -y firecrawl-cli@latest --status`); gdy nie jest zalogowany, powiedz jednym zdaniem, że czujka potrzebuje `firecrawl login` przed pierwszym sprawdzeniem. Nie loguj się za użytkownika.
6. Jeśli projekt jest repozytorium gita (`git rev-parse --is-inside-work-tree`), dopisz do `.gitignore` linie z sekcji "Do .gitignore" niżej, żeby teksty i profil marki nie trafiły do gita użytkownika. Jeśli nie jest, pomiń ten krok i powiedz o tym w podsumowaniu.
7. Jeśli projekt ma `CLAUDE.md` albo `AGENTS.md`, dopisz jedną linię: "Skille z skille-marketera: <lista>. Walidator: `.claude/agents/walidator.md`." Jeśli nie ma, nie twórz.
8. Usuń folder tymczasowy tylko wtedy, gdy sam go utworzyłeś w kroku 1 (`/tmp/skille-marketera`). Nigdy nie usuwaj ścieżki podanej przez użytkownika.
9. Powiedz użytkownikowi, co zostało skopiowane i jak zacząć: teksty marki do `glos-marki/korpus/`, potem "Wyprowadź głos marki", potem "Sprawdź ten tekst". Dla czujki: "Skonfiguruj czujkę". Dla grup: "Skonfiguruj grupy". Dla radaru: "Skonfiguruj radar".

## Do .gitignore

```
/glos-marki*/**
!/glos-marki/README.md
!/glos-marki/korpus/
!/glos-marki/korpus/.gitkeep
/czujka*/**
/grupy-fb*/**
/radar*/**
.env
```

## Aktualizacja

Ta sama procedura z krokiem 3 i 4 nadpisującym pliki skilla i agenta (to pliki z repo, nie użytkownika). `glos-marki/` i `.gitignore` zostają nietknięte.

## Czego instalacja nie robi

Nie instaluje niczego globalnie, nie dotyka `~/.claude`, nie zmienia ustawień, nie pobiera nic spoza tego repo.

# Instalacja (instrukcja dla agenta)

Ten plik czyta Claude Code albo Codex, gdy użytkownik powie np. "Zainstaluj skille z https://github.com/Szewowsky/skille-marketera" albo "zainstaluj strażnika głosu marki z tego repo". Wykonaj kroki po kolei, w projekcie użytkownika (bieżący folder). Nic nie pobieraj poza tym repo.

## Kroki

1. Pobierz repo do folderu tymczasowego: `git clone --depth 1 https://github.com/Szewowsky/skille-marketera /tmp/skille-marketera` (jeśli użytkownik podał ścieżkę lokalną albo ZIP, użyj jej).
2. Zapytaj, które skille zainstalować, jeśli użytkownik nie powiedział. Lista: `skills/*/`. Domyślnie wszystkie.
3. Dla każdego wybranego skilla skopiuj cały folder `skills/<nazwa>/` do `.claude/skills/<nazwa>/` w projekcie użytkownika. Codex: dodatkowo do `.agents/skills/<nazwa>/`, jeśli taki katalog jest w użyciu. Nie kopiuj `evals/`.
4. Skopiuj `agents/*.md` do `.claude/agents/` w projekcie użytkownika. To sub-agenci, których skille wołają (np. `walidator` z narzędziami tylko do czytania). Jeśli plik o tej nazwie już istnieje, zapytaj przed nadpisaniem.
5. Skopiuj `glos-marki/` (README + pusty `korpus/`) do projektu użytkownika, jeśli jeszcze go nie ma. Nie nadpisuj istniejącego.
6. Dopisz do `.gitignore` projektu (utwórz, jeśli brak) linie z sekcji "Do .gitignore" niżej, żeby teksty i profil marki nie trafiły do publicznego gita użytkownika.
7. Jeśli projekt ma `CLAUDE.md` albo `AGENTS.md`, dopisz jedną linię: "Skille z skille-marketera: <lista>. Walidator: `.claude/agents/walidator.md`." Jeśli nie ma, nie twórz.
8. Usuń folder tymczasowy.
9. Powiedz użytkownikowi, co zostało skopiowane i jak zacząć: teksty marki do `glos-marki/korpus/`, potem "Wyprowadź głos marki", potem "Sprawdź ten tekst".

## Do .gitignore

```
glos-marki*/**
!glos-marki/README.md
!glos-marki/korpus/
!glos-marki/korpus/.gitkeep
```

## Aktualizacja

Ta sama procedura z krokiem 3 i 4 nadpisującym pliki skilla i agenta (to pliki z repo, nie użytkownika). `glos-marki/` i `.gitignore` zostają nietknięte.

## Czego instalacja nie robi

Nie instaluje niczego globalnie, nie dotyka `~/.claude`, nie zmienia ustawień, nie pobiera nic spoza tego repo.

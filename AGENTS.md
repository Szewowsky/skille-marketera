# skille-marketera

Publiczne repo ze skillami dla marketera. Jeden skill = jeden folder `skills/<nazwa>/` z `SKILL.md`, opcjonalnie `eval.md`, `references/`, `examples/`.

## Zasady

- Repo jest publiczne. Nie wolno tu trafić: profilom głosu prawdziwych marek, brand contextom, eksportom z narzędzi mailingowych, listom grup FB, tokenom, prawdziwym postom klientów. Fixtures w `tests/` wyłącznie syntetyczne.
- Polski, krótkie myślniki "-". Długie pauzy i półpauzy nie wchodzą do plików repo (check.sh je łapie).
- Skill niczego nie generuje, gdy jest bramką (strażnicy). Nie dopisuj kroków "zaproponuj poprawkę".
- Każdy skill działa w Claude Code i w Codex. `AGENTS.md` to to samo co ten plik, dla Codexa.
- Przed commitem: `scripts/check.sh`.

## Testy

`tests/<skill>/` trzyma syntetyczne fixtures i opis oczekiwanego zachowania na seamach. Nie testujemy, jak agent liczy - testujemy, co wychodzi z danego wejścia.

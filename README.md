# Skille marketera

Skille dla Claude Code i Codex z webinaru "5 skilli Claude Code dla marketera" (AI_Marketers 3). Każdy skill to folder `skills/<nazwa>/` z plikiem `SKILL.md`. Działają w Claude Code i w Codex - ten sam tekst instrukcji, różny mechanizm uruchomienia (opis w sekcji "Claude Code vs Codex").

## Instalacja: jedno zdanie do agenta

Otwórz Claude Code albo Codex w swoim projekcie i powiedz:

```
Zainstaluj skille z https://github.com/Szewowsky/skille-marketera
```

Agent czyta `INSTALACJA.md` z tego repo i kopiuje do Twojego projektu: skille do `.claude/skills/`, sub-agenta walidatora do `.claude/agents/`, szablon folderu `glos-marki/` i wpisy do `.gitignore`. Nic globalnego, nic poza tym repo. Potem: teksty marki do `glos-marki/korpus/`, "Wyprowadź głos marki", "Sprawdź ten tekst".

Alternatywa dla jednego skilla bez agenta: `npx skills add Szewowsky/skille-marketera --skill straznik-glosu-marki` (walidator uruchomi się wtedy jako zwykły sub-agent, bez ograniczenia narzędzi).

## Skille

| Skill | Co robi | Stan |
|---|---|---|
| `straznik-glosu-marki` | Wyprowadza profil głosu marki z jej tekstów (posty, strona, newslettery) i sprawdza dowolny tekst komunikacji punkt po punkcie, z cytatami jako dowodem. Bramka, nie pisarz. | gotowy |
| `poranny-radar` | Poranny brief marketera z danych newslettera i pamięcią wniosków. | planowany |
| `grupy-fb` | Monitoring grup Facebook pod kątem tematu, z anonimizacją autorów. | planowany |
| `audyt-strony` | Wrapper na audyt strony (Impeccable) z instrukcją. | planowany |
| `straznik-wysylki` | Checklista przed wysyłką newslettera, z dowodami. | planowany |

## Jak skonfigurować pod siebie

Skille nie mają w sobie żadnej marki. Profil głosu, listy grup, dane kampanii - to Twoje pliki, trzymane w Twoim folderze projektu, nie w tym repo. Każdy skill mówi na starcie, czego potrzebuje i gdzie tego szuka.

## Claude Code vs Codex

Instrukcje są te same. Różnica jest w izolacji: w Claude Code walidator uruchamia się jako osobny agent z pustym kontekstem, w Codex - w świeżym wątku. Zadania cykliczne: w Claude Code scheduled task, w Codex cron albo ręczne uruchomienie.

## Licencja

MIT. Modyfikuj pod siebie.

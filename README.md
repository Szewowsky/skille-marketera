# Skille marketera

Skille dla Claude Code i Codex z webinaru "5 skilli Claude Code dla marketera" (AI_Marketers 3). Każdy skill to folder `skills/<nazwa>/` z plikiem `SKILL.md`. Działają w Claude Code i w Codex - ten sam tekst instrukcji, różny mechanizm uruchomienia (opis w sekcji "Claude Code vs Codex").

## Instalacja jedną linią

```
npx skills add Szewowsky/skille-marketera --skill straznik-glosu-marki
```

Bez flag `npx skills` zapyta, czy instalować do projektu czy globalnie. Dla wszystkich skilli naraz:

```
npx skills add Szewowsky/skille-marketera --all
```

Albo powiedz agentowi: "Zainstaluj skill straznik-glosu-marki z https://github.com/Szewowsky/skille-marketera".

## Skille

| Skill | Co robi | Stan |
|---|---|---|
| `straznik-glosu-marki` | Wyprowadza profil głosu marki z jej tekstów i sprawdza gotowy tekst punkt po punkcie, z cytatami jako dowodem. Bramka, nie pisarz. | w budowie |
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

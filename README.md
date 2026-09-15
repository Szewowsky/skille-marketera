# Skille marketera

Skille dla Claude Code i Codex z webinaru "5 skilli Claude Code dla marketera" (AI_Marketers 3). Każdy skill to folder `skills/<nazwa>/` z plikiem `SKILL.md`. Działają w Claude Code i w Codex - ten sam tekst instrukcji, różny mechanizm uruchomienia (opis w sekcji "Claude Code vs Codex").

## Instalacja: jedno zdanie do agenta

Otwórz Claude Code albo Codex w swoim projekcie i powiedz:

```
Zainstaluj skille z https://github.com/Szewowsky/skille-marketera
```

Agent czyta `INSTALACJA.md` z tego repo i kopiuje do Twojego projektu: skille do `.claude/skills/`, sub-agenta walidatora do `.claude/agents/`, szablon folderu `glos-marki/` i wpisy do `.gitignore`. Nic globalnego, nic poza tym repo. Potem jedno zdanie: "Skonfiguruj skille marketera" - konfigurator pokaże, co gotowe, czego brakuje, i poprowadzi przez resztę.

Grupy FB potrzebują darmowego konta Apify i klucza w `APIFY_API_TOKEN` (skill prowadzi przez to w konfiguracji; najbezpieczniej z pęku kluczy, w tej samej linii polecenia). Pobieranie kosztuje: sprawdzenie trzech grup po 10 postów to około 0,15 USD, po 20 postów około 0,30 USD, a darmowy plan Apify to 5 USD miesięcznie, więc skill proponuje kadencję co 2-3 dni rano, nie codziennie. Czujka potrzebuje dodatkowo klucza Firecrawl (`firecrawl login` albo `FIRECRAWL_API_KEY` w `.env`). Potem: "Skonfiguruj czujkę", a po pierwszym porównaniu "Załóż rutynę".

Alternatywa dla jednego skilla bez agenta: `npx skills add Szewowsky/skille-marketera --skill straznik-glosu-marki` (walidator uruchomi się wtedy jako zwykły sub-agent, bez ograniczenia narzędzi).

## Skille

| Skill | Co robi | Stan |
|---|---|---|
| `straznik-glosu-marki` | Wyprowadza profil głosu marki z jej tekstów (posty, strona, newslettery) i sprawdza dowolny tekst komunikacji punkt po punkcie, z cytatami jako dowodem. Bramka, nie pisarz. | gotowy |
| `czujka` | Pilnuje stron www (własnych i rynku) oraz reklam w Meta Ads Library: pobiera stan wyrenderowanej strony przez Firecrawl, porównuje z poprzednim i pisze raport "było -> jest" z podziałem na istotne i drobiazgi. | gotowy |
| `poranny-radar` | Poranny brief z eksportu mailingowego i klocków (sprzedaż, skrzynka): trzy rzeczy na dziś, co traci, co zaskoczyło, wnioski z licznikiem obserwacji, które kolejny brief cytuje z powrotem. Liczby liczy skrypt. | gotowy |
| `grupy-fb` | Czyta nowe posty z wybranych grup Facebook, odsiewa według tematu użytkownika, pisze raport "o co pytają, na co narzekają, co wraca" z pomysłami i pilnuje wzmianek o marce. Autorzy tylko z imienia, bez linków do profili, anonimizacja w skrypcie zanim agent cokolwiek zobaczy. | gotowy |
| `konfigurator` | Jedno wejście do reszty: sprawdza, co jest zainstalowane i skonfigurowane, czy są klucze (Firecrawl, Apify), pokazuje tabelę gotowości i prowadzi przez konfigurację wybranego skilla, krok po kroku, jego własną instrukcją. | gotowy |
| `straznik-wysylki` | Checklista przed wysyłką newslettera, z dowodami. | planowany |

## Jak skonfigurować pod siebie

Skille nie mają w sobie żadnej marki. Profil głosu, listy grup, dane kampanii - to Twoje pliki, trzymane w Twoim folderze projektu, nie w tym repo. Każdy skill mówi na starcie, czego potrzebuje i gdzie tego szuka.

## Claude Code vs Codex

Instrukcje są te same. Różnica jest w izolacji: w Claude Code walidator uruchamia się jako osobny agent z pustym kontekstem, w Codex - w świeżym wątku. Zadania cykliczne: w Claude Code scheduled task, w Codex cron albo ręczne uruchomienie.

## Licencja

MIT. Modyfikuj pod siebie.

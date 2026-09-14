# Raport z grup

Czyta się w minutę, wkleja do wiadomości dla zespołu. Po polsku, bez żargonu. Autor tylko "Imię N.", bez linków do profili, cytat najwyżej jedno zdanie. Plik `raporty/YYYY-MM-DD_raport.md`.

## Szablon

```markdown
# Grupy pod obserwacją: raport z <data>

Grupy: <N>. Nowych postów: <M> (pominięto <K> już zaraportowanych). Koszt: <X> USD, w planie zostało <Y> USD. (Przy sprawdzeniu z zapisanego pliku: "Koszt: 0 USD, raport z wcześniejszego pobrania z <data>.")

## Wzmianki o marce
- **<Nazwa grupy>, <data>, <Imię N.>** (<ton: poleca / pyta / narzeka / neutralnie>): <kontekst jednym zdaniem, parafraza>. Zasięg: <polubienia> polubień, <komentarze> komentarzy. <adres posta>
  Co zrobić: <odpowiedzieć / podziękować / odpuścić, jedno zdanie>.
(albo: "Brak wzmianek w tym sprawdzeniu.")

## O co pytają
1. **<Temat parafrazą>** (<ile osób>, <zasięg>). <Najlepsza odpowiedź z komentarzy w jednym zdaniu, jeśli była>. Co z tym zrobić: <pomysł na treść, odpowiedź w grupie, produkt albo rozmowę z klientem>.

## Na co narzekają
1. **<Temat>** (<ile osób>, <zasięg>). Co z tym zrobić: <...>.

## Co pokazują
1. **<Czyj projekt albo narzędzie, parafrazą>** (<Imię N.>, <zasięg>). <Czym to jest w jednym zdaniu>. Co z tym zrobić: <...>.

## Co wraca
- <temat, który pojawił się w poprzednich raportach albo u więcej niż jednej osoby> (<ile razy>)

## Pominięte
<liczba> postów bez związku z tematem (ogłoszenia, memy, sprzedaż). Niedostępne grupy: <lista albo "żadna">.
```

## Reguły

- Wzmianki o marce zawsze na górze, także gdy post nie pasuje do tematu. Post z wzmianką nie trafia drugi raz do "O co pytają".
- Parafraza zamiast cytatu. Dosłowny cytat tylko wtedy, gdy sformułowanie jest treścią (np. hasło, którego ludzie używają), i tylko jedno zdanie.
- Jedno "co z tym zrobić" na temat, zdanie, nie akapit. Pomysł ma być do wykonania w tym tygodniu.
- "Co pokazują" to opisy własnych rozwiązań: ktoś pokazuje swój arkusz, automatyzację, szablon albo narzędzie, którego używa. Nie pytanie i nie narzekanie, więc nie mieszaj tego z dwiema sekcjami wyżej. Gdy takich postów nie było, napisz "Nikt nic nie pokazywał w tym sprawdzeniu."
- Liczby zasięgu z pól skryptu, nie z pamięci. Gdy dwa posty to ten sam temat, zasięg sumujesz i piszesz "2 osoby".
- Ten sam post wklejony do kilku grup (pole `kopie` większe niż 1) liczy się raz, z dopiskiem "w <N> grupach" po nazwie tematu. To jedna osoba, nie dwie, więc zasięgu z kopii nie sumujesz z liczbą osób.
- "Co wraca" wypełniasz motywem przekrojowym z tego raportu (wspólny wątek kilku tematów) i z poprzednich raportów w `raporty/`, jeśli są. Gdy nie ma poprzednich raportów, napisz "pierwszy raport, porównanie od następnego".
- W raporcie nie ma pełnych nazwisk, adresów e-mail, numerów telefonu ani linków do profili. Adres posta w grupie jest w porządku.
- Krótki myślnik "-" w całym raporcie.

# Raport ze sprawdzenia

Raport czyta człowiek w minutę i wkleja do wiadomości dla zespołu. Po polsku, bez słów technicznych, bez własnego HTML-a ani kodu. Jeden raport na sprawdzenie, plik `raporty/YYYY-MM-DD_raport.md`.

## Klasyfikacja zmian

**Istotne** (zawsze na górze, w tej kolejności):
1. Status zapisów albo dostępności: lista oczekujących, zapisy otwarte, sprzedaż zamknięta, "wyprzedane".
2. Cena i wszystko wokół ceny: kwota, waluta, netto/brutto, raty, przekreślona cena, kod rabatowy, termin promocji.
3. Daty: start programu, start zapisów, koniec zapisów, webinar.
4. Nagłówek główny i obietnica na pierwszym ekranie.
5. Sekcje: nowa albo usunięta sekcja, nowy moduł, nowy bonus.
6. Ludzie: nowy albo usunięty prowadzący, zespół.
7. Liczniki: absolwenci, klienci, opinie (liczba, nie treść).
8. Reklamy: nowy zestaw reklam (data startu, pierwsze zdanie), zakończony zestaw, zmiana przekazu w reklamach. Nowe i zakończone to osobne punkty, każdy z własnym zdaniem znaczenia.
9. Pojawienie się elementu, którego nie było: odliczanie, pasek promocji, przekreślona cena. Samo tykanie odliczania to drobiazg, ale odliczanie, które wczoraj nie istniało, to start kampanii i jest istotne.

**Drobiazgi** (na dole, w jednej sekcji, można nie czytać): odliczanie czasu, rotujące opinie i cytaty, data w stopce, kolejność elementów bez zmiany treści, poprawki literówek, drobne przeredagowanie bez zmiany sensu, zmiana obrazka bez zmiany tekstu.

**Wezwania do działania**: zmiana słów na przycisku to drobiazg ("Zapisz się" -> "Zapisz się teraz"), chyba że zmienia obietnicę albo etap sprzedaży ("Zapisz się na listę" -> "Kup teraz"), wtedy jest istotna jako status.

**Nie jest zmianą**: ta sama treść w innym miejscu strony, różnica w białych znakach, zmiana w kodzie niewidoczna dla użytkownika.

Gdy nie masz pewności, czy coś jest istotne: sprawdź notatkę "ważne" przy tym celu w `config.md`. To, co użytkownik tam wpisał, jest istotne z definicji.

## Szablon

```markdown
# Czujka: raport z <data i godzina pobrania stanu>

Sprawdzone: <N> stron, <M> kont reklamowych. Nie udało się sprawdzić: <lista albo "nic">.

## Istotne

### <Etykieta celu>
- **Status zapisów:** było "lista oczekujących" -> jest "zapisy otwarte". Co to może znaczyć: <jedno zdanie w kontekście notatki "ważne">.
- **Cena:** było 2490 zł -> jest 2990 zł (przekreślone 3490 zł, promocja do 30.09).

### <Etykieta konta reklamowego>
- **Nowe reklamy (2):** od 12.09 "Ostatnie miejsca w jesiennej edycji..." i od 13.09 "Sprawdź, czy Twoja firma...". Co to może znaczyć: <jedno zdanie>.
- **Zakończone reklamy (1):** była od 20.08 "..." -> wyłączona. Co to może znaczyć: <jedno zdanie>.

## Bez istotnych zmian
- <Etykieta>: <co sprawdzono bez zmian, jedną linią: nagłówek, status, cena, sekcje>

## Drobiazgi
- <Etykieta>: odliczanie czasu zmieniło się z 47 dni na 46.
- <Etykieta>: inna opinia w karuzeli.

## Nie udało się sprawdzić
- <Etykieta>: strona nie odpowiedziała (przekroczony czas). Spróbuję przy następnym sprawdzeniu.
```

Gdy nie zmieniło się nic istotnego, sekcja Istotne ma jedno zdanie: "Bez istotnych zmian." i reszta raportu to same drobiazgi. Przy pierwszym pobraniu (baza) raport ma zamiast sekcji Istotne sekcję "Stan wyjściowy" z jedną linią na cel: nagłówek, status, cena, liczba aktywnych reklam. Rzeczy, które zauważyłeś przy pobraniu i które przydadzą się przy następnym porównaniu (martwy formularz, czynny przycisk starej edycji, ucięta lista reklam), idą do opcjonalnej sekcji "Warto wiedzieć przy następnym sprawdzeniu" na końcu raportu, w bazie i w każdym późniejszym raporcie.

## Reguły

- "Było -> jest" przy każdej zmianie, z dosłownym fragmentem po obu stronach strzałki. Bez "zmieniła się cena" bez kwot.
- Jedno zdanie "co to może znaczyć" tylko przy zmianie istotnej. Nie przy drobiazgach, nie przy bazie.
- Odliczanie czasu, które tyka codziennie, to zawsze drobiazg. Nigdy nie jest główną wiadomością dnia.
- Cel, którego nie udało się sprawdzić, dostaje własną sekcję, a reszta raportu powstaje normalnie.
- W raporcie nie ma adresów e-mail, nazwisk osób prywatnych ani treści komentarzy. Firmy, strony, prowadzący jako osoby publiczne na stronie: tak.
- Krótki myślnik "-" w całym raporcie. Strzałka "->" tylko w parach było/jest.

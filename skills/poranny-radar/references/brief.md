# Brief "co dziś"

Czyta się w dwie minuty. Zdania, nie tabelki; tabelka jest na końcu, dla dociekliwych. Plik `briefy/YYYY-MM-DD_brief.md`.

## Szablon

```markdown
# Poranny radar: <data, dzień tygodnia>

Źródła: <mailing: N kampanii do <data ostatniej>, okno: ostatnie N>, <klocki, które weszły>. Nie udało się odczytać: <klocek albo "nic">.

## Trzy rzeczy na dziś
1. <Zadanie z liczbą, z której wynika. Np. "Wyślij kolejny mail w piątek przed południem: sobotnie wysyłki mają 25,4% otwarć przy 34,7% w piątki (2 obserwacje).">
2. <...>
3. <...>

## Co traci, co zaskoczyło
- **Traci:** <jedno zdanie z sygnału skryptu, z kampanią, wartością i medianą>.
- **Zaskoczyło:** <jedno zdanie>.

## Co pamiętam
- <Wniosek z wnioski.md, dosłownie> (obserwacje: N). <Jak to stosuję dziś: jedno zdanie.>
- <...>
(albo: "Pierwszy brief, pamięć pusta. Zapisałem <N> wniosków na start.")

## Z innych klocków
- **Sprzedaż:** <jedna linia: suma, zamówienia, czy po ostatniej kampanii coś wpadło>.
- **Skrzynka:** <zobowiązania z terminem, bez nadawców>.

## Liczby
| Data | Kampania | Temat | Wysłane | Otwarcia | Kliknięcia | Wypisy |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ...% | ...% | ... |
```

## Reguły

- Każde zadanie ma liczbę, z której wynika, i jest wykonalne dziś albo w tym tygodniu. Zadanie bez liczby = wykreśl.
- "Traci" i "Zaskoczyło" biorą się z sygnałów skryptu. Gdy sygnałów brak: "Bez odchyleń od mediany w tym oknie" i tyle.
- Wnioski cytujesz z pliku dosłownie (tytuł w pogrubieniu), z aktualnym licznikiem. Wniosek z 1-2 obserwacjami nazywasz hipotezą, od 3 wzorcem. Nie udawaj pewności: "3 obserwacje, do potwierdzenia" jest lepsze niż "zawsze".
- Liczby ze skryptu, nie z pamięci. Procenty z przecinkiem i jednym miejscem po przecinku w tekście; w tabeli dwa miejsca dopuszczalne.
- Klocek, którego nie udało się odczytać, dostaje jedną linię i nie blokuje briefu.
- Bez CTR, OR, CSV, JSON w tekście: "kliknięcia", "otwarcia", "eksport", "plik".
- Krótki myślnik "-" w całym briefie.

## Plik wniosków (`wnioski.md`)

```markdown
# Wnioski radaru: <nazwa>

Agent dopisuje, nigdy nie kasuje. Człowiek może edytować i usuwać.

- **<Wniosek jednym zdaniem>** (obserwacje: N, od <data>): <przykłady z liczbami, po przecinku>. [opcjonalnie: (zaprzeczenie: <kampania>) (sprawdzono: <data>)]
```

Jedna linia na wniosek, tytuł w pogrubieniu, licznik w nawiasie, przykłady po dwukropku. Skrypt czyta ten format, więc trzymaj go znak w znak.

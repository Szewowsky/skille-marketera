# Samokontrola raportu walidacji

Przejdź po każdej walidacji, zanim uznasz raport za gotowy. Dziewięć checków, każdy pass albo fail. Jeden fail = walidator uruchamiany ponownie z informacją, który check padł.

1. **Cytat przy każdym punkcie.** Wszystkie 8 punktów (1, 2, 3, 4, 5, 6, 7a, 7b, 8 - dziewięć linii, bo 7 jest podwójny) ma linię "Dowód:" z tekstem w cudzysłowie. PASS bez cytatu = fail.
2. **Cytaty dosłowne.** Wybrane 3 cytaty sprawdź w ocenianym tekście znak w znak, po normalizacji białych znaków (teksty ze stron mają niełamliwe spacje, które wyglądają jak zwykłe). Parafraza = fail.
3. **Dwa cytaty przy porównaniach.** Punkty 3, 4 i 7a mają cytat z tekstu i cytat z profilu. Brak drugiego = fail.
4. **Zero propozycji.** W raporcie nie ma zdania zaczynającego się od "lepiej", "zamiast tego", "proponuję", "można by", ani żadnego wariantu ocenianego tekstu. Jedno takie = fail.
5. **Werdykt zgodny z regułą.** Liczba NIE w podsumowaniu zgadza się z liczbą punktów NIE wyżej; 0 = do publikacji, 1-2 = do poprawek, 3+ = od nowa. Niezgodność = fail.
6. **Typografia względem profilu.** Punkt 7a odwołuje się do sekcji "Typografia" profilu, nie do ogólnej listy. Jeśli marka pisze półpauzą, a raport karze półpauzę = fail. Jeśli nie ma profilu, punkt 7a ma "brak profilu, pominięto" zamiast werdyktu.
7. **7b jako tabela 20 wzorców.** Każdy wiersz ma "jest" albo "nie ma", każde "jest" ma cytat. Brak tabeli albo "brzmi jak AI" bez wzorca = fail.
8. **Typografia raportu.** Poza cytatami w raporcie nie ma "—" ani "–". Jedna poza cytatem = fail.
9. **Jeden fragment, jedno NIE w punktach 1-6 i 7a.** Ten sam cytat nie jest dowodem NIE w dwóch z tych punktów ani w dwóch wierszach 7b. Tabela 7b może powtarzać fragmenty z punktów wyżej, to nie jest fail. Wiersz 7b z "nie ma (policzone w punkcie X)" = fail, bo tabela ma pokazywać inwentarz.

# Samokontrola profilu po ekstrakcji

Przejdź po zapisaniu `glos.md`. Jeden fail = popraw profil przed pokazaniem go użytkownikowi.

1. **Cytat przy każdej regule.** Każda reguła w sekcjach 1-8 ma cytat z korpusu. Reguła bez cytatu = fail (usuń ją albo znajdź cytat).
2. **Cytaty dosłowne.** Sprawdź wszystkie cytaty skryptem znak w znak wobec plików korpusu, po normalizacji białych znaków. Rozjazd = fail.
3. **Status zgodny z liczbą tekstów.** Poniżej 5 = "za mało danych", 5-9 = "wstępny", 10+ = "pełny". Inny = fail.
4. **Typografia policzona, nie oszacowana.** Sekcja 4 ma liczby dla myślników każdego typu, emoji i cudzysłowów. "Rzadko" zamiast liczby = fail.
5. **Brief rozliczony.** Każdy wpis z briefu jest albo potwierdzony cytatem, albo oznaczony "(z briefu, nie widziane w korpusie)". Wpis bez jednego z dwóch = fail.
6. **Sekcja 9 nietknięta.** Jeśli `glos.md` istniał, sekcja 9 jest identyczna znak w znak z poprzednią. Zmiana = fail.
7. **Figury, które mogą wyglądać na AI, udokumentowane.** Jeśli korpus regularnie używa kontrastu "nie X, tylko Y" albo krótkiej końcówki, sekcja 2 mówi o tym z liczbą. Brak przy częstym użyciu = fail, bo walidator ukarze markę za jej własny styl.

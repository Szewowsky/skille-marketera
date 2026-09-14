# Samokontrola tabeli gotowości

Przejdź przed pokazaniem tabeli. Sześć checków, pass albo fail. Jeden fail = popraw tabelę.

1. **Cztery skille rozliczone.** Tabela ma wiersz dla każdego skilla z inwentarza (więcej tylko przy agencji: jeden na folder klienta). Brak wiersza dla skilla niezainstalowanego = fail (ma być `nie zainstalowany`).
2. **Stan z pliku, nie z pamięci.** Każdy stan `w toku x/y` zgadza się z tabelą kroków w `config.md` tego skilla: x = liczba wierszy `gotowe` albo `pominięte`, y = liczba wszystkich wierszy, "następny" = pierwszy wiersz bez tych stanów. Rozjazd = fail.
3. **Klucz bez wartości.** Kolumna klucz zawiera wyłącznie `jest`, `brak`, `nie dotyczy` albo `częściowo: brak <nazwa klucza>` (nazwa zmiennej albo usługi, np. Apify). Fragment klucza, e-mail konta albo ścieżka do pliku z kluczem = fail.
4. **Następny ruch po polsku.** Zdanie bez nazw plików, flag i poleceń. Jedno = fail.
5. **Kolejność uzasadniona.** Propozycja kolejności pomija skille `gotowe` i zaczyna od tego, który wymaga od użytkownika najmniej. Skill `gotowy` w propozycji = fail.
6. **Typografia.** Krótki myślnik "-", zero "—" i "–".

# Samokontrola po przekazaniu

1. Gałąź Konfiguracja wybranego skilla poszła od pierwszego kroku bez `gotowe` ani `pominięte`, nie od K1.
2. Pytania padały jedno naraz i tylko z tego skilla; żadnego pytania z innego skilla w tym samym przebiegu.
3. Po zakończeniu albo przerwaniu użytkownik zobaczył tabelę gotowości ze zmienionym wierszem.

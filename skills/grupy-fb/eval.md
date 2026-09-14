# Samokontrola raportu z grup

Przejdź po każdym sprawdzeniu, zanim pokażesz raport. Jeden fail = popraw raport.

1. **Nowe posty rozliczone.** Liczba postów w sekcjach (wzmianki + "O co pytają" + "Na co narzekają" + "Co pokazują", zsumowane po osobach, + pominięte) równa `nowe` z wyjścia skryptu. Post wklejony do kilku grup liczy się raz. Post zgubiony = fail.
2. **Wzmianki kompletne.** Każdy post z niepustym `wzmianki_marki` stoi w "Wzmianki o marce" z tonem, kontekstem, adresem posta i zdaniem "co zrobić". Brak = fail.
3. **Tylko imię i inicjał.** W raporcie nie ma żadnego ciągu wyglądającego jak "Imię Nazwisko" poza nazwami firm i osób publicznych, które są marką z `config.md`. Pełne nazwisko autora albo komentującego = fail.
4. **Bez linków do profili.** Żaden adres `facebook.com/<profil>` ani `facebook.com/profile.php`. Adresy postów w grupach (`/groups/.../permalink/`) są w porządku.
5. **Cytaty krótkie.** Żaden dosłowny fragment dłuższy niż jedno zdanie.
6. **Temat przesiał.** Ogłoszenia o pracę, zlecenia, memy bez treści i sprzedaż nie stoją w "O co pytają", "Na co narzekają" ani "Co pokazują"; są policzone w "Pominięte". Opis własnego rozwiązania stoi w "Co pokazują", nie zniknął z raportu i nie wylądował w "Pominiętych" = fail.
7. **Jedno "co z tym zrobić" na temat**, zdanie, wykonalne w tym tygodniu. Brak albo akapit = fail.
8. **Liczby ze skryptu.** Koszt, budżet, liczby postów i zasięgi zgadzają się z plikiem `surowe/` (budżet to stan po runie, pole `budzet`). Liczba z pamięci = fail.
9. **Typografia i język.** Krótki myślnik, zero "—" i "–" poza cytatami, zero słów scrape / dedup / JSON w tekście raportu.

# Samokontrola po Dodaniu grupy

1. Adres zawiera `facebook.com/groups/` i stoi w tabeli Grupy z nazwą i uwagą.
2. Użytkownik dostał potwierdzenie jednym zdaniem i pytanie, czy sprawdzić tę grupę od razu.

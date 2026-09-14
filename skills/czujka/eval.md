# Samokontrola raportu ze sprawdzenia

Przejdź po każdym sprawdzeniu, zanim pokażesz raport. Osiem checków, każdy pass albo fail. Jeden fail = popraw raport przed pokazaniem.

1. **Każdy cel rozliczony.** Liczba etykiet w raporcie (Istotne + Bez istotnych zmian + Nie udało się sprawdzić + Stan wyjściowy) równa liczbie wpisów w `config.md`. Brakujący cel = fail.
2. **Było -> jest z dosłownymi fragmentami.** Każda zmiana istotna ma oba fragmenty po obu stronach strzałki, znak w znak z snapshotu i z nowego stanu. "Zmieniła się cena" bez kwot = fail.
3. **Odliczanie w drobiazgach.** Żadna zmiana wartości odliczania czasu, rotującej opinii ani daty w stopce nie stoi w sekcji Istotne. Jedna taka = fail.
4. **Baza bez zmian.** Gdy dla celu nie było poprzedniego snapshotu, raport ma dla niego linię w "Stan wyjściowy", a nie jakąkolwiek zmianę. Zmiana wymyślona na bazie = fail.
5. **Jedno zdanie znaczenia, tylko przy istotnych.** Każda zmiana istotna ma dokładnie jedno zdanie "co to może znaczyć"; drobiazgi i baza nie mają żadnego. Brak albo akapit = fail.
6. **Padnięty cel osobno.** Cel, którego nie udało się pobrać, stoi w "Nie udało się sprawdzić" z powodem, a jego snapshot z poprzedniego razu jest nietknięty. Nadpisany snapshot pustym stanem = fail.
7. **Bez danych osobowych i żargonu.** W raporcie nie ma adresów e-mail, nazwisk osób prywatnych, słów "scrape", "diff", "snapshot", "DOM". Jedno = fail.
8. **Typografia.** W raporcie krótki myślnik "-", strzałka "->" tylko w parach było/jest, zero "—" i "–" poza cytatami ze stron. Jedna poza cytatem = fail.

# Samokontrola po Dodaniu

1. Nowy wpis ma etykietę, adres, notatkę "ważne" i stoi we właściwej sekcji (Strony albo Reklamy).
2. Adres został pobrany raz i odpowiedział; jeśli nie, wpis ma uwagę "nie potwierdzony" i użytkownik o tym wie.
3. Użytkownik dostał pytanie, czy zrobić pierwsze pobranie teraz.

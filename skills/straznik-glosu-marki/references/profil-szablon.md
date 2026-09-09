# Szablon profilu głosu marki (glos.md)

Profil to czytelny markdown, który przełożony może przeczytać i poprawić. Osiem sekcji, każda z 1-3 cytatami z korpusu jako dowodem, że reguła nie jest zmyślona. Sekcja 9 należy do człowieka.

```markdown
# Głos marki: <nazwa>

Źródło: <ile tekstów, skąd, data>. Status: pełny (10+ tekstów) / wstępny (5-9 tekstów) / za mało danych (<5).
<jeśli był brief:> Brief: <plik>. Wpisy z briefu niepotwierdzone w korpusie oznaczone "(z briefu, nie widziane w korpusie)".

## 1. Rytm i długość zdań
<średnia, rozrzut, czy miesza krótkie z długimi, typowy akapit>
Cytat: "..."

## 2. Otwarcia
<jakimi typami pierwszego zdania marka zaczyna: sytuacja, liczba, pytanie, teza, zwrot do czytelnika... - z częstością w korpusie>
Cytat: "..."

## 3. Forma
<Ty / Pan / my / bezosobowo; czy marka mówi o sobie "my" czy z nazwy>
Cytat: "..."

## 4. Emoji i typografia
<emoji: tak/nie/gdzie; myślnik: "-" / "–" / "—" z liczbą wystąpień; cudzysłowy; wypunktowania; nawiasy>
Cytat: "..."

## 5. Słowa firmowe
<słowa i frazy, które wracają i są cechą, nie przypadkiem; z liczbą wystąpień>
- "..." (N razy)

## 6. Słowa zakazane
<czego marka nie mówi; z korpusu (przez nieobecność przy temacie, gdzie inni by użyli) i z briefu>
- "..." - <skąd: korpus / brief / brief, nie widziane w korpusie>

## 7. Czego marka nigdy nie robi
<konstrukcje, tony, chwyty nieobecne w korpusie: np. nie obiecuje skrótów, nie używa wykrzykników, nie pisze o sobie w trzeciej osobie>

## 8. Zdania-wzorce
<5-8 zdań z korpusu, które najlepiej pokazują głos; dosłownie>

## 9. Reguły ręczne
<!-- Sekcja człowieka. Ekstraktor jej nie dotyka przy ponownym uruchomieniu. -->
```

## Zasady ekstraktora

- Każda reguła ma cytat z korpusu. Reguła bez cytatu nie wchodzi.
- Brief (jeśli jest) wchodzi do sekcji 5 i 6. Każdy wpis z briefu ekstraktor sprawdza w korpusie: potwierdzony (podaj cytat) albo "(z briefu, nie widziane w korpusie)".
- Przy ponownym uruchomieniu na istniejącym `glos.md`: sekcje 1-8 przepisz, sekcję 9 przenieś znak w znak.
- Mniej niż 5 tekstów: profil powstaje ze statusem "za mało danych" i ostrzeżeniem, że walidacja na nim będzie zgadywaniem. 5-9: "wstępny". 10+: "pełny".

# Przykład tabeli gotowości

Projekt fikcyjnej marki Pracownia Zielnik po instalacji wszystkich skilli i po skonfigurowaniu czujki do bazy.

| Skill | Stan | Klucz | Następny ruch |
|---|---|---|---|
| Strażnik głosu marki | nie zaczęty | nie dotyczy | Zbierzemy teksty marki (strona, newslettery, posty) i wyprowadzimy z nich profil głosu. |
| Poranny radar | nie zaczęty | nie dotyczy | Potrzebny jeden eksport kampanii z narzędzia mailingowego, resztę policzy skrypt. |
| Grupy FB | nie zaczęty | brak | Najpierw darmowe konto Apify i klucz, potem lista 2-5 grup. |
| Czujka | w toku 4/5, następny: K5 Kadencja | częściowo: brak Apify | Czeka na pierwsze porównanie po zapisanej bazie, potem wybór rutyny; do reklam brakuje jeszcze klucza Apify. |

Python 3 jest. W `.gitignore` brakuje wpisu `/radar*/**` - dopisać?

Proponuję kolejność: strażnik, radar, grupy, a czujka po jutrzejszym sprawdzeniu. Od którego zaczynamy, czy lecimy po kolei?

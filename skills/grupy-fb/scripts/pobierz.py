#!/usr/bin/env python3
"""Pobiera posty z grup Facebook przez Apify (REST), anonimizuje autorów, odsiewa
widziane i zaznacza wzmianki o marce. Agent dostaje tylko wynik tego skryptu,
więc pełnych nazwisk ani linków do profili nigdy nie widzi.

Użycie:
  pobierz.py URL [URL ...] [--limit 20] [--widziane grupy-fb/widziane.json]
             [--marka "fraza;fraza;https://..."] [--wyjscie plik.json]
             [--z-pliku surowe.json] [--oznacz-widziane]

Token Apify: zmienna środowiskowa APIFY_API_TOKEN. Bez tokena skrypt kończy się
błędem "brak_tokena" (chyba że --z-pliku). Tylko biblioteka standardowa.
"""
import argparse
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request

ACTOR = "apify~facebook-groups-scraper"
API = "https://api.apify.com/v2"


def http_json(url, data=None, timeout=60):
    req = urllib.request.Request(url, method="POST" if data is not None else "GET")
    body = None
    if data is not None:
        req.add_header("Content-Type", "application/json")
        body = json.dumps(data).encode("utf-8")
    with urllib.request.urlopen(req, body, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def anonimizuj(nazwa):
    """'Anna Kowalska-Nowak' -> 'Anna K.'; 'Anna' -> 'Anna'; puste -> 'Ktoś'."""
    if not nazwa or not str(nazwa).strip():
        return "Ktoś"
    czesci = str(nazwa).strip().split()
    if len(czesci) == 1:
        return czesci[0]
    return f"{czesci[0]} {czesci[1][0]}."


def pierwsze_zdanie(tekst):
    tekst = re.sub(r"\s+", " ", tekst or "").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", tekst)
    zd = m.group(1) if m else tekst
    return zd[:200]


def rdzenie(tekst):
    """Polska odmiana: słowa od 5 liter obcinamy o 2 znaki, 'Pracownia'/'Pracowni'/'Pracownię' -> 'pracown'."""
    slowa = re.findall(r"[\w@./-]+", tekst.lower())
    return " ".join(w[:-2] if len(w) >= 5 and not re.search(r"[./@]", w) else w for w in slowa)


def wzmianki(post, frazy):
    """Fraza z kropką, ukośnikiem albo @ (link, domena) musi wystąpić dosłownie; nazwa dopasowuje się po rdzeniach słów, żeby złapać odmianę."""
    if not frazy:
        return []
    pola = [post.get("text") or "", post.get("shared_link") or "", post.get("image_text") or ""]
    pola += [k.get("text") or "" for k in post.get("top_comments", [])]
    blob = " ".join(pola)
    blob_l, blob_r = blob.lower(), " " + rdzenie(blob) + " "
    trafione = []
    for f in frazy:
        if re.search(r"[./@]", f):
            if f.lower() in blob_l:
                trafione.append(f)
        elif f.lower() in blob_l or (" " + rdzenie(f) + " ") in blob_r:
            trafione.append(f)
    return trafione


def normalizuj(item, frazy):
    komentarze = []
    for k in (item.get("topComments") or [])[:3]:
        komentarze.append({
            "autor": anonimizuj(k.get("profileName")),
            "text": (k.get("text") or "").strip()[:500],
        })
    ocr = " ".join(
        (a.get("ocrText") or "") for a in (item.get("attachments") or []) if a.get("ocrText")
    ).strip()
    post = {
        "post_url": item.get("url"),
        "post_id": item.get("legacyId") or item.get("id"),
        "grupa": item.get("groupTitle") or item.get("facebookUrl"),
        "data": item.get("time"),
        "autor": anonimizuj((item.get("user") or {}).get("name")),
        "text": (item.get("text") or "").strip(),
        "shared_link": item.get("link"),
        "image_text": ocr[:1000] or None,
        "polubienia": item.get("likesCount", 0),
        "komentarze_liczba": item.get("commentsCount", 0),
        "udostepnienia": item.get("sharesCount", 0),
        "top_comments": komentarze,
    }
    post["wzmianki_marki"] = wzmianki(post, frazy)
    return post


def budzet(token):
    try:
        d = http_json(f"{API}/users/me/limits?token={token}")["data"]
        used = d["current"]["monthlyUsageUsd"]
        cap = d["limits"]["maxMonthlyUsageUsd"]
        return {"zuzyte_usd": round(used, 3), "limit_usd": cap, "zostalo_usd": round(cap - used, 3)}
    except Exception as e:  # noqa: BLE001
        return {"blad": f"nie udało się odczytać limitów: {e}"}


def uruchom_apify(token, urls, limit):
    wejscie = {"startUrls": [{"url": u} for u in urls], "resultsLimit": limit, "viewOption": "CHRONOLOGICAL"}
    start = http_json(f"{API}/acts/{ACTOR}/runs?token={token}", wejscie)["data"]
    run_id = start["id"]
    status = start.get("status")
    koszt = 0.0
    dsid = start.get("defaultDatasetId")
    for _ in range(60):
        r = http_json(f"{API}/actor-runs/{run_id}?token={token}")["data"]
        status = r["status"]
        dsid = r.get("defaultDatasetId", dsid)
        koszt = r.get("usageTotalUsd", koszt) or 0.0
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        time.sleep(10)
    items = []
    if status == "SUCCEEDED" and dsid:
        items = http_json(f"{API}/datasets/{dsid}/items?token={token}&clean=true&format=json")
    return {"run_id": run_id, "status": status, "koszt_usd": round(float(koszt), 4)}, items


def wczytaj_widziane(path):
    if not path or not os.path.exists(path):
        return {"version": 1, "ostatni_run": None, "widziane": {}, "statystyki": {"runy": 0, "posty": 0, "koszt_usd": 0.0}}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return {"version": 1, "ostatni_run": None, "widziane": {}, "statystyki": {"runy": 0, "posty": 0, "koszt_usd": 0.0}}


def zapisz_widziane(path, dane):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--widziane", default=None)
    ap.add_argument("--marka", default="", help="frazy i linki do pilnowania, rozdzielone ';'")
    ap.add_argument("--wyjscie", default=None)
    ap.add_argument("--z-pliku", default=None, help="surowe itemy aktora z pliku JSON zamiast Apify (test, zapas)")
    ap.add_argument("--oznacz-widziane", action="store_true")
    a = ap.parse_args()

    frazy = [f.strip() for f in a.marka.split(";") if f.strip()]
    wynik = {"data": time.strftime("%Y-%m-%d %H:%M"), "grupy": a.urls, "limit": a.limit}

    if a.z_pliku:
        with open(a.z_pliku, encoding="utf-8") as f:
            items = json.load(f)
        wynik["run"] = {"run_id": None, "status": "Z_PLIKU", "koszt_usd": 0.0}
        wynik["budzet"] = None
    else:
        token = os.environ.get("APIFY_API_TOKEN", "").strip()
        if not token:
            print(json.dumps({"blad": "brak_tokena", "jak_naprawic": "ustaw APIFY_API_TOKEN (klucz z konsoli Apify, plan Free wystarcza)"}, ensure_ascii=False))
            sys.exit(2)
        if not a.urls:
            print(json.dumps({"blad": "brak_grup"}, ensure_ascii=False))
            sys.exit(2)
        wynik["budzet"] = budzet(token)
        if wynik["budzet"].get("zostalo_usd") is not None and wynik["budzet"]["zostalo_usd"] <= 0:
            wynik["blad"] = "limit_wyczerpany"
            print(json.dumps(wynik, ensure_ascii=False, indent=2))
            sys.exit(3)
        try:
            wynik["run"], items = uruchom_apify(token, a.urls, a.limit)
        except urllib.error.HTTPError as e:
            tresc = e.read().decode("utf-8", "replace")[:300]
            wynik["blad"] = "apify_http_%s" % e.code
            wynik["szczegoly"] = tresc
            print(json.dumps(wynik, ensure_ascii=False, indent=2))
            sys.exit(4)
        if wynik["run"]["status"] != "SUCCEEDED":
            wynik["blad"] = "run_" + wynik["run"]["status"].lower()

    widziane = wczytaj_widziane(a.widziane)
    znane = widziane.get("widziane", {})
    nowe, pominiete = [], 0
    for it in items:
        p = normalizuj(it, frazy)
        if p["post_url"] and p["post_url"] in znane:
            pominiete += 1
            continue
        nowe.append(p)

    wynik["pobrane"] = len(items)
    wynik["pominiete_widziane"] = pominiete
    wynik["nowe"] = len(nowe)
    wynik["wzmianki_marki"] = sum(1 for p in nowe if p["wzmianki_marki"])
    wynik["posty"] = nowe

    if a.oznacz_widziane and a.widziane:
        dzis = time.strftime("%Y-%m-%d")
        for p in nowe:
            if p["post_url"]:
                znane[p["post_url"]] = dzis
        # sprzątanie: wpisy starsze niż 60 dni
        try:
            prog = time.strftime("%Y-%m-%d", time.localtime(time.time() - 60 * 86400))
            for k in [k for k, v in znane.items() if isinstance(v, str) and v < prog]:
                del znane[k]
        except Exception:  # noqa: BLE001
            pass
        st = widziane.setdefault("statystyki", {"runy": 0, "posty": 0, "koszt_usd": 0.0})
        st["runy"] = st.get("runy", 0) + 1
        st["posty"] = st.get("posty", 0) + len(nowe)
        st["koszt_usd"] = round(st.get("koszt_usd", 0.0) + (wynik.get("run") or {}).get("koszt_usd", 0.0), 4)
        widziane["widziane"] = znane
        widziane["ostatni_run"] = wynik["data"]
        zapisz_widziane(a.widziane, widziane)
        wynik["widziane_zapisane"] = a.widziane

    out = json.dumps(wynik, ensure_ascii=False, indent=2)
    if a.wyjscie:
        os.makedirs(os.path.dirname(a.wyjscie) or ".", exist_ok=True)
        with open(a.wyjscie, "w", encoding="utf-8") as f:
            f.write(out)
        print(json.dumps({k: v for k, v in wynik.items() if k != "posty"}, ensure_ascii=False, indent=2))
        print(f"posty zapisane do: {a.wyjscie}")
    else:
        print(out)


if __name__ == "__main__":
    main()

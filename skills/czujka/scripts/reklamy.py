#!/usr/bin/env python3
"""Pobiera aktywne reklamy konta z Meta Ads Library przez aktora Apify (REST).

Wejście do aktora jest tu ustalone i sprawdzone - NIE układaj go od nowa.
Pierwsze pobranie z wejściem ułożonym z pamięci (pola `urls`, `count`)
wróciło puste; działa wyłącznie zestaw pól z funkcji `wejscie_aktora`.

Użycie:

    APIFY_API_TOKEN=$(security find-generic-password -a APIFY_API_TOKEN -s <usługa> -w) \\
      python3 .claude/skills/czujka/scripts/reklamy.py \\
      --page-id <id strony> \\
      --wyjscie czujka/snapshoty/_surowe/<etykieta>-reklamy.json

Argumenty:
    --page-id   identyfikator strony na Facebooku (`view_all_page_id`), wymagany
    --country   kraj wyświetlania reklam, domyślnie PL
    --limit     ile reklam najwyżej pobrać, domyślnie 100
    --wyjscie   ścieżka pliku JSON z wynikiem, wymagana

Na wyjściu (plik JSON): run_id, status, koszt_usd, pobrano, ile, ucieta,
items (surowe reklamy) oraz kreacje (zgrupowane po treści, z liczbą kopii).
Na stdout jedna linia JSON z podsumowaniem.

Token bierzemy wyłącznie ze zmiennej APIFY_API_TOKEN - nigdy z pliku.
Brak tokena albo odpowiedź 401/402/403 (także "hard limit exceeded") kończy
pracę kodem 1 bez ponawiania: jeden run dziennie, budżet aktora jest wspólny.

Aktor zwraca reklamy od najnowszych (sortBy: mostRecent), więc gdy `ucieta`
jest prawdziwe, poza listą zostały NAJSTARSZE reklamy - przy następnym
sprawdzeniu podnieś --limit do 200.

Tylko biblioteka standardowa.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

AKTOR = "bo5X18oGenWEV9vVo"  # igolaizola/facebook-ad-library-scraper
API = "https://api.apify.com/v2"
ODSTEP_S = 10
MAKS_PROB = 120


def wejscie_aktora(page_id, country, limit):
    """Sprawdzone wejście aktora. Nie zmieniaj nazw pól ani ich nie pomijaj."""
    return {
        "pageId": str(page_id),
        "country": country,
        "maxItems": int(limit),
        "category": "all",
        "mediaType": "all",
        "sortBy": "mostRecent",
        "activeStatus": "active",
        "advertisers": [],
        "fetchDetails": False,
    }


def http_json(url, dane=None, timeout=120):
    req = urllib.request.Request(url, method="POST" if dane is not None else "GET")
    body = None
    if dane is not None:
        req.add_header("Content-Type", "application/json")
        body = json.dumps(dane).encode("utf-8")
    with urllib.request.urlopen(req, body, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _pole(item, *nazwy):
    """Pierwsza niepusta wartość spośród podanych pól - w item albo w snapshot."""
    snapshot = item.get("snapshot") or {}
    if not isinstance(snapshot, dict):
        snapshot = {}
    for nazwa in nazwy:
        for zrodlo in (item, snapshot):
            wartosc = zrodlo.get(nazwa)
            if isinstance(wartosc, dict):
                wartosc = wartosc.get("text") or wartosc.get("markup") or ""
            if wartosc not in (None, "", [], {}):
                return wartosc
    return ""


def data_startu(item):
    """Data startu reklamy jako YYYY-MM-DD; pusty tekst, gdy brak."""
    ts = _pole(item, "start_date", "startDate", "start_date_unix", "ad_delivery_start_time")
    if isinstance(ts, str):
        ts = ts.strip()
        if ts.isdigit():
            ts = int(ts)
        elif len(ts) >= 10 and ts[4] == "-":
            return ts[:10]
        else:
            return ""
    if isinstance(ts, (int, float)) and ts > 0:
        return datetime.fromtimestamp(float(ts), timezone.utc).strftime("%Y-%m-%d")
    return ""


def platformy(item):
    """Platformy wyświetlania, posortowane, żeby kolejność nie psuła porównania."""
    wartosc = _pole(item, "publisher_platform", "publisherPlatform", "platforms")
    if isinstance(wartosc, str):
        wartosc = [wartosc]
    if not isinstance(wartosc, list):
        return []
    return sorted({str(p).strip().lower() for p in wartosc if str(p).strip()})


def tekst_body(item):
    wartosc = _pole(item, "body", "ad_creative_body", "text")
    return " ".join(str(wartosc).split())


def pierwsze_zdanie(tekst, maks=220):
    tekst = " ".join(str(tekst).split())
    if not tekst:
        return ""
    najblizszy = len(tekst)
    for znak in (". ", "! ", "? ", "… "):
        pozycja = tekst.find(znak)
        if 0 <= pozycja < najblizszy:
            najblizszy = pozycja + 1
    if najblizszy < len(tekst):
        return tekst[:najblizszy].strip()
    return tekst[:maks].strip()


def adres(item):
    """Adres docelowy albo caption - to, co identyfikuje kreację poza treścią."""
    return str(_pole(item, "link_url", "linkUrl", "caption", "link_description") or "").strip()


def cta(item):
    return str(_pole(item, "cta_text", "ctaText", "call_to_action") or "").strip()


def klucz_kreacji(item):
    """Klucz porównania: data startu, adres/caption, wezwanie, platformy, pierwsze zdanie."""
    return (
        data_startu(item),
        adres(item),
        cta(item),
        tuple(platformy(item)),
        pierwsze_zdanie(tekst_body(item)),
    )


def grupuj(items):
    """Zwija reklamy o tej samej treści kreacji w jedną pozycję z liczbą kopii."""
    zebrane = {}
    kolejnosc = []
    for item in items:
        if not isinstance(item, dict):
            continue
        klucz = klucz_kreacji(item)
        if klucz not in zebrane:
            zebrane[klucz] = {
                "start": klucz[0],
                "adres": klucz[1],
                "cta_text": klucz[2],
                "platformy": list(klucz[3]),
                "pierwsze_zdanie": klucz[4],
                "kopie": 0,
            }
            kolejnosc.append(klucz)
        zebrane[klucz]["kopie"] += 1
    return [zebrane[k] for k in kolejnosc]


def blad(tresc, kod=1):
    print(json.dumps(tresc, ensure_ascii=False))
    sys.exit(kod)


def blad_http(e):
    """Każdy błąd HTTP kończy pracę bez ponawiania.

    401/402/403 oraz treść z "hard limit" to wspólny budżet Apify - ponawianie
    tylko pali limit, więc wychodzimy od razu z kodem i treścią odpowiedzi.
    """
    szczegoly = e.read().decode("utf-8", "replace")[:600]
    blad({"blad": f"http_{e.code}", "szczegoly": szczegoly})


def pobierz(page_id, country, limit, token):
    try:
        start = http_json(f"{API}/acts/{AKTOR}/runs?token={token}", wejscie_aktora(page_id, country, limit))["data"]
    except urllib.error.HTTPError as e:
        blad_http(e)
    except urllib.error.URLError as e:
        blad({"blad": "brak_polaczenia", "szczegoly": str(e.reason)[:600]})

    run_id = start["id"]
    status = start.get("status")
    dsid = start.get("defaultDatasetId")
    koszt = 0.0
    komunikat = start.get("statusMessage") or ""

    for _ in range(MAKS_PROB):
        time.sleep(ODSTEP_S)
        try:
            r = http_json(f"{API}/actor-runs/{run_id}?token={token}")["data"]
        except urllib.error.HTTPError as e:
            blad_http(e)
        status = r["status"]
        dsid = r.get("defaultDatasetId") or dsid
        koszt = r.get("usageTotalUsd") or 0.0
        komunikat = r.get("statusMessage") or komunikat
        print(f"... {status}", file=sys.stderr)
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT", "TIMED_OUT"):
            break

    # Wyczerpany budżet Apify potrafi wrócić komunikatem runu, nie kodem HTTP.
    if "hard limit" in str(komunikat).lower():
        blad({"blad": "http_402", "szczegoly": str(komunikat)[:600]})

    items = []
    if status == "SUCCEEDED" and dsid:
        try:
            items = http_json(f"{API}/datasets/{dsid}/items?token={token}&clean=true&format=json")
        except urllib.error.HTTPError as e:
            blad_http(e)
    if not isinstance(items, list):
        items = []
    return run_id, status, float(koszt), items


def main():
    p = argparse.ArgumentParser(description="Reklamy konta z Meta Ads Library przez aktora Apify.")
    p.add_argument("--page-id", required=True, help="identyfikator strony na Facebooku (view_all_page_id)")
    p.add_argument("--country", default="PL", help="kraj wyświetlania, domyślnie PL")
    p.add_argument("--limit", type=int, default=100, help="ile reklam najwyżej pobrać, domyślnie 100")
    p.add_argument("--wyjscie", required=True, help="ścieżka pliku JSON z wynikiem")
    a = p.parse_args()

    token = os.environ.get("APIFY_API_TOKEN", "").strip()
    if not token:
        blad({"blad": "brak_tokena"})

    run_id, status, koszt, items = pobierz(a.page_id, a.country, a.limit, token)

    kreacje = grupuj(items)
    wynik = {
        "run_id": run_id,
        "status": status,
        "koszt_usd": round(koszt, 4),
        "pobrano": time.strftime("%Y-%m-%d %H:%M"),
        "ile": len(items),
        "ucieta": len(items) == a.limit,
        "items": items,
        "kreacje": kreacje,
    }
    with open(a.wyjscie, "w", encoding="utf-8") as f:
        json.dump(wynik, f, ensure_ascii=False)

    print(json.dumps({
        "run_id": run_id,
        "status": status,
        "koszt_usd": wynik["koszt_usd"],
        "ile": wynik["ile"],
        "ucieta": wynik["ucieta"],
        "kreacje": len(kreacje),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

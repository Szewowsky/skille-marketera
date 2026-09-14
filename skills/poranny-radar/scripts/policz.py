#!/usr/bin/env python3
"""Liczy statystyki kampanii z eksportu mailingowego (CSV) i sprawdza hipotezy
z pliku wniosków. Agent pisze brief na podstawie wyniku, nie liczy sam.

Użycie:
  policz.py radar/zrodla/mailing.csv [--wnioski radar/wnioski.md] [--sprzedaz radar/zrodla/sprzedaz.csv]
            [--ostatnie 12] [--do 2026-09-14] [--wyjscie plik.json]

Wejście: CSV z kolumnami (nazwy dopasowane luźno, po polsku albo po angielsku):
  kampania/name, temat/subject, data/date/sent_at, wyslane/sent, otwarcia/opens, klikniecia/clicks, wypisy/unsubscribes.
  Otwarcia i kliknięcia mogą być liczbą albo procentem ("34.5%").
Tylko biblioteka standardowa.
"""
import argparse
import csv
import json
import re
import statistics as st
import sys
from datetime import datetime

ALIASY = {
    "kampania": ["kampania", "nazwa", "name", "campaign", "campaign name", "campaign_name", "title"],
    "temat": ["temat", "subject", "subject line", "subject_line", "email subject"],
    "data": ["data", "date", "sent", "sent_at", "send date", "send_date", "finished_at", "wysłano", "delivered"],
    "wyslane": ["wyslane", "wysłane", "sent", "recipients", "emails sent", "total recipients", "odbiorcy"],
    "otwarcia": ["otwarcia", "opens", "unique opens", "opens_count", "open rate", "open_rate", "otwarcia_proc"],
    "klikniecia": ["klikniecia", "kliknięcia", "clicks", "unique clicks", "clicks_count", "click rate", "click_rate", "klikniecia_proc"],
    "wypisy": ["wypisy", "unsubscribes", "unsubscribed", "unsubscribes_count", "unsubs"],
}


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").strip().lower().replace("ł", "l").replace("ś", "s").replace("ę", "e").replace("ą", "a")).strip()


def mapuj_kolumny(naglowki):
    n = {norm(h): h for h in naglowki}
    out = {}
    for pole, ali in ALIASY.items():
        for a in ali:
            if norm(a) in n and n[norm(a)] not in out.values():
                out[pole] = n[norm(a)]
                break
    return out


def liczba(v):
    if v is None:
        return None
    s = str(v).strip().replace(" ", "").replace(",", ".")
    if s == "":
        return None
    proc = s.endswith("%")
    s = s.rstrip("%")
    try:
        x = float(s)
    except ValueError:
        return None
    return ("proc", x) if proc else ("n", x)


def procent(wart, baza):
    """wart = ('proc', x) albo ('n', x); zwraca procent 0-100."""
    if wart is None:
        return None
    typ, x = wart
    if typ == "proc":
        return round(x, 2)
    if x <= 1.0 and baza and baza > 1:
        return round(x * 100, 2)  # ułamek 0.345
    if baza:
        return round(x / baza * 100, 2)
    return None


def data_iso(v):
    if not v:
        return None
    v = str(v).strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%d.%m.%Y", "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(v[:19] if "T" in v or ":" in v else v, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return v[:10]


def wczytaj_mailing(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        probka = f.read(4096); f.seek(0)
        try:
            dial = csv.Sniffer().sniff(probka, delimiters=",;\t")
        except csv.Error:
            dial = csv.excel
        rd = csv.DictReader(f, dialect=dial)
        kol = mapuj_kolumny(rd.fieldnames or [])
        brak = [p for p in ("kampania", "data", "wyslane") if p not in kol]
        if brak or ("otwarcia" not in kol and "klikniecia" not in kol):
            return None, {"blad": "brak_kolumn", "brakuje": brak, "znalezione": kol, "naglowki": rd.fieldnames}
        rows = []
        for r in rd:
            wys = liczba(r.get(kol["wyslane"]))
            wys = wys[1] if wys else None
            rows.append({
                "kampania": (r.get(kol["kampania"]) or "").strip(),
                "temat": (r.get(kol.get("temat", ""), "") or "").strip(),
                "data": data_iso(r.get(kol["data"])),
                "wyslane": int(wys) if wys is not None else None,
                "otwarcia_proc": procent(liczba(r.get(kol.get("otwarcia", ""))), wys) if "otwarcia" in kol else None,
                "klikniecia_proc": procent(liczba(r.get(kol.get("klikniecia", ""))), wys) if "klikniecia" in kol else None,
                "wypisy": int(liczba(r.get(kol["wypisy"]))[1]) if "wypisy" in kol and liczba(r.get(kol["wypisy"])) else None,
            })
        return rows, {"kolumny": kol}


def wczytaj_sprzedaz(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        out = []
        for r in rd:
            k = {norm(a): b for a, b in r.items()}
            def g(*names):
                for n_ in names:
                    if norm(n_) in k:
                        return k[norm(n_)]
                return None
            p = liczba(g("przychod_pln", "przychod", "revenue", "kwota"))
            z = liczba(g("zamowienia", "orders", "zamówienia", "sprzedaz"))
            out.append({"od": data_iso(g("tydzien_od", "od", "from", "week_start", "data")), "do": data_iso(g("tydzien_do", "do", "to", "week_end")),
                        "przychod_pln": p[1] if p else None, "zamowienia": int(z[1]) if z else None})
        return out


def wczytaj_wnioski(path):
    """Wnioski w markdown: linie zaczynające się od '- ' z '**tytuł**' i 'obserwacje: N'."""
    try:
        txt = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        return []
    out = []
    for m in re.finditer(r"^- \*\*(.+?)\*\*(.*)$", txt, re.M):
        tyt, reszta = m.group(1).strip(), m.group(2)
        obs = re.search(r"obserwacj\w*:\s*(\d+)", reszta, re.I)
        out.append({"wniosek": tyt, "obserwacje": int(obs.group(1)) if obs else None, "linia": m.group(0)})
    return out


def ma_liczbe(temat):
    return bool(re.search(r"\d", temat or ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mailing")
    ap.add_argument("--wnioski", default=None)
    ap.add_argument("--sprzedaz", default=None)
    ap.add_argument("--ostatnie", type=int, default=12)
    ap.add_argument("--do", default=None, help="licz tylko kampanie do tej daty włącznie (okno 'tydzień później' w demie)")
    ap.add_argument("--wyjscie", default=None)
    a = ap.parse_args()

    rows, meta = wczytaj_mailing(a.mailing)
    if rows is None:
        print(json.dumps(meta, ensure_ascii=False, indent=2)); sys.exit(2)
    rows = [r for r in rows if r["data"]]
    if a.do:
        rows = [r for r in rows if r["data"] <= a.do]
    rows.sort(key=lambda r: r["data"])
    rows = rows[-a.ostatnie:]
    wyn = {"zrodlo": a.mailing, "kampanii": len(rows), "okno_do": a.do, "kolumny": meta["kolumny"], "kampanie": rows}
    if not rows:
        wyn["blad"] = "brak_kampanii"; print(json.dumps(wyn, ensure_ascii=False, indent=2)); sys.exit(3)

    def kol(k):
        return [r[k] for r in rows if r.get(k) is not None]

    def med(xs):
        return round(st.median(xs), 2) if xs else None

    def sr(xs):
        return round(st.mean(xs), 2) if xs else None

    ors, ctrs, wyp = kol("otwarcia_proc"), kol("klikniecia_proc"), kol("wypisy")
    wyn["srednie"] = {"otwarcia_proc": sr(ors), "klikniecia_proc": sr(ctrs), "wypisy_mediana": med(wyp), "wypisy_srednia": sr(wyp)}
    ost = rows[-1]
    wyn["ostatnia"] = ost

    # Sygnały: odchylenia od mediany
    sygnaly = []
    mo, mc, mw = med(ors), med(ctrs), med(wyp)
    for r in rows:
        if r["otwarcia_proc"] is not None and mo and r["otwarcia_proc"] < mo * 0.8:
            sygnaly.append({"typ": "traci", "pole": "otwarcia", "kampania": r["kampania"], "data": r["data"], "wartosc": r["otwarcia_proc"], "mediana": mo,
                            "opis": f"{r['kampania']}: otwarcia {r['otwarcia_proc']}% przy medianie {mo}%"})
        if r["klikniecia_proc"] is not None and mc and r["klikniecia_proc"] > mc * 1.5:
            sygnaly.append({"typ": "zaskoczylo", "pole": "klikniecia", "kampania": r["kampania"], "data": r["data"], "wartosc": r["klikniecia_proc"], "mediana": mc,
                            "opis": f"{r['kampania']}: kliknięcia {r['klikniecia_proc']}% przy medianie {mc}%"})
        if r["wypisy"] is not None and mw and r["wypisy"] > mw * 2.5:
            sygnaly.append({"typ": "traci", "pole": "wypisy", "kampania": r["kampania"], "data": r["data"], "wartosc": r["wypisy"], "mediana": mw,
                            "opis": f"{r['kampania']}: {r['wypisy']} wypisów przy medianie {mw}"})
    wyn["sygnaly"] = sygnaly

    # Hipotezy wbudowane (agent może dopisać własne w wnioski.md, te są liczone zawsze)
    z = [r for r in rows if ma_liczbe(r["temat"]) and r["klikniecia_proc"] is not None]
    b = [r for r in rows if not ma_liczbe(r["temat"]) and r["klikniecia_proc"] is not None]
    wyn["hipotezy"] = {
        "temat_z_liczba": {"z_liczba_n": len(z), "z_liczba_ctr": sr([r["klikniecia_proc"] for r in z]),
                            "bez_liczby_n": len(b), "bez_liczby_ctr": sr([r["klikniecia_proc"] for r in b]),
                            "potwierdza": bool(z and b and sr([r["klikniecia_proc"] for r in z]) > sr([r["klikniecia_proc"] for r in b])),
                            "przyklady_z_liczba": [r["temat"] for r in z][-3:]},
    }
    # Dzień tygodnia wysyłki
    dni = {}
    for r in rows:
        try:
            d = datetime.strptime(r["data"], "%Y-%m-%d").strftime("%A")
        except ValueError:
            continue
        dni.setdefault(d, []).append(r["otwarcia_proc"])
    wyn["hipotezy"]["dzien_wysylki"] = {d: {"n": len([x for x in v if x is not None]), "otwarcia_sr": sr([x for x in v if x is not None])} for d, v in dni.items()}

    if a.wnioski:
        wyn["wnioski_z_pliku"] = wczytaj_wnioski(a.wnioski)
    if a.sprzedaz:
        try:
            tyg = wczytaj_sprzedaz(a.sprzedaz)
            wyn["sprzedaz"] = {"tygodnie": tyg, "suma_pln": round(sum(t["przychod_pln"] or 0 for t in tyg), 2), "zamowienia": sum(t["zamowienia"] or 0 for t in tyg)}
        except Exception as e:  # noqa: BLE001
            wyn["sprzedaz"] = {"blad": f"nie udało się odczytać: {e}"}

    out = json.dumps(wyn, ensure_ascii=False, indent=2)
    if a.wyjscie:
        open(a.wyjscie, "w", encoding="utf-8").write(out)
        print(json.dumps({k: v for k, v in wyn.items() if k != "kampanie"}, ensure_ascii=False, indent=2))
    else:
        print(out)


if __name__ == "__main__":
    main()

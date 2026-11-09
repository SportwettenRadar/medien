#!/usr/bin/env python3
"""Abgleich: alle Zahlen der Homepage gegen daten/ergebnisse.json und daten/signale.json (Tage, Wochen, Monate, Jahr, Ø-Quote).
Aufruf: python3 abgleich_zahlen.py --medien <dir> --homepage <dir>
Prüft trackrecord-daten.js, die statischen Monatsseiten und die gerenderte Startseite. Ausgabe: Liste der Abweichungen (leer = alles gleich).
Exit-Code 0 = alles gleich, 1 = Abweichungen."""
import argparse, json, os, re, subprocess, sys


def de(n, k=1):
    return f"{abs(n):,.{k}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def sg(n, k=1):
    return ("+" if n > 0 else "−" if n < 0 else "") + de(n, k)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--medien", required=True)
    ap.add_argument("--homepage", required=True)
    a = ap.parse_args()
    d = json.load(open(os.path.join(a.medien, "daten/ergebnisse.json"), encoding="utf-8"))
    hp = a.homepage
    out = subprocess.run(["node", "-e", "global.window={};require(process.argv[1]);console.log(JSON.stringify(window))",
                          os.path.abspath(os.path.join(hp, "trackrecord-daten.js"))], capture_output=True, text=True, check=True).stdout
    w = json.loads(out)
    f = []
    ok = 0

    def cmp(name, a_, b_, tol=0.051):
        nonlocal ok
        if isinstance(a_, (int, float)) and isinstance(b_, (int, float)):
            same = abs(a_ - b_) <= tol
        else:
            same = a_ == b_
        if same:
            ok += 1
        else:
            f.append(f"{name}: Homepage {a_} ≠ ergebnisse.json {b_}")

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import auto_ergebnisse as ae
    ae.lade_signale(a.medien)
    VERBOTEN = ("rendite", "gewinn", "rueckgang", "besterTag", "schlechtesterTag")  # nie in Monats-/Wochenblöcken der Homepage

    def block_ok(name, h, x, von, bis):
        for k in ("wetten", "treffer"):
            cmp(f"{name} live.{k}", h["live"].get(k), x["live"][k], 0)
        if "verlustserie" in x["live"]:
            cmp(f"{name} live.verlustserie", h["live"].get("verlustserie"), x["live"]["verlustserie"], 0)
        q = ae.quote_block(d, x, von, bis)
        if q is not None:
            cmp(f"{name} Ø-Quote", h["live"].get("quote"), q, 0.0051)
        elif "quote" in h["live"]:
            f.append(f"{name}: Ø-Quote {h['live']['quote']} auf der Homepage, aber nicht aus den Bot-Daten herleitbar")
        for k in VERBOTEN:
            if k in h["live"]:
                f.append(f"{name}: Feld {k} darf auf der Homepage nicht stehen (nur Jahr)")

    hm = {m["monat"]: m for m in w.get("TRACKRECORD", [])}
    for m in d.get("monate", []):
        h = hm.get(m["monat"])
        if not h:
            f.append(f"Monat {m['monat']}: fehlt auf der Homepage")
            continue
        block_ok(f"Monat {m['monat']}", h, m, m["monat"] + "-01", m["monat"] + "-31")
        for k in ("tipps", "treffer"):
            cmp(f"Monat {m['monat']} einzelspiele.{k}", h["einzelspiele"].get(k), m["einzelspiele"][k], 0)
        cmp(f"Monat {m['monat']} Markierung", bool(h.get("rueckrechnung")), bool(m.get("rueckrechnung")))
    hw = {x["von"]: x for x in w.get("TRACKRECORD_WOCHEN", [])}
    for x in d.get("wochen", []):
        h = hw.get(x["von"])
        if not h:
            f.append(f"Woche {x['von']}: fehlt auf der Homepage")
            continue
        block_ok(f"Woche {x['von']}", h, x, x["von"], x["bis"])
    tage = sorted(d.get("tage", []), key=lambda t: t["datum"])
    ss = lambda t: t.get("seitStart") or t.get("seit_start") or {}
    # Jahre: Wetten/Treffer/Einsätze/Rendite aus seitStart-Differenzen; unter 100 Wetten darf nichts davon veröffentlicht sein
    ht = {t["d"]: t for t in w.get("TRACKRECORD_TAGE", [])}
    hj = {j["jahr"]: j for j in w.get("TRACKRECORD_JAHRE", [])}
    for jahr in sorted({t["datum"][:4] for t in tage if ss(t)}):
        tj = [t for t in tage if t["datum"][:4] == jahr]
        vor = [t for t in tage if t["datum"][:4] < jahr]
        v = ss(vor[-1]) if vor else {"wetten": 0, "treffer": 0, "gewinn": 0.0}
        z = ss(tj[-1])
        H = hj.get(int(jahr))
        if not H:
            f.append(f"Jahr {jahr}: fehlt auf der Homepage")
            continue
        wj = z["wetten"] - v["wetten"]
        cmp(f"Jahr {jahr} Wetten", H["wetten"], wj, 0)
        cmp(f"Jahr {jahr} Treffer", H["treffer"], z["treffer"] - v["treffer"], 0)
        cmp(f"Jahr {jahr} Stand", H["stand"], tj[-1]["datum"])
        for k in ("gewinn", "rendite"):
            if k in H:
                f.append(f"Jahr {jahr}: Feld {k} darf auf der Homepage nicht stehen (Einsätze/Rendite nur in Telegram)")
        if wj >= ae.JAHR_MIN_WETTEN:
            for t in tj:
                wt, tt = ss(t)["wetten"] - v["wetten"], ss(t)["treffer"] - v["treffer"]
                hh = ht.get(t["datum"])
                if wt < ae.KURVE_AB_WETTEN:
                    if hh:
                        f.append(f"Tag {t['datum']}: Kurve beginnt erst ab {ae.KURVE_AB_WETTEN} Wetten im Jahr")
                    continue
                if not hh:
                    f.append(f"Tag {t['datum']}: fehlt in der Kurve")
                    continue
                if "g" in hh:
                    f.append(f"Tag {t['datum']}: altes Kurvenfeld g (Einsätze) darf nicht mehr stehen")
                cmp(f"Tag {t['datum']} Kurve Trefferquote (Jahr)", hh.get("q"), round(tt / wt * 100, 1), 0.051)
                cmp(f"Tag {t['datum']} Markierung", bool(hh["rr"]), bool(t.get("rueckrechnung")))
        else:
            if any(t["datum"][:4] == jahr for t in ht.values()):
                f.append(f"Jahr {jahr}: Kurve veröffentlicht, obwohl nur {wj} Wetten (< {ae.JAHR_MIN_WETTEN})")
        qj = ae.quote_zeitraum(d, tj[0]["datum"], tj[-1]["datum"])
        if qj is not None:
            cmp(f"Jahr {jahr} Ø-Quote", H.get("quote"), qj, 0.0051)
    # Statische Monatsseiten: Wetten, Treffer, Ø-Quote, Verlustserie; keine Einsätze/Rendite
    for m in d.get("monate", []):
        p = os.path.join(hp, f"monatsbericht-{m['monat']}.html")
        if not os.path.exists(p):
            f.append(f"Seite {p} fehlt")
            continue
        h = open(p, encoding="utf-8").read()
        L = m["live"]
        q = L["treffer"] / L["wetten"] * 100 if L["wetten"] else 0
        soll = [("Wetten", str(L["wetten"])), ("Treffer", f"{L['treffer']} ({de(q)} %)"), ("Längste Verlustserie", f"{L['verlustserie']} in Folge")]
        qq = ae.quote_block(d, m, m["monat"] + "-01", m["monat"] + "-31")
        if qq is not None:
            soll.append(("Ø-Quote", de(qq, 2)))
        for lab, val in soll:
            mm = re.search(rf"<th>{lab}</th><td>([^<]*)</td>", h)
            if mm and mm.group(1) == val:
                ok += 1
            else:
                f.append(f"Seite {m['monat']} {lab}: {mm.group(1) if mm else 'fehlt'} ≠ {val}")
        for lab in ("Einsätze", "Rendite", "Größter Rückgang", "Bester Tag", "Schlechtester Tag"):
            if re.search(rf"<th>{lab}</th>", h):
                f.append(f"Seite {m['monat']}: Zeile {lab} darf nicht auf der Monatsseite stehen")
        for w_ in ("zurückgerechnet", "Rückrechnung", "rückgerechnet"):
            if w_.lower() in h.lower():
                f.append(f"Seite {m['monat']}: enthält '{w_}'")
    # Verbotene Wörter überall
    for dp, _, fs in os.walk(hp):
        if "/.git" in dp:
            continue
        for fn in fs:
            if fn.endswith((".html", ".js", ".css", ".xml", ".txt")):
                t = open(os.path.join(dp, fn), encoding="utf-8", errors="ignore").read().lower()
                for w_ in ("zurückgerechnet", "rückrechnung", "rückgerechnet", "rueckrechnungtext"):
                    if w_ in t:
                        f.append(f"{fn}: enthält '{w_}'")
    print(json.dumps({"geprueft_gleich": ok, "abweichungen": f}, ensure_ascii=False, indent=1))
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())

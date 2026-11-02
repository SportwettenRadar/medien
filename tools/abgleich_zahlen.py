#!/usr/bin/env python3
"""Abgleich: alle Zahlen der Homepage gegen daten/ergebnisse.json (Tage, Wochen, Monate, Seit Start).
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

    hm = {m["monat"]: m for m in w.get("TRACKRECORD", [])}
    for m in d.get("monate", []):
        h = hm.get(m["monat"])
        if not h:
            f.append(f"Monat {m['monat']}: fehlt auf der Homepage")
            continue
        for k in ("wetten", "treffer", "rendite", "gewinn", "verlustserie", "rueckgang", "besterTag", "schlechtesterTag"):
            if k in m["live"]:
                cmp(f"Monat {m['monat']} live.{k}", h["live"].get(k), m["live"][k])
        for k in ("tipps", "treffer"):
            cmp(f"Monat {m['monat']} einzelspiele.{k}", h["einzelspiele"].get(k), m["einzelspiele"][k], 0)
        cmp(f"Monat {m['monat']} Markierung", bool(h.get("rueckrechnung")), bool(m.get("rueckrechnung")))
    hw = {x["von"]: x for x in w.get("TRACKRECORD_WOCHEN", [])}
    for x in d.get("wochen", []):
        h = hw.get(x["von"])
        if not h:
            f.append(f"Woche {x['von']}: fehlt auf der Homepage")
            continue
        for k in ("wetten", "treffer", "rendite"):
            cmp(f"Woche {x['von']} live.{k}", h["live"].get(k), x["live"][k])
    ht = {t["d"]: t for t in w.get("TRACKRECORD_TAGE", [])}
    tage = sorted(d.get("tage", []), key=lambda t: t["datum"])
    ss = lambda t: t.get("seitStart") or t.get("seit_start") or {}
    for t in tage:
        h = ht.get(t["datum"])
        if not ss(t):
            continue
        if not h:
            f.append(f"Tag {t['datum']}: fehlt in der Kurve")
            continue
        cmp(f"Tag {t['datum']} Stand seit Start", h["g"], ss(t)["gewinn"])
        cmp(f"Tag {t['datum']} Markierung", bool(h["rr"]), bool(t.get("rueckrechnung")))
    if tage and ss(tage[-1]):
        S, z = w.get("TRACKRECORD_START") or {}, ss(tage[-1])
        for k in ("wetten", "treffer", "rendite", "gewinn"):
            cmp(f"Seit Start {k}", S.get(k), z[k])
        cmp("Seit Start Stand", S.get("stand"), tage[-1]["datum"])
        # Seit Start muss der Summe der Monate entsprechen, wenn die Monate lückenlos ab Start vorliegen
        sw = sum(m["live"]["wetten"] for m in d.get("monate", []))
        st = sum(m["live"]["treffer"] for m in d.get("monate", []))
        sg_ = sum(m["live"].get("gewinn", 0) for m in d.get("monate", []))
        if tage[-1]["datum"] == max(m["monat"] for m in d["monate"]) + "-" + str(__import__("calendar").monthrange(*map(int, max(m["monat"] for m in d["monate"]).split("-")))[1]):
            cmp("Seit Start Wetten = Summe Monate", z["wetten"], sw, 0)
            cmp("Seit Start Treffer = Summe Monate", z["treffer"], st, 0)
            cmp("Seit Start Einsätze = Summe Monate", z["gewinn"], sg_, 0.11)
    # Statische Monatsseiten
    for m in d.get("monate", []):
        p = os.path.join(hp, f"monatsbericht-{m['monat']}.html")
        if not os.path.exists(p):
            f.append(f"Seite {p} fehlt")
            continue
        h = open(p, encoding="utf-8").read()
        L = m["live"]
        q = L["treffer"] / L["wetten"] * 100 if L["wetten"] else 0
        for lab, val in (("Einsätze", sg(L.get("gewinn", 0))), ("Wetten", str(L["wetten"])), ("Treffer", f"{L['treffer']} ({de(q)} %)"),
                         ("Rendite", sg(L["rendite"]) + " %")):
            mm = re.search(rf"<th>{lab}</th><td>([^<]*)</td>", h)
            if mm and mm.group(1) == val:
                ok += 1
            else:
                f.append(f"Seite {m['monat']} {lab}: {mm.group(1) if mm else 'fehlt'} ≠ {val}")
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

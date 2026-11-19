#!/usr/bin/env python3
"""Independent verification of the health-efficiency story (pre-Avaloka).

Senior-dev rule: know the answer before the tool tells you, so Avaloka's
output can be checked against it. Pure stdlib (no pandas needed).

Reads data/worldbank_health_panel.csv, prints:
1. 2023 efficiency ranking (years of life per $1,000 health spend, PPP),
   top 15 + bottom 5 among countries with population > 5M.
2. Spend bins vs mean life expectancy (the saturation curve).
3. India's position vs income-matched peers (GDP/capita PPP within 0.7x-1.4x).
4. Anchor table: USA / JPN / CRI / IND / CHE / GBR / DEU.
"""
import csv
import os
from statistics import mean

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE) if os.path.basename(_HERE) == "scripts" else _HERE
CSV = os.path.join(ROOT, "data", "worldbank_health_panel.csv")


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    rows = []
    with open(CSV, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["year"] != "2023":
                continue
            le = f(r["life_expectancy"])
            spend = f(r["health_spend_ppp"])
            gdp = f(r["gdp_per_capita_ppp"])
            pop = f(r["population"])
            if le is None or spend is None or spend <= 0:
                continue
            rows.append({
                "code": r["country_code"], "country": r["country"],
                "le": le, "spend": spend, "gdp": gdp, "pop": pop,
                "eff": le / (spend / 1000.0),  # years per $1000/person
            })
    print(f"2023 rows with life expectancy + spend: {len(rows)}")

    big = [r for r in rows if r["pop"] and r["pop"] > 5_000_000]
    print(f"of those, population > 5M: {len(big)}\n")

    print("TOP 15 efficiency (years per $1,000 health spend, pop > 5M):")
    for i, r in enumerate(sorted(big, key=lambda x: -x["eff"])[:15], 1):
        print(f"  {i:2}. {r['country']:<28} {r['eff']:6.1f} yrs/$1k "
              f"(LE {r['le']:.1f}, spend ${r['spend']:,.0f})")
    print("\nBOTTOM 5 efficiency (pop > 5M):")
    for i, r in enumerate(sorted(big, key=lambda x: x["eff"])[:5], 1):
        print(f"  {i}. {r['country']:<28} {r['eff']:6.2f} yrs/$1k "
              f"(LE {r['le']:.1f}, spend ${r['spend']:,.0f})")

    print("\nSATURATION — mean life expectancy by health-spend band (2023, all countries):")
    bands = [(0, 250), (250, 500), (500, 1000), (1000, 2000),
             (2000, 4000), (4000, 8000), (8000, 10**9)]
    for lo, hi in bands:
        grp = [r["le"] for r in rows if lo <= r["spend"] < hi]
        if grp:
            print(f"  ${lo:>5,}-${hi if hi < 10**9 else 0:>5,}  n={len(grp):3}  mean LE {mean(grp):.1f} yrs")

    ind = next(r for r in rows if r["code"] == "IND")
    print(f"\nINDIA 2023: LE {ind['le']:.1f}, spend ${ind['spend']:,.0f}, "
          f"GDP/cap PPP ${ind['gdp']:,.0f}, efficiency {ind['eff']:.1f} yrs/$1k")
    peers = [r for r in rows if r["gdp"] and 0.7 * ind["gdp"] <= r["gdp"] <= 1.4 * ind["gdp"]]
    peers_sorted = sorted(peers, key=lambda x: -x["le"])
    rank = next(i for i, r in enumerate(peers_sorted, 1) if r["code"] == "IND")
    print(f"Income-matched peers (GDP/cap PPP 0.7x-1.4x of India): n={len(peers)}; "
          f"India ranks #{rank} by life expectancy (peer mean LE {mean([r['le'] for r in peers]):.1f})")
    print("  peers above India:", ", ".join(
        f"{r['country']} ({r['le']:.1f})" for r in peers_sorted[:rank - 1][:8]) or "none")

    print("\nANCHORS 2023:")
    for code in ("USA", "JPN", "CRI", "IND", "CHE", "GBR", "DEU", "KOR", "CHN"):
        r = next((x for x in rows if x["code"] == code), None)
        if r:
            print(f"  {r['country']:<15} LE {r['le']:5.1f}  spend ${r['spend']:>8,.0f}  "
                  f"eff {r['eff']:6.2f} yrs/$1k  GDP/cap ${r['gdp']:,.0f}" if r["gdp"] else
                  f"  {r['country']:<15} LE {r['le']:5.1f}  spend ${r['spend']:>8,.0f}  eff {r['eff']:6.2f} yrs/$1k")


if __name__ == "__main__":
    main()

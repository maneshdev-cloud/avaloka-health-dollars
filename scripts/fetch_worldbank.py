#!/usr/bin/env python3
"""Fetch World Bank indicators and join into one health-efficiency panel.

Question: Which countries get the most years of life per health dollar — and
where does India stand?

Indicators (all countries, 2000-2023):
- SP.DYN.LE00.IN    Life expectancy at birth, total (years)
- SH.XPD.CHEX.PP.CD Current health expenditure per capita, PPP (current intl $)
- SH.XPD.CHEX.PC.CD Current health expenditure per capita (current US$)
- NY.GDP.PCAP.PP.CD GDP per capita, PPP (current international $)
- SP.POP.TOTL       Population, total

Output: data/worldbank_health_panel.csv — one row per country-year.
"""
import csv
import json
import os
import urllib.request

BASE = "https://api.worldbank.org/v2/country/all/indicator"
COUNTRY_META = "https://api.worldbank.org/v2/country?format=json&per_page=300"
INDICATORS = {
    "life_expectancy": "SP.DYN.LE00.IN",
    "health_spend_ppp": "SH.XPD.CHEX.PP.CD",
    "health_spend_usd": "SH.XPD.CHEX.PC.CD",
    "gdp_per_capita_ppp": "NY.GDP.PCAP.PP.CD",
    "population": "SP.POP.TOTL",
}
YEARS = "2000:2023"
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE) if os.path.basename(_HERE) == "scripts" else _HERE
OUT = os.path.join(ROOT, "data", "worldbank_health_panel.csv")


def real_countries():
    """ISO3 codes of real countries only. The World Bank API also returns
    aggregates (World, High income, North America, ...) whose region.id is
    'NA' — those pollute rankings and must be excluded."""
    with urllib.request.urlopen(COUNTRY_META, timeout=60) as r:
        meta, rows = json.load(r)
    real = {row["id"] for row in rows or []
            if row.get("region", {}).get("id") != "NA"}
    print(f"country metadata: {len(rows or [])} entries, {len(real)} real countries")
    return real


def fetch(indicator, keep):
    url = f"{BASE}/{indicator}?format=json&per_page=20000&date={YEARS}"
    with urllib.request.urlopen(url, timeout=60) as r:
        meta, rows = json.load(r)
    print(f"{indicator}: {meta['total']} records (pages {meta['pages']})")
    out = {}
    for row in rows or []:
        if row.get("value") is None:
            continue
        if row["countryiso3code"] not in keep:
            continue
        key = (row["countryiso3code"], row["date"])
        out[key] = (row["country"]["value"], row["value"])
    return out


def main():
    keep = real_countries()
    data = {}
    for name, code in INDICATORS.items():
        data[name] = fetch(code, keep)

    keys = set()
    for d in data.values():
        keys |= set(d)
    print(f"distinct country-years with >=1 value: {len(keys)}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["country_code", "country", "year", "life_expectancy",
                    "health_spend_ppp", "health_spend_usd",
                    "gdp_per_capita_ppp", "population"])
        n_full = 0
        for (code, year) in sorted(keys):
            name = None
            vals = []
            for col in INDICATORS:
                got = data[col].get((code, year))
                if got:
                    name = name or got[0]
                    vals.append(got[1])
                else:
                    vals.append("")
            if all(v != "" for v in vals):
                n_full += 1
            w.writerow([code, name or "", year] + vals)
    print(f"wrote {OUT} ({len(keys)} rows, {n_full} complete)")

    # Sanity check: 2023 values for USA / JPN / CRI / IND
    print("\n2023 sanity check:")
    for code in ("USA", "JPN", "CRI", "IND"):
        row = []
        for col in INDICATORS:
            got = data[col].get((code, "2023"))
            row.append(f"{col}={got[1] if got else 'NA'}")
        print(f"  {code}: " + " | ".join(row))


if __name__ == "__main__":
    main()

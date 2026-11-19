"""Prepare Avaloka-ready datasets from the World Bank health panel.

1. data/wb_2023_snapshot.csv — 2023 rows only, with a spend_band column
   (health spend PPP $/person bands) for the saturation-curve group comparison.
2. data/wb_panel_dated.csv — full 2000-2023 panel with a real date column
   (YYYY-01-01) so Avaloka's trend analysis can use it.
"""
import os

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE) if os.path.basename(_HERE) == "scripts" else _HERE

panel = pd.read_csv(os.path.join(ROOT, "data", "worldbank_health_panel.csv"))

# --- 2023 snapshot with spend bands ---
snap = panel[panel["year"] == 2023].copy()
snap = snap.dropna(subset=["life_expectancy", "health_spend_ppp"])
bins = [0, 250, 500, 1000, 2000, 4000, 8000, float("inf")]
labels = ["0-250", "250-500", "500-1000", "1000-2000", "2000-4000", "4000-8000", "8000+"]
snap["spend_band"] = pd.cut(
    snap["health_spend_ppp"], bins=bins, labels=labels, include_lowest=True
)
snap.to_csv(os.path.join(ROOT, "data", "wb_2023_snapshot.csv"), index=False)
print(f"snapshot: {len(snap)} rows")
print(snap.groupby("spend_band", observed=True)["life_expectancy"].agg(["mean", "count"]).round(1))

# --- Full panel with a date column ---
dated = panel.copy()
dated["date"] = pd.to_datetime(dated["year"], format="%Y")
dated.to_csv(os.path.join(ROOT, "data", "wb_panel_dated.csv"), index=False)
print(f"panel: {len(dated)} rows, years {dated['year'].min()}-{dated['year'].max()}")

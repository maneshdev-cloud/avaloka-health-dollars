# The $4,000 Ceiling — Years of Life per Health Dollar

**Avaloka Hackathon entry (Guruvai Sciences), November 2026 — by Manesh Sunil Jadhav**

📊 **[Read the full report](https://maneshdev-cloud.github.io/avaloka-health-dollars/)**

> **Past about $4,000 of health spending per person, doubling the money buys just +0.4 years of life.**
> The richest health system on Earth buys the least life per dollar — and India is quietly beating its income peers.

## The question

Which countries get the most years of life per health dollar — and where does India stand?

## What the data says

**The saturation curve.** Mean life expectancy by 2023 health-spending band (PPP $ per person, n = 192 countries):

| Spend / person | Mean life expectancy | Countries |
|---|---|---:|
| $0–250 | 65.0 yrs | 45 |
| $250–500 | 67.5 yrs | 17 |
| $500–1,000 | 72.2 yrs | 30 |
| $1,000–2,000 | 74.1 yrs | 37 |
| $2,000–4,000 | 77.5 yrs | 30 |
| $4,000–8,000 | 82.6 yrs | 25 |
| $8,000+ | 83.0 yrs | 8 |

**The USA paradox.** The USA spends $13,473 per person (2023) — the most on Earth — for 78.4 years of life. Among 123 countries with population over 5 million, it is **dead last** in years of life per $1,000 spent (5.82). Japan spends 40% of that and lives 5.7 years longer (84.0 yrs). Costa Rica spends one-seventh and lives 2.4 years longer (80.8 yrs).

**Where India stands.** India: $346 per person → 72.0 years. Among 30 income-matched peers (GDP per capita PPP 0.7×–1.4× India's $9,853), India ranks **#14 — 2.0 years above the peer mean (70.0)**. Bangladesh (74.7 yrs) leads the peer group at similar income.

**24 years of progress.** Global mean life expectancy rose from 67.6 years (2000) to 73.8 (2023), +6.2 years — with a single reversal: COVID-19 (73.0 → 71.8, 2019–2021), recovered by 2022.

**The GDP twist.** Health spending correlates with life expectancy at r = 0.655 — but GDP per capita correlates at r = 0.651, nearly identically. The money itself isn't the differentiator; **how a country spends it is**.

**The model.** A random forest predicting life expectancy from spending, GDP, population and year: holdout R² 0.7762 (time-based split, 4,166 train / 1,042 test), CV R² 0.846 ± 0.051, validation PASS (level 4/4). Linear regression on the same data manages R² 0.11 — the relationship is curved, not straight.

## Methodology

- **Data:** World Bank Open Data API (open, no key). Five indicators joined on country + year: life expectancy (SP.DYN.LE00.IN), health expenditure per capita PPP (SH.XPD.CHEX.PP.CD) and current US$ (SH.XPD.CHEX.PC.CD), GDP per capita PPP (NY.GDP.PCAP.PP.CD), population (SP.POP.TOTL). 217 real countries, 2000–2023, 5,208 rows, 4,415 complete. World Bank aggregates (World, High income, regions) filtered out.
- **Analysis:** [Avaloka](https://github.com/guruvaidev/avaloka) open-source CLI v1.6 — `avaloka analyze` (deterministic goal-specific calculations: group comparison, Pearson correlation, time trend) and `avaloka train` (random forest, time-based holdout). No LLM-generated figures anywhere in this report.
- **Verification:** every number Avaloka reported was independently re-computed from the raw CSV with `scripts/verify_numbers.py`. All headline figures matched exactly.
- **Efficiency framing:** efficiency (years per $1,000) is compared only among large countries (population > 5M). A raw global efficiency ranking is dominated by the poorest countries and is not presented — that is poverty, not efficiency.

## Reproduce

```bash
# 1. Fetch the data (World Bank API, no key needed)
python scripts/fetch_worldbank.py
python scripts/prep_analysis_data.py

# 2. Install Avaloka (https://github.com/guruvaidev/avaloka)
git clone https://github.com/guruvaidev/avaloka && cd avaloka
./scripts/install.sh && source .venv/bin/activate

# 3. Run the analyses
avaloka analyze data/wb_2023_snapshot.csv --goal "average life_expectancy by spend_band"
avaloka analyze data/wb_panel_dated.csv --goal "correlation between health_spend_ppp and life_expectancy"
avaloka analyze data/wb_panel_dated.csv --goal "life_expectancy trend over time"
avaloka train data/wb_panel_dated.csv --target life_expectancy

# 4. Verify every number independently
python scripts/verify_numbers.py

# 5. Rebuild the report page
python scripts/build_report.py   # writes index.html at the repo root
```

## Repo contents

- `index.html` — the full report (also served via GitHub Pages)
- `data/` — the World Bank panel (5,208 rows), the 2023 snapshot, the dated panel
- `avaloka-outputs/` — Avaloka's raw mission bundles: `bands/`, `correlation/`, `trend/` (executive + technical reports, goal_analysis.json, reproducible analysis.py) and `train/` (model card, validation report, evaluation)
- `scripts/` — data fetch, verification, prep, and the report builder

Note: the trained model binary (`avaloka-model/model/`, 73 MB) is intentionally not included; retrain with the command above.

## Author

**Manesh Sunil Jadhav** — Final-year Diploma in AI & ML, Government Polytechnic Mumbai.
Best Undergraduate, Google Mumbai Data Challenge (Google + Zindi), November 2026.
[GitHub](https://github.com/maneshdev-cloud) · [LinkedIn](https://www.linkedin.com/in/manesh-jadhav04)

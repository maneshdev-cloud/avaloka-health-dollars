# Avaloka mission `c5b14c84e8da`

**Goal:** average life_expectancy by spend_band

This bundle was produced by Avaloka as a governed *Data Mission* — an outcome, not an interaction. Economic multiplier: **11.1x** (≈9.4 manual hours compressed).

## Deliverables

- `executive_report.html` — the decision-maker summary
- `technical_report.html` — full methodology, schema, quality and validation
- `analysis.ipynb` / `analysis.py` — reproducible pipeline
- `transformed_dataset.parquet` — cleaned working dataset
- `data_quality.json`, `validation_report.json`, `planner_graph.json` — evidence
- `assumptions.yaml`, `lineage.json`, `environment.lock` — governance & reproducibility
- `goal_analysis.json` — measured answer to the stated goal

## Key findings

- spend_band=8000+: mean life_expectancy=83.
- spend_band=4000-8000: mean life_expectancy=82.6.
- spend_band=2000-4000: mean life_expectancy=77.5.
- spend_band=1000-2000: mean life_expectancy=74.1.
- spend_band=500-1000: mean life_expectancy=72.2.

## Limitations

- Small sample size limits statistical confidence.
- Estimated manual effort and value are heuristics pending customer calibration.

## Reproduce

```bash
avaloka analyze data/wb_2023_snapshot.csv --goal 'average life_expectancy by spend_band' --output ./reproduced-analysis
```

---
_Reproduce or adapt this mission with `avaloka`._
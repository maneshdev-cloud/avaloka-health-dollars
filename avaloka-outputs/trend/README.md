# Avaloka mission `b23d2d830a2d`

**Goal:** life_expectancy trend over time

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

- Monthly mean life_expectancy changed from 67.6 in 2000-01 to 73.8 in 2023-01 (change +6.2).
- This is a descriptive change, not an explanation of its cause.

## Limitations

- Estimated manual effort and value are heuristics pending customer calibration.

## Reproduce

```bash
avaloka analyze data/wb_panel_dated.csv --goal 'life_expectancy trend over time' --output ./reproduced-analysis
```

---
_Reproduce or adapt this mission with `avaloka`._
# Avaloka mission `7622c6e30fd9`

**Goal:** correlation between health_spend_ppp and life_expectancy

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

- life_expectancy and health_spend_ppp: Pearson r=0.655.
- Correlation alone does not establish causation.

## Limitations

- Estimated manual effort and value are heuristics pending customer calibration.

## Reproduce

```bash
avaloka analyze data/wb_panel_dated.csv --goal 'correlation between health_spend_ppp and life_expectancy' --output ./reproduced-analysis
```

---
_Reproduce or adapt this mission with `avaloka`._
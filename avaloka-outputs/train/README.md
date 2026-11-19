# Avaloka mission `0fba6f8e7878`

**Goal:** Predict 'life_expectancy'

This bundle was produced by Avaloka as a governed *Data Mission* — an outcome, not an interaction. Economic multiplier: **11.1x** (≈17.7 manual hours compressed).

## Deliverables

- `executive_report.html` — the decision-maker summary
- `technical_report.html` — full methodology, schema, quality and validation
- `analysis.ipynb` / `analysis.py` — reproducible pipeline
- `transformed_dataset.parquet` — cleaned working dataset
- `data_quality.json`, `validation_report.json`, `planner_graph.json` — evidence
- `assumptions.yaml`, `lineage.json`, `environment.lock` — governance & reproducibility
- `model/` + `model_card.md` — the validated model and its card
- `evaluation_report.html`, `cost_quality.json` — candidate comparison & economics
- `service.py`, `Dockerfile`, `deployment/` — the deployment package
- `feature_contract.yaml`, `inference_schema.json`, `monitoring_config.yaml` — the serving contract

## Key findings

- 'health_spend_ppp' and 'health_spend_usd' are strongly associated (|corr|=0.955).
- Best model 'random_forest' scored 0.7762 r2 on holdout.
- 'health_spend_ppp' and 'health_spend_usd' move together (|corr|=0.955); consider redundancy or a shared driver.

## Limitations

- Estimated manual effort and value are heuristics pending customer calibration.

## Reproduce

```bash
python analysis.py  # reproduce data preparation
```

## Serve locally

```bash
pip install -r requirements.lock
uvicorn service:app --port 8080
# then: avaloka deploy . --target local
```

---
_Reproduce or adapt this mission with `avaloka`._
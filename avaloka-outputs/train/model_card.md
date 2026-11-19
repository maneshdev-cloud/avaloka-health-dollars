# Model card — Predict 'life_expectancy'

- **Mission:** `0fba6f8e7878`
- **Task:** regression
- **Target:** life_expectancy
- **Primary metric:** r2
- **Selected model:** random_forest
- **Validation verdict:** PASS (max safe deployment level 4/4)

## Intended use

Decision support for the stated goal. Not a substitute for human judgement on high-stakes decisions.

## Performance

| Candidate | r2 | CV mean ± std |
|---|---|---|
| random_forest | 0.7762 | 0.846 ± 0.051 |
| gradient_boosting | 0.7610 | 0.788 ± 0.028 |
| linear_regression | 0.1139 | 0.457 ± 0.032 |

## Training data

- Rows: 4166 train / 1042 test
- Features: 8

## Limitations & ethical considerations

- Estimated manual effort and value are heuristics pending customer calibration.

## Validation checks

- **data_sufficiency** — PASS: ~50 rows/feature suggests >= 400 rows for 8 features.
- **target_leakage** — PASS: No feature is near-perfectly predictive of the target.
- **split_validity** — PASS: Used 'time_based_holdout' (4166 train / 1042 test rows).
- **beats_baseline** — PASS: CV r2 0.846 beats the mean baseline (-0.106) by more than fold noise.
- **stability** — PASS: CV r2 = 0.846 +/- 0.051 (stable).
- **overfitting** — PASS: Holdout and CV scores are consistent.

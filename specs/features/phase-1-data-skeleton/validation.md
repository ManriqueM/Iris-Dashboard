# Phase 1 — Data & Skeleton: Validation

## Automated (`python3 scripts/validate.py`)
- [x] `data/iris.csv` has 150 rows, with 50 each of setosa, versicolor and virginica.
- [x] The `IRIS` constant in `index.html` matches the CSV row for row.
- [x] The overall means round to 5.843 / 3.057 / 3.758 / 1.199 (sepal L/W, petal L/W).
- [x] The setosa mean petal length rounds to 1.462, and the virginica one to 5.552.

## Visual (headless screenshot)
- [x] The page opens from `file://` with no network requests and no console errors.
- [x] The KPI tiles show 150, 3 and the four means, matching the script.
- [x] The per-species table shows 3 rows × 4 features in the species colors.
- [x] The chart grid shows 4 placeholders and the layout doesn't break at 375px width.

# Phase 1 — Data & Skeleton: Requirements

## Scope
- Add `data/iris.csv` (150 rows: sepal_length, sepal_width, petal_length, petal_width, species).
- Build `index.html`, which holds the dataset as a JS constant.
- Page layout: header, filter bar (placeholder for Phase 3), chart grid (placeholders for Phase 2).
- KPI tiles:
  - Overall: 150 samples, 3 species, and the mean of each of the 4 features.
  - Per-species breakdown: the mean of each feature for setosa, versicolor and virginica.

## Decisions
- Use the canonical UCI/Fisher values. The CSV is the source of truth, and the embedded constant must match it.
- Means are computed in JS at load time, not hard-coded.
- One fixed color per species, defined once and reused by every later phase.
- Plotly is not loaded yet. It arrives in Phase 2, which keeps this phase dependency-free.

## Out of scope
Charts, filters, data table, export.

# Phase 1 — Data & Skeleton: Plan

Aligned with `specs/mission.md` (offline teaching demo) and `specs/tech-stack.md` (single HTML, vanilla JS).

## 1. Data
1.1 Create `data/iris.csv` with the 150 canonical rows.
1.2 Write `scripts/build.py`. It embeds the CSV into `index.html` as `const IRIS = [...]`, so the two never drift apart.

## 2. Skeleton
2.1 HTML structure: header (title + one-line intro), filter bar placeholder, KPI section, chart grid with 4 labeled placeholders.
2.2 CSS: design tokens (species colors, spacing, type), responsive grid, light/dark support.

## 3. KPIs
3.1 JS: parse `IRIS` and compute the count, species count, overall means and per-species means.
3.2 Render the overall tiles, then a per-species table (rows = species, columns = features).

## 4. Validation tooling
4.1 Write `scripts/validate.py`. It checks the CSV (150 rows, 50 per species), the embedded data against the CSV, and the means against the known reference values.
4.2 Take a headless-browser screenshot of `index.html` opened offline.

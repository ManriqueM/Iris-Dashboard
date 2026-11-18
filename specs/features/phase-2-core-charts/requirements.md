# Phase 2 — Core Charts: Requirements

## Scope
Replace the four placeholders with interactive Plotly charts. Each chart is colored by species using the Phase 1 colors.
1. **Feature distributions**: overlaid histograms for one feature at a time, with a feature picker.
2. **Spread by species**: a box plot per species for one feature, with a picker that defaults to petal length.
3. **Feature vs. feature**: a scatter plot with X and Y pickers (default: petal length vs. petal width) and hover showing all four measurements.
4. **All pairs at once**: a 4×4 scatter matrix (SPLOM).

## Decisions
- Plotly.js (`plotly.js-dist-min`) is inlined into `index.html` by `build.py`, so the page needs no CDN and stays offline (~4.5 MB).
- The library is version-pinned via `package.json`.
- Chart colors are read from the CSS variables, so light and dark mode stay consistent.
- The Plotly mode bar is trimmed to zoom, pan, reset and download PNG.
- Charts resize with their cards, and the scatter matrix spans the full width.

## Out of scope
Species filters, linked selection, the data table (Phase 3), and ML views (Phase 4).

# Phase 2 — Core Charts: Validation

## Automated (`python3 scripts/validate.py`)
- [x] All Phase 1 checks still pass.
- [x] `Plotly` is defined, and the page makes no network requests.
- [x] The histogram, box and scatter charts each have 3 traces (one per species), and each trace has 50 points.
- [x] The scatter matrix has 3 traces with 4 dimensions each.
- [x] Changing the scatter X picker to sepal_width updates the trace x data to the sepal widths.
- [x] Changing the histogram picker updates the plotted feature.
- [x] No console errors.

## Visual (screenshots, desktop + 375px)
- [x] All 4 charts render with legible axes and the species colors match the Phase 1 dots.
- [x] Petal length vs. petal width clearly shows setosa separated from the other two.
- [x] Nothing overflows horizontally on mobile.

# Phase 3 — Interactivity: Plan

Aligned with `specs/mission.md` (let users filter, compare and inspect the raw data) and `specs/tech-stack.md` (vanilla JS, offline).

## 1. State
1.1 Add a row `id` to each flower, plus the `state` object and a `visibleRows()` helper (filters, then selection).
1.2 A central `update()` that re-renders the KPIs, species table, charts, table and banner.

## 2. Filters
2.1 Turn the chips into toggle buttons with `aria-pressed`, and stop the last active species from being turned off.
2.2 Make the KPIs and species table use the visible rows.

## 3. Linked selection
3.1 Enable select/lasso on the scatter. On `plotly_selected`, store the ids; on `plotly_deselect` or double-click, clear them.
3.2 Use `selectedpoints` on the scatter, scatter matrix and box points so unselected flowers fade, and make the histograms use only the selected rows.
3.3 Add a selection banner with a count and a Clear button.

## 4. Data table + export
4.1 A table card under the charts with sortable headers (with ▲/▼ indicators), a sticky header and a max-height scroll.
4.2 An "Export CSV" button that downloads the visible rows in the current sort order.

## 5. Validation
5.1 Extend `validate.py` with filter, selection, sort and export checks, then take screenshots.

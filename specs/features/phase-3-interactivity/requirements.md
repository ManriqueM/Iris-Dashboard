# Phase 3 — Interactivity: Requirements

## Scope
1. **Species filters**: the three species chips become toggles. Turning one off removes it from every chart, the KPIs, the species table and the data table. At least one species must stay on.
2. **Linked selection**: box- or lasso-select flowers in the scatter plot.
   - Selected flowers stay full-color in every chart. Unselected ones fade (scatter, scatter matrix, box plot points), and the histograms show only the selected flowers.
   - The KPIs and data table narrow to the selection, and a banner shows "N flowers selected" with a **Clear** button. Double-clicking the scatter also clears it.
3. **Data table**: every flower currently in view (filters + selection), with columns for row number, species and the 4 features. Sorting by any column; a sticky header with a scrollable body.
4. **CSV export**: downloads exactly the rows in the table (same columns, sorted as shown) as `iris-filtered.csv`.

## Decisions
- One shared state, `{ species: Set, selected: Set<rowId> | null, sort }`, with a single `update()` that redraws everything.
- Each flower gets a stable row id (1–150, in dataset order) so selections survive redraws.
- The species table keeps showing all three species, but rows whose species is filtered out are greyed rather than removed. Its means follow the current view.
- Export is built client-side (Blob + download link), so it works offline.
- Changing the species filters clears the selection, so the two never conflict.

## Out of scope
ML views (Phase 4), help text and README (Phase 5).

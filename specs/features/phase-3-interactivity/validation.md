# Phase 3 — Interactivity: Validation

## Automated (`python3 scripts/validate.py`)
- [x] All Phase 1–2 checks still pass.
- [x] Turning off setosa makes the data table show 100 rows, the Samples KPI show 100, and every chart drop the setosa trace or its points.
- [x] Turning off all but one species leaves the last chip unable to be turned off.
- [x] Simulating a scatter selection of 10 flowers makes the banner read "10 flowers selected", the table show 10 rows and the Samples KPI show 10.
- [x] Clear restores the table to its full filtered size.
- [x] Sorting by petal length descending puts the first row at 6.9 cm.
- [x] The exported CSV has a header plus as many rows as the table, in the same order.
- [x] No console errors and no network requests.

## Visual (screenshots, desktop + 375px)
- [x] An active selection shows faded unselected points across charts and the banner is visible.
- [x] Filtered-out chips look clearly "off".
- [x] The table scrolls inside its card on mobile with no page overflow.

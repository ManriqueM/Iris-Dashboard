# Phase 5 — Polish: Validation

## Automated (`python3 scripts/validate.py`)
- [x] All 61 existing checks pass with the system in light mode, and the full suite also passes in dark mode.
- [x] The theme toggle cycles Auto → Light → Dark, and `data-theme` and the chart paper text colors change.
- [x] The theme choice persists across a reload.
- [x] The "How to read" guide exists, is closed by default and opens on click.
- [x] Every chart card (7) has a "What to notice" note.
- [x] Body and muted text contrast is ≥ 4.5:1 on the surface and background colors, in both themes.
- [x] There is no horizontal overflow at 375, 768 and 1280 px.
- [x] No console errors and no network requests.

## Visual
- [x] Screenshots at 375/768/1280 in light and dark look clean, with no clipped controls or unreadable chart text.
- [x] `README.md` renders correctly and its instructions work (fresh `npm install` → build → validate).

# Phase 2 — Core Charts: Plan

Aligned with `specs/mission.md` (show which features separate species) and `specs/tech-stack.md` (single offline HTML, Plotly).

## 1. Library
1.1 Add `package.json` pinning `plotly.js-dist-min` and run `npm install`.
1.2 Extend `build.py` to inline the Plotly bundle in place of a `/*PLOTLY_JS*/` marker.

## 2. Shared chart setup
2.1 A helper that reads the species colors and theme colors from CSS.
2.2 A base layout (fonts, margins, transparent background, grid colors) and a trimmed config.
2.3 A reusable feature `<select>` control.

## 3. Charts
3.1 Histograms: one trace per species, overlay, opacity 0.6, feature picker.
3.2 Box plots: one box per species, all points shown, feature picker.
3.3 Scatter: X/Y pickers, rich hover template.
3.4 Scatter matrix: a full-width card with a 4×4 SPLOM and the diagonal hidden.

## 4. Validation
4.1 Extend `validate.py` with the Phase 2 checks, then rebuild and take screenshots.

# Phase 5 — Polish: Plan

Aligned with `specs/mission.md` (a teaching demo that answers "how do species differ?" in under a minute) and `specs/tech-stack.md` (single offline HTML).

## 1. Theme
1.1 Restructure the CSS variables: light defaults, `[data-theme="dark"]`, and `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) }`.
1.2 Add a header toggle button that cycles Auto/Light/Dark, persists the choice in localStorage (try/catch) and calls `update()` to re-theme the charts.
1.3 Make the heatmap midpoint and any other hard-coded colors read the theme.

## 2. Learner notes
2.1 Add a `<details>` "How to read this dashboard" guide under the header.
2.2 Add a "What to notice" line on each chart card, styled with an accent left border.

## 3. Responsive review
3.1 Take screenshots at 375/768/1280 in both themes, and fix any issues found.

## 4. Contrast
4.1 Make `validate.py` compute contrast ratios from the computed CSS variables in both themes.

## 5. Validation + README
5.1 Run the existing suite in light and in dark mode, and add checks for the toggle, persistence and notes.
5.2 Run `mm-readme` to generate `README.md`.

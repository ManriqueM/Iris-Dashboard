# Phase 5 — Polish: Requirements

## Scope
1. **How to read this dashboard**: a collapsible `<details>` guide under the header, closed by default. It holds 4–5 short points: what the dataset is, how to filter, how to select, how to use the predictor, and the key lesson (petals separate species, sepals don't).
2. **"What to notice" takeaways**: one short sentence per chart card (7: four charts, heatmap, PCA, predictor), visually distinct from the existing "how it works" hints.
3. **Light/dark toggle**: a small button in the header that cycles Auto → Light → Dark.
   - Auto follows the system setting. The choice is remembered with localStorage (wrapped in try/catch).
   - All Plotly charts re-theme immediately.
4. **Responsive check**: layouts at 375, 768 and 1280 px with no overflow and no clipped controls. Also fix anything the review finds.
5. **README**: generated with the `mm-readme` skill from the specs. It covers what the project is, how to open the dashboard, how to rebuild and validate it, the project structure and the roadmap status.

## Decisions
- The theme is applied via `data-theme` on `<html>`, and the CSS variables keyed on it replace the media-query-only approach. Auto mode keeps the media query.
- The heatmap's midpoint color follows the theme.
- Text contrast must be ≥ 4.5:1 for body and muted text, against the surface and background colors in both themes.
- No new dependencies.

## Out of scope
New charts or features, and hosting.

# Phase 4 — ML Extras: Requirements

## Scope
A new "Patterns & prediction" section below the charts, with three cards.

1. **Correlation heatmap**: a 4×4 Pearson correlation matrix with values printed in the cells and a diverging scale from -1 to 1. A toggle switches between "All flowers" and a single species, which teaches that correlations change within species (Simpson's-paradox-style).
2. **PCA view**: a 2-D projection of the standardized features, colored by species, with axis titles showing the % of variance explained. It follows the species filters and linked selection like the other charts.
3. **k-NN "predict a flower"**:
   - Four sliders (step 0.1 cm, ranges = dataset min–max) and a k selector (1, 3, 5, 7, 9, 15).
   - The output is the predicted species, with vote shares as a small bar.
   - The new flower is shown as a star on both the Feature-vs-feature scatter and the PCA view, with lines to its k nearest neighbours.
   - Leave-one-out accuracy is shown for the current k.
   - Presets: "Typical setosa / versicolor / virginica" and "Borderline" (between versicolor and virginica).

## Decisions
- All maths is implemented in plain JS (no ML library), so the page stays offline and small:
  - **PCA:** standardize with the population std, form the covariance matrix and eigen-decompose it (Jacobi method).
  - **k-NN:** Euclidean distance on standardized features. Ties go to the nearest neighbour's class.
- PCA and k-NN are always fitted on all 150 flowers. Filters affect only what's displayed.
- Eigenvector signs are flipped so that setosa sits on the left of PC1, keeping the picture stable.
- The prediction overlay on the scatter is drawn as extra traces (not part of the selection). It shows only when the predictor has been touched or a preset chosen, and a "Hide on charts" toggle turns it off.

## Out of scope
Training other models, uploading data, help text and README (Phase 5).

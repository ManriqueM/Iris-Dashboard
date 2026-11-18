# Phase 4 — ML Extras: Plan

Aligned with `specs/mission.md` (show *why* Iris is a classification classic) and `specs/tech-stack.md` (vanilla JS, offline, Plotly).

## 1. Math module (plain JS)
1.1 `standardize()` (means, population std, z-scores) and `pearson()`.
1.2 `jacobiEigen()` for a symmetric 4×4 matrix, then `pca()` returning the loadings, explained variance and 2-D scores. Apply the sign convention (setosa mean PC1 < 0).
1.3 `knnPredict(point, k)` (votes, neighbours) and `looAccuracy(k)`.
1.4 Expose these on `window.IRIS_ML` for validation.

## 2. Correlation heatmap
2.1 A card with a scope toggle (All / setosa / versicolor / virginica), drawn as a Plotly heatmap with text annotations and a diverging colorscale.

## 3. PCA view
3.1 A card with a scatter of PC1 vs PC2 for each active species, using `selectedpoints` for linked selection and axis titles with % variance.
3.2 Hook it into `update()`.

## 4. k-NN predictor
4.1 A card with 4 range sliders and value labels, a k select, preset buttons, and a result block (species, vote bar, LOO accuracy).
4.2 A state field `prediction: { point, k, show }`. On change, recompute and redraw the overlays on the scatter and PCA (a star plus neighbour lines).

## 5. Validation
5.1 A Python script writes scikit-learn reference values (correlations, PCA variance and scores, k-NN predictions for test points, LOO accuracy for each k). `validate.py` compares them with the JS values to a tolerance of 1e-6 (accuracies exact).
5.2 Add UI checks and take screenshots.

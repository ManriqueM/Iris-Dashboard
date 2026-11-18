# Phase 4 — ML Extras: Validation

## Automated (`python3 scripts/validate.py`), compared with scikit-learn
- [x] All Phase 1–3 checks still pass.
- [x] The correlation matrix (all flowers and each species) matches `numpy.corrcoef` to within 1e-6.
- [x] The PCA explained-variance ratios match `sklearn.decomposition.PCA` on `StandardScaler` data (PC1 ≈ 72.96%, PC2 ≈ 22.85%).
- [x] The PCA scores match scikit-learn up to sign, to within 1e-6, and the setosa mean PC1 is < 0.
- [x] The k-NN predictions for the presets and 20 random points match `KNeighborsClassifier` (standardized, Euclidean) for k = 1, 5 and 15.
- [x] The leave-one-out accuracy for each k in {1, 3, 5, 7, 9, 15} matches scikit-learn exactly.
- [x] UI: moving the sliders to a typical setosa predicts setosa, and the star plus k neighbour lines appear on the scatter and PCA.
- [x] UI: the heatmap toggle changes the values (for example, the sepal length–width correlation is negative for all flowers and positive within setosa).
- [x] The PCA view follows the species filter and the linked selection.
- [x] No console errors and no network requests.

## Visual (screenshots, desktop + 375px)
- [x] The heatmap is readable and its colors are centered at 0.
- [x] The PCA view clearly shows three clusters, with setosa on the left.
- [x] The predictor is usable on mobile (sliders full width) with no overflow.

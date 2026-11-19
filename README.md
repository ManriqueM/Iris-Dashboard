# Iris Explorer

> An offline, single-file interactive dashboard for exploring the classic Iris dataset.

## Overview
Iris Explorer turns Fisher's Iris dataset (150 flowers, 3 species, 4 measurements) into a dashboard you can explore in any browser. It's built for students, analysts and instructors learning exploratory data analysis, and it answers one question in under a minute: *how do the three species differ, and which measurements tell them apart?* Everything lives in one `index.html` file, so it works offline and needs nothing installed.

## Features
- **Data & summary:** the embedded dataset, with summary tiles and a table of each species' average measurements.
- **Core charts:** interactive histograms, box plots, a feature-vs-feature scatter plot with axis pickers, and a scatter matrix of every measurement pair.
- **Interactivity:**
  - Species filters that apply everywhere.
  - Drag-to-select flowers on the scatter plot, highlighted across every chart.
  - A sortable data table and CSV export of exactly what's shown.
- **Patterns & prediction:**
  - A correlation heatmap, overall or within one species.
  - A PCA view that squeezes all four measurements into two dimensions.
  - A k-nearest-neighbours "predict a flower" tool, with sliders, presets, vote shares and leave-one-out accuracy.
- **Polish:**
  - A "How to read this dashboard" guide and a "What to notice" takeaway on every chart.
  - Auto, light and dark themes, with the choice remembered between visits.
  - Responsive layout from phone to desktop.

## Tech Stack
- **HTML, CSS and vanilla JavaScript:** a single self-contained page with no build framework.
- **Plotly.js** (`plotly.js-dist-min`, version-pinned): interactive charts, built into the page for offline use.
- **Plain-JS statistics:** Pearson correlation, PCA (Jacobi eigen-decomposition) and k-NN, so no ML library is needed in the browser.
- **Python 3:** the build script uses only the standard library.
- **Playwright, NumPy and scikit-learn:** automated checks, including comparing the dashboard's statistics with scikit-learn.
- **Git:** version control.

## Installation
You only need this to rebuild or check the dashboard. To just *use* it, open `index.html`.

```bash
git clone <repo-url>
cd iris-dashboard
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # tools for the automated checks
python -m playwright install chromium
npm install                      # downloads the pinned Plotly.js used by the build
```

Requires Python 3.9+ and Node.js (for `npm`).

## Usage

**Open the dashboard:** double-click `index.html`, or open it in any modern browser. No internet connection is needed.

**Rebuild after changing the page or the data:**
```bash
python scripts/build.py
```
This takes `src/template.html` and builds the data from `data/iris.csv` and the Plotly library into `index.html`.

**Run the automated checks** (light mode, then dark mode):
```bash
python scripts/validate.py
```
The script covers:
- **Data and display:** data integrity, the summary values, every chart, filters, selection, sorting and CSV export.
- **Statistics:** the correlations, PCA results and k-NN predictions are compared with scikit-learn.
- **Theme and layout:** theme switching, text contrast, and layout at phone, tablet and desktop widths.

Screenshots are saved to `screenshots/`. To use a different Chrome or Chromium, set `CHROME_PATH=/path/to/chrome`.

**Things to try in the dashboard:**
- Untick *setosa* to see how much harder it is to tell the other two apart.
- Drag a box around the versicolor/virginica overlap in the scatter plot and watch those flowers light up in every chart.
- Switch the correlation heatmap to *setosa only*: sepal length vs. width flips from −0.12 to +0.74.
- In *Predict a flower*, choose **Borderline** and change *k* to see how the vote shifts near the boundary.

## Project Structure
```
iris-dashboard/
├── index.html          # The finished dashboard, one self-contained offline file (built)
├── src/
│   └── template.html   # Dashboard source: layout, styles and JavaScript
├── data/
│   └── iris.csv        # Fisher's Iris dataset, 150 rows (source of truth)
├── scripts/
│   ├── build.py        # Builds index.html from the template, data and Plotly
│   └── validate.py     # Automated checks in light and dark mode
├── screenshots/        # Screenshots produced by validate.py
├── package.json        # Pins the Plotly.js version
└── requirements.txt    # Python packages for the checks
```

## Roadmap
- [x] Phase 1: Data & skeleton
- [x] Phase 2: Core charts
- [x] Phase 3: Interactivity (filters, linked selection, data table, CSV export)
- [x] Phase 4: ML extras (correlations, PCA, k-NN predictor)
- [x] Phase 5: Polish (learner notes, themes, responsive layout, README)

## License
MIT License. The Iris dataset is from R. A. Fisher (1936) via the UCI Machine Learning Repository.

# Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Output | One self-contained `index.html` | Opens offline, easy to share |
| Language | HTML, CSS, vanilla JavaScript | No build step |
| Charts | Plotly.js (inlined) | Interactive hover, zoom, linked selection |
| Data | Iris CSV embedded as a JS constant | No network or file loading |
| Version control | Git + GitHub | Track roadmap phases on branches |

## Conventions
- All code, styles and data stay inside `index.html` (source data also kept in `data/iris.csv`).
- Consistent species colors across every chart.
- Works in current Chrome, Edge, Firefox and Safari.

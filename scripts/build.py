"""Embed data/iris.csv into src/template.html and write index.html."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUMERIC = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def load_rows():
    with open(ROOT / "data" / "iris.csv", newline="") as f:
        return [{**{k: float(r[k]) for k in NUMERIC}, "species": r["species"]} for r in csv.DictReader(f)]


def main():
    rows = load_rows()
    template = (ROOT / "src" / "template.html").read_text()
    data = json.dumps(rows, separators=(",", ":"))
    plotly_path = ROOT / "node_modules" / "plotly.js-dist-min" / "plotly.min.js"
    if not plotly_path.exists():
        raise SystemExit("Plotly not found: run `npm install` first")
    plotly = plotly_path.read_text()
    if "</script" in plotly.lower():
        raise SystemExit("Plotly bundle contains '</script'; cannot inline safely")
    html = template.replace("/*IRIS_DATA*/", data).replace("/*PLOTLY_JS*/", plotly)
    (ROOT / "index.html").write_text(html)
    print(f"index.html built with {len(rows)} rows ({len(html) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()

"""Phase 1 validation: data integrity, embedded data, KPI values, offline render + screenshot."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import ROOT, NUMERIC, load_rows  # noqa: E402

REF_OVERALL = {"sepal_length": 5.843, "sepal_width": 3.057, "petal_length": 3.758, "petal_width": 1.199}
REF_PETAL_LENGTH = {"setosa": 1.462, "virginica": 5.552}
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{' (' + detail + ')' if detail else ''}")


def mean(rows, k):
    return sum(r[k] for r in rows) / len(rows)


rows = load_rows()
counts = Counter(r["species"] for r in rows)
check("CSV has 150 rows", len(rows) == 150, str(len(rows)))
check("50 rows per species", set(counts.values()) == {50} and len(counts) == 3, dict(counts).__repr__())

html = (ROOT / "index.html").read_text()
m = re.search(r"const IRIS = (\[.*?\]);", html, re.S)
check("IRIS constant matches CSV", bool(m) and json.loads(m.group(1)) == rows)

overall = {k: round(mean(rows, k), 3) for k in NUMERIC}
check("Overall means match reference", overall == REF_OVERALL, str(overall))
for s, ref in REF_PETAL_LENGTH.items():
    v = round(mean([r for r in rows if r["species"] == s], "petal_length"), 3)
    check(f"{s} mean petal length = {ref}", v == ref, str(v))

# --- Browser checks ---
from playwright.sync_api import sync_playwright  # noqa: E402

shots = ROOT / "screenshots"
shots.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    errors, external = [], []
    page.on("console", lambda msg: msg.type == "error" and errors.append(msg.text))
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: not r.url.startswith("file://") and external.append(r.url))
    page.goto((ROOT / "index.html").as_uri())
    check("No console errors", not errors, "; ".join(errors))
    check("No network requests (offline)", not external, ", ".join(external))

    stats = page.evaluate("window.IRIS_STATS")
    js_overall = {k: round(v, 3) for k, v in stats["overall"].items()}
    check("JS KPI means match Python", js_overall == overall, str(js_overall))
    tiles = page.locator(".kpi .value").all_inner_texts()
    check("KPI tiles show 150 and 3", tiles[:2] == ["150", "3"], str(tiles[:2]))
    check("4 feature-mean tiles", len(tiles) == 6, str(len(tiles)))
    check("Species table has 3 rows", page.locator("#species-table tbody tr").count() == 3)
    check("4 chart cards", page.locator("#chart-grid .chart-card").count() == 4)

    # --- Phase 2: charts ---
    check("Plotly loaded (inlined)", page.evaluate("typeof Plotly === 'object'"))
    traces = page.evaluate("""() => Object.fromEntries(['chart-hist','chart-box','chart-scatter','chart-splom'].map(id => {
        const d = document.getElementById(id).data || [];
        return [id, d.map(t => ({ name: t.name, n: (t.x || t.y || (t.dimensions && t.dimensions[0].values) || []).length,
                                  dims: t.dimensions ? t.dimensions.length : 0 }))];
    }))""")
    for cid in ["chart-hist", "chart-box", "chart-scatter"]:
        tr = traces[cid]
        check(f"{cid}: 3 species traces x 50 points",
              [t["name"] for t in tr] == ["setosa", "versicolor", "virginica"] and all(t["n"] == 50 for t in tr),
              str(tr))
    sp = traces["chart-splom"]
    check("chart-splom: 3 traces x 4 dimensions", len(sp) == 3 and all(t["dims"] == 4 and t["n"] == 50 for t in sp), str(sp))

    sepal_w = [r["sepal_width"] for r in rows if r["species"] == "setosa"]
    page.select_option("#scatter-x", "sepal_width")
    page.wait_for_timeout(300)
    x0 = page.evaluate("Array.from(document.getElementById('chart-scatter').data[0].x)")
    check("Scatter X picker updates data", x0 == sepal_w)
    page.select_option("#scatter-x", "petal_length")

    petal_w = [r["petal_width"] for r in rows if r["species"] == "setosa"]
    page.select_option("#hist-feature", "petal_width")
    page.wait_for_timeout(300)
    h0 = page.evaluate("Array.from(document.getElementById('chart-hist').data[0].x)")
    check("Histogram picker updates data", h0 == petal_w)
    page.select_option("#hist-feature", "petal_length")
    page.wait_for_timeout(300)
    check("No console errors after interaction", not errors, "; ".join(errors))
    check("Still no network requests", not external, ", ".join(external))

    page.screenshot(path=str(shots / "phase2-desktop.png"), full_page=True)

    page.set_viewport_size({"width": 375, "height": 800})
    page.wait_for_timeout(600)
    overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
    check("No horizontal overflow at 375px", not overflow)
    page.screenshot(path=str(shots / "phase2-mobile.png"), full_page=True)
    browser.close()

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)

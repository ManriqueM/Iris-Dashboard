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
    check("4 chart placeholders", page.locator("#chart-grid .placeholder").count() == 4)
    page.screenshot(path=str(shots / "phase1-desktop.png"), full_page=True)

    page.set_viewport_size({"width": 375, "height": 800})
    overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
    check("No horizontal overflow at 375px", not overflow)
    page.screenshot(path=str(shots / "phase1-mobile.png"), full_page=True)
    browser.close()

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)

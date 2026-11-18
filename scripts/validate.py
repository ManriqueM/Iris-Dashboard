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
m = re.search(r"const IRIS = (\[.*?\])\.map\(", html, re.S)
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

    # --- Phase 3: interactivity ---
    kpi_samples = lambda: page.locator(".kpi .value").first.inner_text()
    table_rows = lambda: page.locator("#data-table tbody tr").count()
    trace_names = lambda cid: page.evaluate(f"document.getElementById('{cid}').data.map(t => t.name)")

    check("Data table starts with 150 rows", table_rows() == 150, str(table_rows()))
    page.click('.chip[data-species="setosa"]')
    page.wait_for_timeout(300)
    check("Setosa off: table shows 100 rows", table_rows() == 100, str(table_rows()))
    check("Setosa off: Samples KPI = 100", kpi_samples() == "100", kpi_samples())
    check("Setosa off: removed from every chart",
          all("setosa" not in trace_names(c) for c in ["chart-hist", "chart-box", "chart-scatter", "chart-splom"]))
    check("Setosa chip shows as off", page.get_attribute('.chip[data-species="setosa"]', "aria-pressed") == "false")
    check("Species table greys setosa", "off" in (page.get_attribute('#species-table tr[data-species="setosa"]', "class") or ""))

    page.click('.chip[data-species="versicolor"]')
    page.wait_for_timeout(200)
    page.click('.chip[data-species="virginica"]', force=True)  # last one: must be ignored
    page.wait_for_timeout(200)
    check("Last active species can't be turned off",
          page.get_attribute('.chip[data-species="virginica"]', "aria-pressed") == "true" and table_rows() == 50)
    page.click('.chip[data-species="setosa"]'); page.click('.chip[data-species="versicolor"]')
    page.wait_for_timeout(300)
    check("All species restored", table_rows() == 150)

    # Simulated selection of 10 flowers (ids from two species) via Plotly's event
    page.evaluate("""() => {
        const gd = document.getElementById('chart-scatter');
        const pts = [];
        gd.data.forEach((t, c) => t.customdata.slice(0, 5).forEach((cd, i) => { if (c < 2) pts.push({ curveNumber: c, pointIndex: i, customdata: cd }); }));
        gd.emit('plotly_selected', { points: pts });
    }""")
    page.wait_for_timeout(400)
    banner = page.locator("#banner-text").inner_text()
    check("Selection banner: '10 flowers selected'", banner == "10 flowers selected" and page.is_visible("#banner"), banner)
    check("Selection: table shows 10 rows", table_rows() == 10, str(table_rows()))
    check("Selection: Samples KPI = 10", kpi_samples() == "10", kpi_samples())
    sel = page.evaluate("document.getElementById('chart-splom').data.map(t => (t.selectedpoints || []).length)")
    check("Selection: scatter matrix highlights 5+5+0", sel == [5, 5, 0], str(sel))
    hist_n = page.evaluate("document.getElementById('chart-hist').data.reduce((a, t) => a + t.x.length, 0)")
    check("Selection: histograms use only selected flowers", hist_n == 10, str(hist_n))
    check("No console errors during selection", not errors, "; ".join(errors))
    page.screenshot(path=str(shots / "phase3-selection-desktop.png"), full_page=True)

    page.click("#clear-sel")
    page.wait_for_timeout(300)
    check("Clear restores full table", table_rows() == 150 and not page.is_visible("#banner"))

    # Real mouse drag over the setosa cluster (petal length 0.9–2.1, petal width 0–0.7)
    page.locator("#chart-scatter").scroll_into_view_if_needed()
    box = page.evaluate("""() => {
        const gd = document.getElementById('chart-scatter'), fl = gd._fullLayout, r = gd.getBoundingClientRect();
        const px = v => r.left + fl.margin.l + fl.xaxis.l2p(v), py = v => r.top + fl.margin.t + fl.yaxis.l2p(v);
        return [px(0.9), py(0.75), px(2.1), py(0.0)];
    }""")
    page.mouse.move(box[0], box[1]); page.mouse.down()
    page.mouse.move((box[0] + box[2]) / 2, (box[1] + box[3]) / 2, steps=5)
    page.mouse.move(box[2], box[3], steps=5); page.mouse.up()
    page.wait_for_timeout(500)
    check("Real drag-select over setosa selects 50", table_rows() == 50 and
          page.locator("#banner-text").inner_text() == "50 flowers selected", page.locator("#banner-text").inner_text())
    page.mouse.dblclick(box[2] + 200, box[1] - 60); page.wait_for_timeout(500)
    check("Double-click on scatter clears selection", table_rows() == 150 and not page.is_visible("#banner"))

    # Sort + export
    page.click('#data-table th button[data-key="petal_length"]')  # first click on a measure = descending
    page.wait_for_timeout(200)
    first = page.locator("#data-table tbody tr").first.locator("td").nth(4).inner_text()
    check("Sort petal length desc: first row 6.9", first == "6.9", first)
    with page.expect_download() as dl:
        page.click("#export-csv")
    csv_text = Path(dl.value.path()).read_text().strip().splitlines()
    table_ids = page.evaluate("Array.from(document.querySelectorAll('#data-table tbody tr td:first-child')).map(td => td.textContent)")
    check("Export: header + 150 rows, same order as table",
          csv_text[0].startswith("id,species") and len(csv_text) == 151 and [l.split(",")[0] for l in csv_text[1:]] == table_ids,
          f"{len(csv_text)} lines, file {dl.value.suggested_filename}")
    page.click('.chip[data-species="virginica"]'); page.wait_for_timeout(300)
    with page.expect_download() as dl2:
        page.click("#export-csv")
    n2 = len(Path(dl2.value.path()).read_text().strip().splitlines()) - 1
    check("Export respects filters (100 rows)", n2 == 100, str(n2))
    page.click('.chip[data-species="virginica"]'); page.wait_for_timeout(300)

    # --- Phase 4: ML extras vs scikit-learn ---
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.preprocessing import StandardScaler

    SP = ["setosa", "versicolor", "virginica"]
    X = np.array([[r[k] for k in NUMERIC] for r in rows])
    y = np.array([SP.index(r["species"]) for r in rows])
    TOL = 1e-6

    ok = True
    for scope in ["all"] + SP:
        subset = rows if scope == "all" else [r for r in rows if r["species"] == scope]
        js = np.array(page.evaluate(f"IRIS_ML.corr({json.dumps(subset)})"))
        ref = np.corrcoef((X if scope == "all" else X[y == SP.index(scope)]).T)
        ok &= np.allclose(js, ref, atol=TOL)
    check("Correlations match numpy (all + each species)", ok)

    Zs = StandardScaler().fit_transform(X)
    pca = PCA(2).fit(Zs)
    js_ratio = page.evaluate("IRIS_ML.ratio.slice(0, 2)")
    check("PCA variance ratio matches sklearn", np.allclose(js_ratio, pca.explained_variance_ratio_, atol=TOL),
          f"{js_ratio[0]:.4f}, {js_ratio[1]:.4f}")
    js_scores = np.array(page.evaluate("IRIS_ML.scores"))
    ref_scores = pca.transform(Zs)
    signs = np.sign((js_scores * ref_scores).sum(0))
    check("PCA scores match sklearn (up to sign)", np.allclose(js_scores, ref_scores * signs, atol=TOL))
    check("PCA: setosa on the left of PC1", js_scores[y == 0, 0].mean() < 0)

    rng = np.random.default_rng(0)
    lo, hi = X.min(0), X.max(0)
    tests = np.round(rng.uniform(lo, hi, size=(20, 4)), 1).tolist() + \
        [[5.0, 3.4, 1.5, 0.2], [5.9, 2.8, 4.3, 1.3], [6.6, 3.0, 5.6, 2.0], [6.0, 2.8, 4.9, 1.7]]
    mism, ties = [], 0
    for k in [1, 5, 15]:
        clf = KNeighborsClassifier(k).fit(Zs, y)
        ref = clf.predict(StandardScaler().fit(X).transform(np.array(tests)))
        js = page.evaluate(f"{json.dumps(tests)}.map(p => IRIS_ML.knn(p, {k}))")
        for p, r, j in zip(tests, ref, js):
            ties += j["tie"]
            if SP[r] != j["pred"] and not j["tie"]:
                mism.append((k, p, SP[r], j["pred"]))
    check("k-NN predictions match sklearn (24 points x k=1,5,15)", not mism, f"{len(mism)} mismatches, {ties} vote ties")

    from sklearn.model_selection import LeaveOneOut, cross_val_score
    loo_ok, detail = True, []
    for k in [1, 3, 5, 7, 9, 15]:
        ref = int(cross_val_score(KNeighborsClassifier(k), Zs, y, cv=LeaveOneOut()).sum())
        js = page.evaluate(f"IRIS_ML.loo({k})")
        loo_ok &= ref == js; detail.append(f"k={k}:{js}")
    check("Leave-one-out accuracy matches sklearn for every k", loo_ok, " ".join(detail))

    # UI: heatmap toggle
    z_all = page.evaluate("document.getElementById('chart-corr').data[0].z[0][1]")
    page.select_option("#corr-scope", "setosa"); page.wait_for_timeout(300)
    z_set = page.evaluate("document.getElementById('chart-corr').data[0].z[0][1]")
    check("Heatmap toggle: sepal L-W negative overall, positive in setosa", z_all < 0 < z_set, f"{z_all:.3f} → {z_set:.3f}")
    page.select_option("#corr-scope", "all")

    # UI: predictor
    n_scatter = lambda: page.evaluate("document.getElementById('chart-scatter').data.length")
    check("No overlay before predictor is used", n_scatter() == 3)
    page.click('[data-preset="0"]'); page.wait_for_timeout(400)
    pred = page.locator("#pred-species").inner_text().strip()
    check("Preset 'Typical setosa' predicts setosa", pred == "setosa", pred)
    star_scatter = page.evaluate("document.getElementById('chart-scatter').data.some(t => t.marker && t.marker.symbol === 'star')")
    star_pca = page.evaluate("document.getElementById('chart-pca').data.some(t => t.marker && t.marker.symbol === 'star')")
    seg = page.evaluate("document.getElementById('chart-pca').data.find(t => t.name === 'neighbours').x.filter(v => v === null).length")
    check("Star + k neighbour lines on scatter and PCA", star_scatter and star_pca and seg == 5, f"lines={seg}")
    page.fill("#pred-petal_length", "6"); page.dispatch_event("#pred-petal_length", "input")
    page.fill("#pred-petal_width", "2.2"); page.dispatch_event("#pred-petal_width", "input")
    page.wait_for_timeout(400)
    pred2 = page.locator("#pred-species").inner_text().strip()
    check("Moving sliders to large petals predicts virginica", pred2 == "virginica", pred2)
    page.select_option("#pred-k", "15"); page.wait_for_timeout(300)
    check("k=15 shows LOO 145/150", "145/150" in page.locator("#pred-result").inner_text())
    page.click('[data-preset="3"]'); page.wait_for_timeout(300)
    page.screenshot(path=str(shots / "phase4-desktop-predictor.png"), full_page=True)
    page.uncheck("#pred-show"); page.wait_for_timeout(300)
    check("'Show on charts' off removes overlay", n_scatter() == 3)
    page.check("#pred-show"); page.wait_for_timeout(300)

    # UI: PCA follows filters and selection
    page.click('.chip[data-species="setosa"]'); page.wait_for_timeout(300)
    names = page.evaluate("document.getElementById('chart-pca').data.map(t => t.name)")
    check("PCA follows species filter", "setosa" not in names and "versicolor" in names, str(names))
    page.click('.chip[data-species="setosa"]'); page.wait_for_timeout(300)
    page.evaluate("""() => { const gd = document.getElementById('chart-scatter');
        const pts = gd.data[0].customdata.slice(0, 7).map((cd, i) => ({ curveNumber: 0, pointIndex: i, customdata: cd }));
        gd.emit('plotly_selected', { points: pts }); }""")
    page.wait_for_timeout(400)
    psel = page.evaluate("document.getElementById('chart-pca').data.slice(0, 3).map(t => (t.selectedpoints || []).length)")
    check("PCA follows linked selection", psel == [7, 0, 0], str(psel))
    page.click("#clear-sel"); page.wait_for_timeout(300)

    check("No console errors overall", not errors, "; ".join(errors))
    check("No network requests overall", not external, ", ".join(external))
    page.screenshot(path=str(shots / "phase3-desktop.png"), full_page=True)

    page.set_viewport_size({"width": 375, "height": 800})
    page.wait_for_timeout(600)
    page.click('.chip[data-species="setosa"]'); page.wait_for_timeout(300)
    overflow = page.evaluate("document.documentElement.scrollWidth > window.innerWidth")
    check("No horizontal overflow at 375px", not overflow)
    page.evaluate("window.scrollTo(0, 0)"); page.wait_for_timeout(300)
    check("Filter chips visible at 375px", page.is_visible('.chip[data-species="virginica"]'))
    page.screenshot(path=str(shots / "phase3-mobile.png"), full_page=True)
    page.screenshot(path=str(shots / "phase3-mobile-top.png"))
    browser.close()

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)

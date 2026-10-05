# Who ends up owning AI? — equity pass-through model

Traces each dollar of equity in the leading AI firms through four layers:

```
company  →  holder type  →  beneficiary account  →  wealth bucket
```

The live page is a single static HTML file (d3 + d3-sankey) that reads assumption
sets from JSON. Nothing runs server-side, so it hosts anywhere static files do.

## Layout

```
index.html         the page (served at /ai-equity/ on the GitHub Pages user site)
data/              generated: assumptions.js bundle (v2 only), raw JSON copy, model_output_*.json
config/            assumption sets (JSON) + sets.json manifest
  assumptions_v1.json   v1 heuristic (regression baseline only; not shipped to the page)
  assumptions_v2.json   v2 researched priors with per-row source + confidence
src/model/
  propagate.py     pure-python pass-through; --regress checks v1 outputs; writes tables/
  build_v2.py      every v2 number with its rationale; regenerates assumptions_v2.json
  build_web.py     bundles config/*.json -> data/assumptions.js (+ raw JSON copies)
  validate.py      spec checks: conservation, Z.1 / TIC / TPC anchors
  methods_note.py  docs/METHODS_*.md from a config
tables/            tidy CSVs of each matrix with source + confidence columns
docs/              audit note, research logs, hosting notes
```

## Run locally

```bash
python3 src/model/propagate.py config/assumptions_v1.json --regress     # must print PASS
python3 src/model/propagate.py config/assumptions_v2.json --out data/model_output_v2.json --tables tables/v2
python3 src/model/build_web.py
python3 -m http.server 8000 --directory ..    # then open http://localhost:8000/ai-equity/
```

`index.html` loads `data/assumptions.js` via a plain `<script>` tag, so it also works
when double-clicked from disk (browsers block `fetch()` of local JSON).

## Deploy

This folder lives inside the `AlexShypula.github.io` Jekyll site. Jekyll copies
`index.html` and `data/` through untouched (no front matter), so the page is served at
`https://alexshypula.github.io/ai-equity/`. `src/`, `config/` and `tables/` are excluded
from the build in the site's `_config.yml`; `docs/*.md` render as themed pages.

**Run `python3 src/model/build_web.py` before committing** whenever a config changes:
`data/assumptions.js` is a committed build product, not generated on the server.
See `docs/HOSTING.md`.

## Adding an assumption set

1. Copy `config/assumptions_v2.json`, edit values, bump `_meta.version`.
2. Fill `sources.<layer>.<row>` with `{source, confidence, note}` for every row you touch.
3. Add it to `config/sets.json`; run `build_web.py`.
4. `?set=<id>` in the URL selects a set directly (e.g. `index.html?set=v1`).

## Validation

- Every row is normalized to 1 at compute time; the table flags raw rows that don't sum to 100.
- `propagate.py --regress` reproduces the v1 handoff numbers to within 0.05 points.
- Total flow equals total company value at every layer by construction.

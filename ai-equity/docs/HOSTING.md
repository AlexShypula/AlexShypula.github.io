# Hosting

**Current setup (Oct 2026): subfolder of the `AlexShypula.github.io` user site.**
The page is at `https://alexshypula.github.io/ai-equity/`. GitHub Pages builds the repo
with Jekyll; files without front matter (`index.html`, `data/*`) are copied verbatim, and
`src/`, `config/`, `tables/`, `SPEC.md`, `README.md`, `reference_v1.html` are excluded
in the site's `_config.yml`. There is no build step on the server, so regenerate
`data/assumptions.js` locally (`python3 src/model/build_web.py`) and commit it.

Things to keep true:

- **Relative paths only.** `index.html` references `data/assumptions.js` without a
  leading slash so it works under `/ai-equity/`.
- **No front matter** in `index.html`, or Jekyll will run Liquid over the d3 code.
- **Fonts and CDNs** (Google Fonts, cdnjs, jsdelivr) are HTTPS; Pages is HTTPS-only.
- **Caveat banner.** Private-lab cap tables are reconstructions; the page labels them
  low-confidence. Consider a one-liner until Anthropic's S-1 is public.
- **Freshness.** `_meta.as_of` in each config records the data vintage. If the 13F
  pipeline is ever run quarterly, add one set per quarter; the dropdown becomes the
  spec's as-of selector.

## Alternative kept for reference: dedicated repo with Actions

The original plan was a standalone repo deploying with `actions/upload-pages-artifact`,
running the v1 regression test before every publish. It is a better fit if the model
source grows (quarterly 13F ingestion, Monte Carlo) and you want CI on it. The workflow
was dropped when the project moved into the user site; it is easy to restore.

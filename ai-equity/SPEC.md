# AI equity pass-through model — v2 spec

## Goal

Estimate who ultimately owns the economic value of the leading AI firms, by tracing each dollar of equity through four layers:

```
company  →  holder type  →  beneficiary account  →  wealth bucket
(NVDA…)     (index fund…)   (US 401k, foreign       (top 0.1% … bottom 50%,
                             pension, offshore…)      public/sovereign, nonprofit)
```

v1 (`reference_v1.html`, `assumptions_v1.json`) is a working interactive Sankey where every layer is a hand-set heuristic matrix. v2 should replace as many heuristics as possible with data, keep the rest explicit, and quantify uncertainty. The output is a research tool, not a point estimate.

## Files in this handoff

- `SPEC.md`: this document.
- `assumptions_v1.json`: v1 defaults (company values, all three matrices, labels, benchmarks, confidence notes). Treat it as the schema seed and as the fallback prior for anything data can't pin down.
- `reference_v1.html`: the v1 front end (d3 + d3-sankey, single file). Reuse its visual design and interactions; v2 should load model output from JSON instead of hardcoding.

## Model

Let `V_c` be company value. The pass-through is three row-stochastic matrices:

- `A[c, h]`: share of company c held by holder type h
- `B[h, b]`: share of holder type h's holdings attributable to beneficiary account b
- `K[b, k]`: share of beneficiary account b owned by wealth bucket k

Flows: `V_c · A[c,h] · B[h,b] · K[b,k]`. Keep flows tagged by origin company through all layers so the Sankey can color by company. Bucket totals are also split by whether the beneficiary is US or foreign (`beneficiary_is_us` in the JSON).

Keep the v1 category lists unless data clearly argues for a change; if categories change, version the schema.

## Data sources by layer

### Layer 0: company values
Public: market cap at a chosen as-of date (any price source; record the date). Private (OpenAI, Anthropic, others to add): last-round post-money from press, flagged low-confidence. Allow per-company overrides in config.

### Layer A: company → holder type
- **SEC 13F-HR information tables** (EDGAR, XML). Filed quarterly by managers with ≥$100M in 13F securities, within 45 days of quarter end. Aggregate holdings by CUSIP for each ticker. EDGAR requires a descriptive User-Agent header; respect rate limits (~10 req/s).
- **Filer classification.** Map each 13F filer to a holder type. Suggested approach: hand-label the top ~200 filers by holdings in these tickers (they cover most of the 13F total), then use name rules plus an LLM-assisted classifier for the tail with a manual review file. Store mappings in a versioned CSV (`filer_cik, name, holder_type, notes`).
- **Insiders.** DEF 14A beneficial ownership tables (and Form 4 for updates). Use economic ownership, not voting control; record dual-class structure separately.
- **Residual.** Shares outstanding minus 13F minus insiders = "Retail & other direct" (includes non-filing foreign holders and small managers).
- **Known 13F issues to handle:** investment discretion ≠ beneficial ownership; possible double counting across advisers and sub-advisers; option positions (exclude or delta-adjust); share-class aggregation for GOOGL/GOOG.
- **Private labs.** No filings. Build a small hand-curated cap table from reporting, with a source URL and confidence per row.

### Layer B: holder type → beneficiary account
- **Federal Reserve Z.1 table L.223 (corporate equities by holder sector).** Use as an aggregate cross-check on holder-sector shares, and for the foreign ("rest of world") share.
- **ICI Investment Company Fact Book.** Share of mutual fund and ETF assets in retirement accounts versus taxable, and institutional versus retail.
- **Treasury TIC SHL annual survey** (foreign holdings of US securities). Foreign equity by country and official versus private. As of June 2025: about $13.8T foreign portfolio US equity, about $2.2T official; UK, Cayman and Canada about $2.1T each. Note that it records custody country, not ultimate owner.
- **Tax Policy Center (Rosenthal and Burke)** decomposition of US equity ownership (foreign about 40%, retirement about 30%, taxable about 25% in 2019) as a sanity target.
- **Large foreign holders with public holdings files** (e.g., NBIM, CPP Investments, other major pension funds) to calibrate the foreign sovereign and pension columns for these specific tickers.
- **Offshore round-tripping.** Literature on reallocating tax-haven holdings to nationality (e.g., Coppola, Maggiori, Neiman and Schreger) for the share of Cayman/BVI holdings that is ultimately US-owned. Keep this as an explicit, tunable parameter.

### Layer K: beneficiary account → wealth bucket
- **Fed Distributional Financial Accounts (DFA)** for the distribution of corporate equities and mutual fund shares (anchors "US taxable accounts"; Q3 2025: top 1% 50.2%, 90th–99th 37.2%, 50th–90th 11.6%, bottom 50% about 1%).
- **Survey of Consumer Finances public microdata** (latest available wave). Compute, by wealth percentile, the distribution of (a) retirement account balances, (b) directly and indirectly held equity in taxable accounts, and (c) DB pension coverage proxies. Use survey weights; report replicate-weight standard errors where feasible.
- **Foreign rows.** No equivalent microdata; keep as priors (v1 values), optionally informed by OECD wealth-distribution data and national pension coverage. Percentiles are within-country.

## Uncertainty

Represent each heuristic row as a Dirichlet prior centered on its point estimate, with concentration reflecting confidence (data-derived rows tight, guessed rows loose). Monte Carlo the pipeline (e.g., 5–10k draws) and report median and 90% intervals for key outputs. Also provide one-at-a-time sensitivity: which rows move "top 1% share" and "public/sovereign share" most.

## Outputs

1. `model_output.json`: nodes, links (with `origin`), bucket totals overall, US, and foreign, and interval estimates. The front end consumes this file.
2. `tables/`: tidy CSVs of each matrix with a `source` and `confidence` column per row.
3. Front end: v1 design, plus an as-of date selector if multiple quarters are processed, interval bars in the summary, and a toggle between data-derived and v1 heuristic rows for each matrix.
4. Short methods note (markdown) generated from the configs, listing every assumption with its source.

## Validation checks

- Each row sums to 1; total flow equals the sum of company values at every layer.
- 13F + insiders + residual reconciles to shares outstanding per ticker (flag >5% gaps).
- Aggregate holder-sector shares across the megacaps are within a reasonable band of Z.1 L.223.
- The US taxable channel reproduces DFA by construction; the US-household total should land between DFA and a flatter distribution as the retirement share rises.
- The foreign share of megacap equity is compared against TIC and TPC, with the gap explained.

## Suggested structure

```
ai-equity/
  config/          companies.yaml, overrides, priors (seeded from assumptions_v1.json)
  data/raw/        cached downloads (gitignored)
  data/mappings/   filer_classification.csv, private_cap_tables.csv
  src/ingest/      sec_13f.py, proxy.py, z1.py, dfa.py, scf.py, tic.py
  src/model/       build_matrices.py, propagate.py, montecarlo.py
  web/             index.html (from reference_v1.html), model_output.json
  notebooks/       sanity checks
```

Python for ingestion and modeling; keep the front end a single static HTML file.

## Milestones

1. Port v1 to the config + `propagate.py` + JSON front end with identical outputs (regression test against `v1_outputs_pct_of_total` in the JSON).
2. Layer A from 13F + proxies for the five public firms, one quarter.
3. Layer K from SCF and DFA.
4. Layer B calibration (ICI, Z.1, TIC, named foreign holders).
5. Monte Carlo, sensitivity and the methods note.
6. Optional: multiple quarters to show how concentration in AI equity shifts over time.

## Open questions for the user

- Wealth or income percentiles as the primary bucket definition?
- Which additional firms (Broadcom, TSMC, Oracle, xAI/SpaceX, Mistral)?
- Should Big Tech strategic stakes in private labs be resolved recursively through the parent's own holder mix (more correct) rather than a blended row?

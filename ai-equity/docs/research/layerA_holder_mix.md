# Layer A research: who owns the economic equity of NVDA, GOOGL/GOOG, MSFT, AMZN, META (2026-10-05)

Primary sources: SEC DEF 14A proxies, Form 4s, 10-Q covers, Fed Z.1, ICI, Vanguard and BlackRock filings. 13F aggregates from api.nasdaq.com/api/company/{TICKER}/institutional-holdings.

**Key finding: headline "% institutional" figures are overstated by ~8–10 points for 2026.** On 2026-01-12 Vanguard moved holdings from The Vanguard Group Inc. into two new advisers (Vanguard Capital Management, Vanguard Portfolio Management). Nasdaq still carries a stale "Vanguard Group Inc" row (12/31/2025) alongside the new rows (6/30/2026), double counting ~9% per ticker. Sources: https://corporate.vanguard.com/content/corporatesite/us/en/corp/articles/update-on-our-us-investment-advisory-structure.html ; https://themonitor.gibsondunn.com/new-considerations-for-reporting-beneficial-ownership-by-the-vanguard-group-in-company-proxy-statements/ . Tables below subtract the stale row.

## 1. 13F institutional ownership, Q2 2026 (6/30/2026 filings), Nasdaq retrieved 2026-10-05

| Ticker | Nasdaq headline | De-duplicated | Denominator | Conf |
|---|---|---|---|---|
| NVDA | 79.53% (6,273 holders) | **70.1%** | 24,100M | high / med-high |
| MSFT | 84.33% | **74.7%** | 7,426M | same |
| AMZN | 75.58% | **67.7%** | 10,786M | same |
| META | 86.82% of Class A | **67.3% of A+B** | 2,547.5M (10-Q 7/24/2026) | same |
| GOOGL (A) / GOOG (C) | 89.57% / 69.42% | — | 5,868M / 5,527M | |
| Alphabet all classes | — | **66.6%** | 12,230M A+B+C (10-Q 7/15/2026) | med-high |

## 2. Top holders, % of economic shares at 6/30/2026 (Vanguard = VCM+VPM+VFTC; Capital Group = 3 filers)

| Holder | NVDA | MSFT | AMZN | META | GOOGL+GOOG |
|---|---|---|---|---|---|
| Vanguard | 9.11 | 9.37 | 7.53 | 7.63 | 7.59 |
| BlackRock | 8.06 | 8.18 | 6.94 | 6.81 | 6.79 |
| State Street | 4.19 | 4.25 | 3.68 | 3.61 | 3.52 |
| FMR (Fidelity) | 4.26 | 2.50 | 3.39 | 3.76 | 3.05 |
| Geode | 2.52 | 2.55 | 2.16 | 2.16 | 2.17 |
| JPMorgan | 1.86 | 1.82 | 1.56 | 1.80 | 1.88 |
| Capital Group | 1.68 | 2.74 | 2.09 | 3.89 | 2.32 |
| T. Rowe | 1.53 | 1.18 | 1.01 | 1.21 | 1.31 |
| Norges Bank | 1.35 | 1.38 | 1.30 | 1.28 | 1.27 |
| Invesco (mostly QQQ) | 1.37 | 1.35 | 1.33 | 1.51 | 1.29 |
| **Index proxy from top 40 holders** | **28.1** | **28.3** | **23.9** | **23.7** | **23.5** |

Index proxy weights: Vanguard 100%, Geode 100%, State Street 95%, BlackRock 90%, Schwab 95%, Northern Trust 80%, Invesco 80%, L&G 80%, UBS AM/Amundi/BNY 60%, Nuveen 50%, FMR 10% (Fidelity index funds are sub-advised by Geode). Berkshire holds 0.87% of Alphabet.

BlackRock active/passive (Q2 2026 earnings release, high): equity AUM $8,888B; active equity $619B (~7%); equity ETFs $4,723B; non-ETF index ~$3,546B → ~93% index/ETF.

Proxy cross-checks: NVDA (3/23/2026) BlackRock 7.43%, VCM 7.31%; MSFT 2025 proxy Vanguard 8.95%, BlackRock 7.30% (stale 13G); AMZN Vanguard 7.2%, BlackRock 5.9%; META BlackRock 7.2%, FMR 6.1% of Class A.

## 3. Insider economic ownership (latest proxies)

| Company / person | Shares | % economic | As of | Source | Conf |
|---|---|---|---|---|---|
| NVDA – Jensen Huang | 870.6M | 3.58% of 24,312M | 2026-03-23 | sec.gov/Archives/edgar/data/1045810/000104581026000036/nvda-20260512.htm | high |
| NVDA – D&O as group (14) | 957.3M | 3.94% | 2026-03-23 | same | high |
| Alphabet – Larry Page | 389.1M B + ~390.3M C ≈ 779M | ~6.4% | B 2026-04-06; C last Form 4 2022-04-19 | sec.gov/Archives/edgar/data/1652044/000130817926000342/goog-20260424.htm | B high; C low-med |
| Alphabet – Sergey Brin | 358.9M B + 359.5M C ≈ 718.5M | ~5.9% | 2026-04/08 | proxy; Form 4 2026-08-07 | high |
| Alphabet – Page + Brin | ~1,498M | **~12.2%** of 12,230M | | derived | medium |
| Alphabet – other insiders (Doerr, Pichai) | ~23M | ~0.2% | 2026-04-06 | proxy | high |
| MSFT – D&O as group (18) | 2.28M | 0.03% | 2025-09-30 | sec.gov/Archives/edgar/data/789019/000119312525245150/d908201ddef14a.htm | high |
| MSFT – Steve Ballmer (not an insider) | ~333.25M | ~4.5% | aggregator, old filings | gurufocus; 247wallst 2026-06-11 | medium |
| MSFT – Gates Foundation Trust | 0 (sold last 7.7M Q1 2026) | 0% | Q1 2026 13F | 247wallst 2026-05-16 | medium |
| MSFT – Bill Gates personally | unknown (aggregators show stale 103.4M = 1.39%) | ? | pre-2020 | | not verified |
| AMZN – Jeff Bezos beneficial | 950.4M | 8.8% of 10,751M | 2026-02-24 | sec.gov/Archives/edgar/data/1018724/000110465926041026/tm261382-1_def14a.htm | high |
| AMZN – of which MacKenzie Scott's (Bezos votes, no investment power) | 68.2M | 0.63% | | same | med-high |
| AMZN – Bezos own economic | ~882.2M | **~8.2%** | | derived | med-high |
| META – Mark Zuckerberg | 341.8M B (99.8% of B) | **13.4–13.5%** of 2,538M; 60.8% of votes | 2026-04-01 | sec.gov/Archives/edgar/data/1326801/000162828026025532/meta-20260416.htm | high |

## 4. Economy-wide reference points

| Metric | Value | As of | Source | Conf |
|---|---|---|---|---|
| Index domestic-equity MFs + ETFs, share of US market cap | 19% | YE2025 | ICI 2026 Fact Book Fig 2.6 | high |
| Active domestic-equity MFs + ETFs | 11% | YE2025 | same | high |
| Index funds' share of Russell 3000 (FactSet) | 23% | 2025-12-31 | Vanguard "Setting the record straight" | high |
| Chinco & Sammon (JFE 2024): all passive incl. internal/closet indexing | 33.5% of US market (2021) vs 16% index funds | 2021 | sciencedirect S0304405X24000837 | high |
| Z.1 L.224 Q4 2025 ($111.4T total): households (incl. HF, nonprofits) 42.4%, ROW 18.4%, MF 15.4%, ETF 9.7%, pensions 8.9%, nonfin corps 3.3%, insurers 1.3% | | 2025 Q4 | federalreserve.gov/releases/z1/20260319/html/l224.htm | high |
| Goldman: households directly own 38%; foreign 18% record | | ~2025 | streetinsider / investing.com | medium |

## 5. Hedge fund ownership of megacaps
- GS Hedge Fund Trend Monitor (Feb 2025): HF own avg 3% of an S&P 500 stock; ~0% for low-concentration large caps (low-med).
- GS universe start Q3 2026: 991 funds, $3.4T long ≈ ≤4% of $83T US public equity (medium).
- VIP list May 2026: AMZN, META, MSFT, NVDA, GOOGL, AAPL most popular. Mag-7 ≈ 19% of HF US net exposure (Aug 2026).
- Bloomberg 13F wrap 2025-08-14: HF hold $47B of MSFT ≈ 1.3% (medium). No per-company 2026 figures found.

## Agent's best-estimate rows (% of economic shares, mid-2026)

| Ticker | Insiders | Index | Active | Pension/insurer/SWF direct | Hedge funds | Retail & other direct |
|---|---|---|---|---|---|---|
| NVDA | 4.0 | 29 | 34.6 | 3.5 | 3.0 | 25.9 |
| GOOGL/GOOG | 12.4 | 25 | 36.6 | 3.0 | 2.0 | 21.0 |
| MSFT | 4.5 | 30 | 39.2 | 3.5 | 2.0 | 20.8 |
| AMZN | 8.8 | 26 | 35.2 | 3.5 | 3.0 | 23.5 |
| META | 13.5 | 25 | 36.1 | 3.2 | 3.0 | 19.2 |

Notes: "Active" includes ~6–8 points of wealth-management/brokerage 13F filers (JPM, MS, BofA, GS, Wells, RBC, UBS) that are economically advised retail accounts. Pension/SWF column is direct holdings only; index mandates run by BlackRock/State Street for pensions sit in "Index".

## Could not verify
Larry Page's Class C since April 2022 (insider figure could be up to ~3 pts high); Ballmer and Gates current holdings; Goldman's full ownership chart; per-ticker HF ownership 2026; Sept 2026 Z.1 release; other aggregators' institutional %; active/index weights for mixed managers are judgment calls.

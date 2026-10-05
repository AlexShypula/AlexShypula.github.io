# Methods note — v1-heuristic (generated from config, 2026-10-05)

As of: n/a

v1 heuristic set from the Oct 2026 handoff. Every matrix row is a hand-set guess; only the US-taxable row is data (Fed DFA Q3 2025). Kept as the fallback prior and regression baseline.

## Method

Each dollar of company value is split by holder type, then by the beneficiary accounts behind each holder type, then by the wealth percentile of the households holding those accounts. Flows keep the color of the company they started in, so you can see how each firm's value disperses.

Anchors: Fed DFA Q3 2025 (top 1% hold 50.2% of household corporate equities and mutual funds; 90th–99th percentiles 37.2%; 50th–90th 11.6%). Tax Policy Center (Rosenthal and Burke) estimated foreigners own about 40% of US corporate equity overall; that figure includes direct investment stakes, so megacap defaults here sit nearer 30%.

Foreign split: the June 2025 TIC survey puts foreign portfolio holdings of US equities near $13.8T, about $2.2T of it held by official institutions, with the UK, Cayman Islands and Canada each near $2.1T. Cayman and UK figures reflect custody location, not the nationality of the final owner, so those rows are the loosest guesses here. Percentiles are within each country, so the "Next 40%" in Canada is far richer globally than the bottom 50% anywhere.

Not modeled: dual-class voting control (economic shares only), liquidation preferences on private stock, founder charitable pledges, cross-holdings beyond the strategic-stake shortcut, and the difference between wealth and income percentiles. Treat outputs as order-of-magnitude, not estimates.

## Confidence by layer

- **company_values**: medium (public caps approximate mid-2026; private = last round post-money)
- **public_holder_mix**: low-medium (13F-style heuristic, insider stakes approximate)
- **private_holder_mix**: low (cap tables not public; illustrative)
- **holder_to_beneficiary**: low (look-through guesses anchored loosely to TPC and TIC)
- **beneficiary_to_bucket**: US taxable row = Fed DFA Q3 2025; other rows are guesses

## Layer A: company value ($B) and holder mix (%)

| Row | Value $B | Founders & insiders | Index funds | Active managers | Pensions, insurers & SWFs | Hedge funds | Retail & other direct | Big Tech strategic stakes | VC & growth funds | Employee equity pools | Nonprofit parent | Confidence | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Nvidia | 5000 | 4 | 22 | 25 | 9 | 5 | 35 | 0 | 0 | 0 | 0 | — | — |
| Alphabet | 4500 | 12 | 20 | 25 | 8 | 5 | 30 | 0 | 0 | 0 | 0 | — | — |
| Microsoft | 3300 | 5 | 24 | 28 | 10 | 4 | 29 | 0 | 0 | 0 | 0 | — | — |
| Amazon | 2700 | 9 | 21 | 28 | 8 | 5 | 29 | 0 | 0 | 0 | 0 | — | — |
| Meta | 1500 | 13 | 21 | 27 | 8 | 5 | 26 | 0 | 0 | 0 | 0 | — | — |
| Anthropic | 965 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 45 | 30 | 0 | — | — |
| OpenAI | 852 | 0 | 0 | 0 | 0 | 0 | 0 | 33 | 23 | 18 | 26 | — | — |

## Layer B: holder type → beneficiary account (%)

| Row | Founder stakes | Employee holdings | US taxable accounts | US 401(k)s & IRAs | US DB pensions & insurance | Endowments & foundations | Foreign sovereign & official | Foreign pensions & insurers | Foreign funds & retail | Offshore vehicles | Foreign family offices & HNW | Confidence | Source |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Founders & insiders | 100 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| Index funds | 0 | 0 | 20 | 40 | 10 | 5 | 3 | 6 | 12 | 2 | 2 | — | — |
| Active managers | 0 | 0 | 20 | 30 | 15 | 5 | 4 | 8 | 12 | 3 | 3 | — | — |
| Pensions, insurers & SWFs | 0 | 0 | 0 | 0 | 50 | 10 | 18 | 20 | 0 | 0 | 2 | — | — |
| Hedge funds | 0 | 0 | 30 | 0 | 15 | 20 | 2 | 3 | 0 | 25 | 5 | — | — |
| Retail & other direct | 0 | 0 | 45 | 15 | 0 | 0 | 8 | 8 | 10 | 7 | 7 | — | — |
| Big Tech strategic stakes | 0 | 0 | 22 | 28 | 10 | 5 | 5 | 8 | 12 | 5 | 5 | — | — |
| VC & growth funds | 0 | 0 | 30 | 0 | 15 | 20 | 15 | 5 | 0 | 10 | 5 | — | — |
| Employee equity pools | 0 | 100 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| Nonprofit parent | 0 | 0 | 0 | 0 | 0 | 100 | 0 | 0 | 0 | 0 | 0 | — | — |

## Layer K: beneficiary account → wealth bucket (%)

| Row | Top 0.1% | Next 0.9% | Next 9% | Next 40% | Bottom 50% | Public / sovereign | Nonprofits | Confidence | Source |
|---|---|---|---|---|---|---|---|---|---|
| Founder stakes | 100 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| Employee holdings | 45 | 40 | 13 | 2 | 0 | 0 | 0 | — | — |
| US taxable accounts | 24.2 | 26 | 37.2 | 11.6 | 1 | 0 | 0 | — | — |
| US 401(k)s & IRAs | 5 | 12 | 45 | 33 | 5 | 0 | 0 | — | — |
| US DB pensions & insurance | 2 | 5 | 28 | 47 | 18 | 0 | 0 | — | — |
| Endowments & foundations | 0 | 0 | 0 | 0 | 0 | 0 | 100 | — | — |
| Foreign sovereign & official | 0 | 0 | 0 | 0 | 0 | 100 | 0 | — | — |
| Foreign pensions & insurers | 2 | 5 | 25 | 45 | 23 | 0 | 0 | — | — |
| Foreign funds & retail | 12 | 18 | 40 | 25 | 5 | 0 | 0 | — | — |
| Offshore vehicles | 30 | 25 | 15 | 5 | 0 | 0 | 25 | — | — |
| Foreign family offices & HNW | 55 | 35 | 10 | 0 | 0 | 0 | 0 | — | — |

## Benchmarks carried in the config

- **fed_dfa_q3_2025_corporate_equities_mutual_funds**: {"Top 0.1%": 24.2, "Next 0.9%": 26, "Next 9%": 37.2, "Next 40%": 11.6, "Bottom 50%": 1} — Federal Reserve Distributional Financial Accounts; excludes pension entitlements
- **tic_june_2025**: {"foreign_portfolio_us_equity_busd": 13840, "foreign_official_us_equity_busd": 2227, "uk_busd": 2056, "cayman_busd": 2156, "canada_busd": 2063} — Treasury SHL annual survey, June 30 2025 (custody country, not ultimate owner)
- **tpc_2019**: {"foreign_share_us_corporate_equity": 40, "us_retirement_accounts": 30, "us_taxable_accounts": 25} — Rosenthal & Burke, Tax Policy Center (2020)

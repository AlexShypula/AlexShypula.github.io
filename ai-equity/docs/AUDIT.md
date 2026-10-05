# Audit of v1 assumptions against data (2026-10-05)

This note records, for every row of the v1 model, what the research found, what v2 uses instead, and why. Research logs with URLs are in `docs/research/`. The generated methods note with full source text per row is `docs/METHODS_v2.md`.

## Headline result

| Share of all AI equity (%) | v1 heuristic | v2 researched | Why it moved |
|---|---|---|---|
| Top 0.1% | 19.8 | 19.4 | Founder blocks re-measured from 2026 proxies (Alphabet 12.4, Meta 13.5, Amazon 8.8, MSFT incl. Ballmer 4.5); Anthropic cofounders added; offset by a flatter employee row. |
| Next 0.9% | 14.4 | 14.8 | Little net change: more concentrated taxable row (DFA 2026 Q2) offset by less concentrated foreign funds/pension rows. |
| Next 9% | 27.5 | 32.2 | SCF 2022 shows the 90th–99th percentiles hold 52% of retirement-account assets (v1 had 45) and DFA puts them at 38.5% of DB entitlements (v1 had 28). |
| Next 40% | 20.1 | 19.5 | Roughly unchanged: the 50th–90th group gains in DB and foreign pensions but loses in taxable accounts. |
| Bottom 50% | 5.3 | 1.6 | The big correction. DFA: bottom half holds 2.6% of DB entitlements and 0.6% of equities; ONS: bottom five UK deciles hold <1% of pension wealth. v1 gave them 18% of US DB and 23% of foreign pensions. |
| Public / sovereign | 5.9 | 7.3 | Form PF and TIC: SWFs hold ~8% of hedge-fund NAV, ~11% of PE NAV, and $2.2T of US equities directly; the 13F residual is now half foreign. Pension/SWF direct holders bumped to ~5% of each megacap. |
| Nonprofits | 7.0 | 5.2 | Form PF puts nonprofits at 13.8% of hedge-fund NAV and 5.1% of PE NAV, below v1's 20% guesses; the offshore row sends 22% rather than 25% to nonprofits. |
| **Top 1%** | **34.2** | **34.2** | Essentially unchanged. |
| **Top 10%** | **61.7** | **66.3** | Up ~5 points, almost all from the retirement and DB rows. |
| Total value ($T) | 18.82 | 20.12 | Market caps refreshed to 2026-09-30. |

The robust finding: **about a third of AI equity value accrues to the top 1% of households in their own country and about two-thirds to the top 10%, in both the heuristic and the researched version.** What the data changed is the bottom of the distribution, where v1 was too generous by a factor of three, and the public/sovereign share, which is larger than v1 assumed.

## Validation against external anchors (public megacaps only, v2)

| Check | Model | Anchor | Verdict |
|---|---|---|---|
| Foreign share of megacap equity | 29.3% | TPC public-equity foreign 32–34% (YE2022); Z.1 ROW 18% direct + foreign-held fund shares; TIC $19.9T ≈ 18% of market | In range; megacaps near TPC, well above Z.1 direct because foreign money also sits inside US funds |
| US retirement share (401k/IRA + DB/insurance) | 33.5% | TPC public-equity retirement 34% | Matches |
| US taxable incl. founder blocks | 34.1% | TPC 28% | High, expected: these five firms carry $1.5T of founder stock that the market average does not |
| US nonprofits | 3.1% | TPC "other" 4–6% (incl. government, insurer separate accounts) | Plausible |
| Funds (index+active) share | 56% | Z.1 MF+ETF 25% of all equities; ICI index 19% + active 11% of US market | Model is higher because 13F managers also run separate accounts and CITs for pensions and foreign clients, which Z.1 books under those sectors. Expected direction; magnitude unverified |
| US-household distribution | top 1% 38.6%, top 10% 76% | DFA equities top 1% 50.9%, top 10% 88%; DFA pensions top 1% 9%, top 10% 50% | Model sits between the two, as it should: ~45% of US household exposure comes through retirement channels |
| Flow conservation, row sums | exact | — | Pass (`propagate.py`, `validate.py`) |
| v1 regression | within 0.05 pts | `v1_outputs_pct_of_total` | Pass |

## Layer 0: company values

| Company | v1 $B | v2 $B | Source / note |
|---|---|---|---|
| Nvidia | 5000 | 5560 | market cap 2026-09-30 |
| Alphabet | 4500 | 4300 | market cap 2026-09-30 |
| Microsoft | 3300 | 3850 | market cap 2026-09-30 |
| Amazon | 2700 | 2710 | market cap 2026-09-30 |
| Meta | 1500 | 1880 | market cap 2026-09-30 |
| Anthropic | 965 | 965 | last-round post-money confirmed |
| OpenAI | 852 | 852 | last-round post-money confirmed |

Both private valuations were verified: OpenAI $852B (Mar 31 2026 round, reconfirmed by the Aug 2026 employee tender) and Anthropic $965B (Series H, May 28 2026). Secondary markets price both higher (OpenAI ~$880–894B, Anthropic ~$1.0–1.2T) and OpenAI is reportedly raising at ~$1.4T, so the private rows are, if anything, conservative. xAI merged into SpaceX (now public at ~$2.3T) and is not modeled separately. Candidate additions the spec asked about: Broadcom $1.69T, TSMC $2.39T, Oracle ~$0.43T, Tesla $1.39T, SpaceX/xAI $2.28T (all 2026-09-30).

## Layer A: company → holder type

Research found two systematic problems with "percent institutional" figures: (1) Nasdaq and other aggregators still carry a stale Vanguard Group row alongside the new Vanguard Capital Management / Vanguard Portfolio Management rows after Vanguard's Jan 2026 restructuring, inflating 13F totals by ~9 points; (2) 13F "institutional" includes ~6–8 points of wirehouse and brokerage filers that are economically advised retail. v2 corrects both.

Order: Founders & insiders / Index / Active / Pensions-insurers-SWFs / Hedge funds / Retail & other direct / Big Tech strategic / VC & growth / Employee pools / Nonprofit parent.

| Company | v1 | v2 | Confidence | Key evidence |
|---|---|---|---|---|
| Nvidia | 4 / 22 / 25 / 9 / 5 / 35 / 0 / 0 / 0 / 0 | 4 / 29 / 27.1 / 5 / 3 / 31.9 / 0 / 0 / 0 / 0 | medium | Huang 3.58%, D&O 3.94% (DEF 14A Mar 2026); 13F 70.1% de-duplicated; index proxy 28% |
| Alphabet | 12 / 20 / 25 / 8 / 5 / 30 / 0 / 0 / 0 / 0 | 12.4 / 25 / 29.1 / 4.5 / 2 / 27 / 0 / 0 / 0 / 0 | medium | Page ~6.4% + Brin ~5.9% all classes (v1's 12 was right); 13F 66.6% of A+B+C |
| Microsoft | 5 / 24 / 28 / 10 / 4 / 29 / 0 / 0 / 0 / 0 | 4.5 / 30 / 31.7 / 5 / 2 / 26.8 / 0 / 0 / 0 / 0 | medium | D&O 0.03%; Ballmer ~4.5% (not an insider); Gates Foundation Trust sold out Q1 2026; 13F 74.7% |
| Amazon | 9 / 21 / 28 / 8 / 5 / 29 / 0 / 0 / 0 / 0 | 8.8 / 26 / 27.7 / 5 / 3 / 29.5 / 0 / 0 / 0 / 0 | medium | Bezos 8.2% economic (8.8% beneficial incl. Scott's voting proxy), Feb 2026; 13F 67.7% |
| Meta | 13 / 21 / 27 / 8 / 5 / 26 / 0 / 0 / 0 / 0 | 13.5 / 25 / 28.6 / 4.7 / 3 / 25.2 / 0 / 0 / 0 / 0 | medium | Zuckerberg 13.4% of A+B; 13F 67.3%; Capital Group overweight 3.9% |
| Anthropic | 0 / 0 / 0 / 0 / 0 / 0 / 25 / 45 / 30 / 0 | 8 / 0 / 0 / 0 / 0 / 0 / 36.6 / 40.4 / 15 / 0 | low | Amazon ~18 (10-Q fair value $190B → 19.7%), Google 14.5, Nvidia 2.4, MSFT 1.2, Salesforce 0.5; 7 cofounders ~8; employees ~15 (guess); VC/sovereign/crossover residual 40. v1 had strategic at 25 — too low given Amazon's filings |
| OpenAI | 0 / 0 / 0 / 0 / 0 / 0 / 33 / 23 / 18 / 26 | 0 / 0 / 0 / 0 / 0 / 0 / 33.5 / 23 / 19 / 24.5 | low-medium | Microsoft ~25 (FY26 10-K), Amazon 5, Nvidia 3.5; Foundation 26→24.5 after dilution; employees 19 (15.9 current + 3.5 former); SoftBank 12, Thrive 2, others 9. v1's 33/23/18/26 was already close |

Judgment calls in v2 beyond the research: pension/insurer/SWF direct holders raised from the agent's 3.5 to ~5 (NBIM alone is 1.3% of each; add SNB, CalPERS/CalSTRS, CPP, APG/PGGM, TSP); six points moved from Active to Retail for advised brokerage accounts; the remaining Active column is therefore ~27–32%.

## Layer B: holder type → beneficiary account

Order: Founder / Employee / US taxable / US 401k-IRA / US DB & insurance / Endowments & foundations / Foreign sovereign / Foreign pensions & insurers / Foreign funds & retail / Offshore / Foreign FO & HNW.

| Holder type | v1 | v2 | Confidence | What changed and why |
|---|---|---|---|---|
| Founders & insiders | 100 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | 100 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | high | Definitional, unchanged. |
| Index funds | 0 / 0 / 20 / 40 / 10 / 5 / 3 / 6 / 12 / 2 / 2 | 0 / 0 / 27 / 42 / 9 / 2 / 4 / 7 / 6 / 1 / 2 | medium-low | ICI 2026: 58% of long-term fund assets in DC+IRA (v1 had 40% to 401k/IRA + 20% taxable; v2 42 + 27 — more taxable because ETFs skew to taxable advisory accounts). Foreign ~20% from BlackRock's 32% non-Americas AUM and 5% official-institution share. |
| Active managers | 0 / 0 / 20 / 30 / 15 / 5 / 4 / 8 / 12 / 3 / 3 | 0 / 0 / 28 / 34 / 13 / 3 / 5 / 7 / 7 / 1 / 2 | low | Same base as index plus separate accounts for US DB plans and insurers (Z.1: MF shares 24% private pensions, 6.8% life insurers). Wirehouse filers removed to Retail. |
| Pensions, insurers & SWFs | 0 / 0 / 0 / 0 / 50 / 10 / 18 / 20 / 0 / 0 / 2 | 0 / 0 / 0 / 4 / 40 / 2 / 36 / 18 / 0 / 0 / 0 | low | Now dominated by NBIM, SNB and Canadian/Dutch funds among 13F filers, so foreign sovereign rises from 18 to 36 and US DB falls from 50 to 40. Endowments cut to 2 (they invest via managers, not direct 13Fs). |
| Hedge funds | 0 / 0 / 30 / 0 / 15 / 20 / 2 / 3 / 0 / 25 / 5 | 0 / 0 / 22 / 1 / 28 / 17 / 10 / 6 / 3 / 7 / 6 | medium-low | Replaced guesses with SEC Form PF 2025 Q3 beneficial owners: nonprofits 13.8, US individuals 11.7, public pensions 11.3, other pensions 9.0, SWF 7.8, insurers 3.6, non-US individuals 2.6; the 20% feeder slice re-spread pro rata. Offshore falls from 25 to 7 because the feeders are now resolved. |
| Retail & other direct | 0 / 0 / 45 / 15 / 0 / 0 / 8 / 8 / 10 / 7 / 7 | 0 / 0 / 36 / 10 / 1 / 4 / 8 / 4 / 20 / 9 / 8 | low | The 13F residual is now ~49% foreign (v1 30%): Irish and Luxembourg UCITS ($2.8T in TIC), Gulf/Asian official non-filers, Cayman SPVs and foreign retail do not file 13Fs, while 13F-filing managers already carry ~20% foreign money. Tuned so total megacap foreign ownership lands near 30% (TPC 32–34%). Loosest row in the model. |
| Big Tech strategic stakes | 0 / 0 / 22 / 28 / 10 / 5 / 5 / 8 / 12 / 5 / 5 | 7.7 / 0 / 26.3 / 24.6 / 9.2 / 3.1 / 6.8 / 6.1 / 9.4 / 3.3 / 3.5 | medium | Now DERIVED from the parents' own holder mixes weighted by stake dollars (Amazon 18%/5%, Google 14.5%, Microsoft 1.2%/25%, Nvidia 2.4%/3.5% of Anthropic/OpenAI). Resolves the spec's recursion question; founder equity (Bezos, Page/Brin, Ballmer) now flows into the labs (7.7% of this row). |
| VC & growth funds | 0 / 0 / 30 / 0 / 15 / 20 / 15 / 5 / 0 / 10 / 5 | 0 / 0 / 20 / 1 / 16 / 20 / 16 / 6 / 6 / 6 / 9 | low | Form PF PE owners (public pensions 16.4, SWF 10.9, nonprofits 5.1, individuals 5.5) tilted toward endowments and family offices per ECB/PitchBook (US VC LPs: foundations & endowments 25–35%). Foreign funds/retail set to 6 because SoftBank (a Japanese public company) is routed here; FO & HNW 9 includes Son. |
| Employee equity pools | 0 / 100 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | 0 / 100 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 / 0 | high | Definitional, unchanged. |
| Nonprofit parent | 0 / 0 / 0 / 0 / 0 / 100 / 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 / 100 / 0 / 0 / 0 / 0 / 0 | high | Definitional, unchanged. |

## Layer K: beneficiary account → wealth bucket

Order: Top 0.1% / Next 0.9% / Next 9% / Next 40% / Bottom 50% / Public / Nonprofits.

| Account | v1 | v2 | Confidence | What changed and why |
|---|---|---|---|---|
| Founder stakes | 100 / 0 / 0 / 0 / 0 / 0 / 0 | 100 / 0 / 0 / 0 / 0 / 0 / 0 | high | Definitional. 2026 top-0.1% threshold ≈ $75–95M. |
| Employee holdings | 45 / 40 / 13 / 2 / 0 / 0 / 0 | 45 / 35 / 18 / 2 / 0 / 0 / 0 | low | OpenAI tender data ($30M cap hit by ~75 people; avg stock comp $1.5M/yr) and Carta grant sizes: more mass in the 90–99th percentile than v1 assumed. |
| US taxable accounts | 24.2 / 26 / 37.2 / 11.6 / 1 / 0 / 0 | 25 / 27 / 38 / 9.5 / 0.5 / 0 / 0 | high | DFA updated to 2026 Q2 (25.0/25.9/37.2/11.4/0.6) and tilted because DFA's equity line includes IRAs, which the model routes separately; SCF 2022 taxable-only equity is 20.5/27.6/42.3/9.3/0.3 with the top understated. Bottom 50% was 1.0 in v1 from an older vintage. |
| US 401(k)s & IRAs | 5 / 12 / 45 / 33 / 5 / 0 / 0 | 2 / 11 / 50 / 34 / 3 / 0 / 0 | high | SCF 2022 microdata: 1.5/11.3/52.5/32.2/2.5; DFA DC pensions 1.3/10.1/44.1/39.7/4.8; JCT mega-IRA counts (~2–3% of IRA assets in IRAs >$5M). v1 was close but gave the top 0.1% too much. |
| US DB pensions & insurance | 2 / 5 / 28 / 47 / 18 / 0 / 0 | 1.5 / 5.5 / 39 / 51 / 3 / 0 / 0 | high | DFA 2026 Q2 DB entitlements 1.6/5.2/38.5/52.0/2.6. v1's 18% for the bottom half was the single largest error in the model. |
| Endowments & foundations | 0 / 0 / 0 / 0 / 0 / 0 / 100 | 0 / 0 / 0 / 0 / 0 / 0 / 100 | high | Definitional. |
| Foreign sovereign & official | 0 / 0 / 0 / 0 / 0 / 100 / 0 | 0 / 0 / 0 / 0 / 0 / 100 / 0 | high | Definitional. |
| Foreign pensions & insurers | 2 / 5 / 25 / 45 / 23 / 0 / 0 | 1.5 / 7.5 / 47 / 40 / 4 / 0 / 0 | medium-low | UK ONS: top wealth decile holds 64% of private pension wealth, bottom five deciles <1%. Even near-universal systems (NL, AU) concentrate balances in the top half. v1's 23% to the bottom half was unsupported. |
| Foreign funds & retail | 12 / 18 / 40 / 25 / 5 / 0 / 0 | 15 / 25 / 40 / 17 / 3 / 0 / 0 | medium | ECB distributional accounts: top 10% hold ~80% of euro-area equities and fund shares. WID 2024 top-1% wealth shares abroad (14–32%) are below the US 35%, so the row is flatter than US taxable but steeper than v1. |
| Offshore vehicles | 30 / 25 / 15 / 5 / 0 / 0 / 25 | 14.5 / 11 / 18.5 / 20.5 / 1.5 / 12 / 22 | low | Built from Form PF hedge-fund ownership: 22% nonprofits (US endowments via Cayman feeders), 12% SWF/official (new; v1 had 0), households 66% split top-heavy for individuals and DB-like for pensions. |
| Foreign family offices & HNW | 55 / 35 / 10 / 0 / 0 / 0 / 0 | 60 / 35 / 5 / 0 / 0 / 0 / 0 | medium | Family-office thresholds ($30M+) are top-1% everywhere; shifted 5 points from the 90–99th to the top 0.1%. |

## Benchmarks corrected

- **TIC June 2025**: v1 recorded $13.84T foreign portfolio US equity. The final survey (April 2026) reports **$19.86T** (common stock $15.2T + fund shares $3.3T + other equity $1.4T); official $2.23T. Country figures ($2.16T Cayman, $2.07T Canada, $2.06T UK) were right. Ireland ($1.47T) and Luxembourg ($1.36T) were missing and matter for the UCITS argument.
- **Fed DFA**: Q3 2025 → 2026 Q2 (files dated 2026-09-15). Equities 25.0/25.9/37.2/11.4/0.6. DFA pension entitlements added as a second benchmark (top 1% 9.1%, bottom 50% 3.7%).
- **TPC**: v1 cited Rosenthal & Burke 2020 (2019 data: foreign 40 / retirement 30 / taxable 25). Latest is Rosenthal & Mucciolo, Tax Notes 2024-04-01 (YE2022): total equity foreign 42 / retirement 27 / taxable 27; **publicly traded** equity retirement 34 / taxable 28 / foreign 32–34. No 2025–26 update exists.
- **Z.1**: table L.223 was renumbered F51.1.s in the Sept 2026 release; 2026 Q2 shares added to the config.
- **Added**: ICI 2026 (index funds 19% of US market, active 11%, 58% of long-term fund assets in DC+IRA), SEC Form PF 2025 Q3 beneficial owners, WID 2024 within-country top-1% shares, SCF 2022 tabulations.

## Data gaps that remain (in order of leverage on the headline)

1. **The 13F residual's foreign share** (Retail & other direct row). No source splits the non-13F ~28% of each megacap between US households and non-filing foreign holders. Milestone 2 of the spec (actual 13F ingestion with a filer-classification file) would pin the residual; TIC-by-country vs 13F-by-filer-domicile would bound its foreign share.
2. **Anthropic's cap table.** Everything other than Amazon's and Google's stakes is inferred. Replace from the S-1 (IPO expected Oct–Nov 2026).
3. **Who owns index funds.** ICI and Z.1 give the mutual-fund side; nobody publishes an ETF holder split or Vanguard's client mix. BlackRock's 10-K is the best public proxy.
4. **Cayman round-tripping.** No published estimate of the US-owned share of Cayman's $2.16T of US equity. Beck et al. (2024) cover Luxembourg and Ireland only (44% and 66% owned outside the euro area, mostly UK, not US).
5. **Larry Page's Class C** (no Form 4 since 2022), **Ballmer** and **Gates** personal holdings. Alphabet's insider row could be up to 3 points high.
6. **Hedge-fund share per ticker.** Goldman's Trend Monitor has it but is paywalled; ~2–3% is an informed guess.
7. **2025 SCF** (due late 2026) will refresh the retirement-account rows; the 2026 Q3 DFA arrives ~Dec 2026.

## Process notes

- Research was done by four parallel agents, one per layer; their reports are in `docs/research/`. Numbers marked "own tabulation" were computed by an agent from the Fed's public SCF 2022 extract and the WID bulk file.
- One agent reported that a single request to sec.gov for a public PDF carried the user's email address in the HTTP User-Agent header (EDGAR's fair-access policy asks for a contact address). No other request did.
- The Forbes OpenAI cap-table article returned 403; its figures were taken from sites that reproduce it and cross-checked against Microsoft's 10-K, which they partly contradict (the leak looks undiluted by the $122B round).


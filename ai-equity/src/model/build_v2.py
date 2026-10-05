#!/usr/bin/env python3
"""Assemble config/assumptions_v2.json from researched priors (docs/research/*).

Everything numeric lives in this file so the provenance of each row is explicit.
The 'Big Tech strategic stakes' look-through row is DERIVED: a dollar-weighted
blend of the parent companies' own holder mixes pushed through layer B, so Bezos's
8% of Amazon shows up as founder equity in Anthropic, etc.
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
v1 = json.load(open(os.path.join(ROOT, "config", "assumptions_v1.json")))

H = v1["holder_types"]; B = v1["beneficiary_accounts"]; K = v1["wealth_buckets"]
def row(names, vals): 
    assert len(names) == len(vals), (names, vals)
    s = sum(vals); assert abs(s - 100) < 0.051, (names[0], s)
    return dict(zip(names, vals))

# ---------------------------------------------------------------- Layer 0 + A
# Holder order: Founders & insiders, Index, Active, Pensions/insurers/SWFs, Hedge funds,
#               Retail & other direct, Big Tech strategic, VC & growth, Employee pools, Nonprofit parent
companies = [
 # public: insiders from DEF 14A; index/active/pension/HF split of de-duplicated 13F totals (Nasdaq 6/30/2026,
 # stale Vanguard Group row removed); ~6 pts of wirehouse/brokerage 13F filers moved from Active to Retail
 # (advised retail accounts); pension/SWF direct bumped to ~5 (NBIM 1.3, SNB 0.3, CalPERS/CalSTRS, Canadian & Dutch funds).
 dict(id="nvda", name="Nvidia",    value_busd=5560, color="#4F7A28", mix=[4.0, 29.0, 27.1, 5.0, 3.0, 31.9, 0, 0, 0, 0]),
 dict(id="googl", name="Alphabet", value_busd=4300, color="#C4842A", mix=[12.4, 25.0, 29.1, 4.5, 2.0, 27.0, 0, 0, 0, 0]),
 dict(id="msft", name="Microsoft", value_busd=3850, color="#2F6FA8", mix=[4.5, 30.0, 31.7, 5.0, 2.0, 26.8, 0, 0, 0, 0]),
 dict(id="amzn", name="Amazon",    value_busd=2710, color="#8A5A9E", mix=[8.8, 26.0, 27.7, 5.0, 3.0, 29.5, 0, 0, 0, 0]),
 dict(id="meta", name="Meta",      value_busd=1880, color="#2D8C8C", mix=[13.5, 25.0, 28.6, 4.7, 3.0, 25.2, 0, 0, 0, 0]),
 # Anthropic: Amazon ~18 (10-Q fair value $190B / $965B = 19.7%, press "mid-to-high teens"), Google 14.5 (14%, cap 15%),
 # Nvidia ~2.4, Microsoft ~1.2, Salesforce ~0.5 -> 36.6 strategic; 7 cofounders ~8; employee pool ~15 (Carta late-stage median);
 # VC/growth/sovereign/crossover residual 40.4.
 dict(id="anthropic", name="Anthropic", value_busd=965, color="#A34E6B", mix=[8.0, 0, 0, 0, 0, 0, 36.6, 40.4, 15.0, 0]),
 # OpenAI: Microsoft ~25 (FY26 10-K), Amazon ~5, Nvidia ~3.5 -> 33.5 strategic; Foundation ~24.5 (26% at recap, diluted by $122B round);
 # employees current+former ~19 (Forbes reconstruction 15.9+3.5); SoftBank ~12, Thrive ~2, a16z/MGX/Khosla/others ~9 -> 23 VC/growth.
 dict(id="openai", name="OpenAI",   value_busd=852, color="#5E6672", mix=[0, 0, 0, 0, 0, 0, 33.5, 23.0, 19.0, 24.5]),
]
# strategic stakes: (lab, parent, % of lab) used to weight the derived Big Tech row
strategic = [("anthropic","amzn",18.0),("anthropic","googl",14.5),("anthropic","nvda",2.4),("anthropic","msft",1.2),
             ("openai","msft",25.0),("openai","amzn",5.0),("openai","nvda",3.5)]

# ---------------------------------------------------------------- Layer B
# Beneficiary order: Founder stakes, Employee holdings, US taxable, US 401k/IRA, US DB & insurance, Endowments & foundations,
#                    Foreign sovereign, Foreign pensions & insurers, Foreign funds & retail, Offshore vehicles, Foreign FO & HNW
hb = {
 "Founders & insiders":        [100, 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
 "Index funds":                [0, 0, 27, 42,  9,  2,  4,  7,  6,  1,  2],
 "Active managers":            [0, 0, 28, 34, 13,  3,  5,  7,  7,  1,  2],
 "Pensions, insurers & SWFs":  [0, 0,  0,  4, 40,  2, 36, 18,  0,  0,  0],
 "Hedge funds":                [0, 0, 22,  1, 28, 17, 10,  6,  3,  7,  6],
 "Retail & other direct":      [0, 0, 36, 10,  1,  4,  8,  4, 20,  9,  8],
 "Big Tech strategic stakes":  None,  # derived below
 "VC & growth funds":          [0, 0, 20,  1, 16, 20, 16,  6,  6,  6,  9],
 "Employee equity pools":      [0, 100, 0,  0,  0,  0,  0,  0,  0,  0,  0],
 "Nonprofit parent":           [0, 0,  0,  0,  0, 100, 0,  0,  0,  0,  0],
}
# derive Big Tech row: sum over (lab, parent) of $-weight * (parent mix . hb)
byid = {c["id"]: c for c in companies}
acc = [0.0]*len(B); wsum = 0.0
for lab, parent, pctlab in strategic:
    w = byid[lab]["value_busd"] * pctlab/100; wsum += w
    mix = byid[parent]["mix"]
    for h, name in enumerate(H):
        if mix[h] == 0 or hb[name] is None: continue
        for b in range(len(B)): acc[b] += w * mix[h]/100 * hb[name][b]/100
acc = [100*x/wsum for x in acc]
# round to 1 dp, fix the rounding residual on the largest cell
r = [round(x,1) for x in acc]; r[r.index(max(r))] += round(100-sum(r),1)
hb["Big Tech strategic stakes"] = r
print("derived Big Tech strategic row:", dict(zip(B, r)))

# ---------------------------------------------------------------- Layer K
# Bucket order: Top 0.1, Next 0.9, Next 9, Next 40, Bottom 50, Public/sovereign, Nonprofits
bk = {
 "Founder stakes":               [100, 0, 0, 0, 0, 0, 0],
 "Employee holdings":            [45, 35, 18, 2, 0, 0, 0],
 "US taxable accounts":          [25, 27, 38, 9.5, 0.5, 0, 0],
 "US 401(k)s & IRAs":            [2, 11, 50, 34, 3, 0, 0],
 "US DB pensions & insurance":   [1.5, 5.5, 39, 51, 3, 0, 0],
 "Endowments & foundations":     [0, 0, 0, 0, 0, 0, 100],
 "Foreign sovereign & official": [0, 0, 0, 0, 0, 100, 0],
 "Foreign pensions & insurers":  [1.5, 7.5, 47, 40, 4, 0, 0],
 "Foreign funds & retail":       [15, 25, 40, 17, 3, 0, 0],
 "Offshore vehicles":            [14.5, 11, 18.5, 20.5, 1.5, 12, 22],
 "Foreign family offices & HNW": [60, 35, 5, 0, 0, 0, 0],
}

# ---------------------------------------------------------------- sources & confidence per row
S = {"companies": {}, "holder_to_beneficiary": {}, "beneficiary_to_bucket": {}}
def src(layer, key, source, confidence, note=""): S[layer][key] = dict(source=source, confidence=confidence, note=note)
pub = "Market cap 2026-09-30 (tradingkey/companiesmarketcap). Insiders: DEF 14A 2026. Institutional split: Nasdaq 13F 6/30/2026 de-duplicated for the Vanguard Group→VCM/VPM restructuring; index proxy from top-40 filers weighted by manager passive share; BlackRock 93% index (Q2-26 release)."
src("companies","nvda", pub+" Huang 3.58%, D&O 3.94%.", "medium", "13F total 70.1%. Hedge-fund share is a guess (GS Trend Monitor: ~3% avg for S&P 500 names).")
src("companies","googl", pub+" Page ~6.4% + Brin ~5.9% across A/B/C (Page's Class C not updated since 2022).", "medium", "13F 66.6% of all classes. Insider figure may be up to ~3 pts high if Page sold Class C.")
src("companies","msft", pub+" Ballmer ~4.5% from old filings (not a proxy insider); D&O 0.03%; Gates Foundation Trust sold out Q1 2026.", "medium", "13F 74.7%.")
src("companies","amzn", pub+" Bezos 8.2% economic (8.8% beneficial incl. 0.6% MacKenzie Scott voting proxy), Feb 2026; selling under 10b5-1.", "medium", "13F 67.7%.")
src("companies","meta", pub+" Zuckerberg 13.4% of A+B (99.8% of Class B), Apr 2026.", "medium", "13F 67.3% of A+B.")
src("companies","anthropic", "Series H $965B post (anthropic.com/news/series-h, 2026-05-28). Amazon fair value $190.4B in Q2-26 10-Q → ~19.7%, press 'mid-to-high teens' → 18. Google 14% (court filings), capped 15%. Nvidia ≤$10B, Microsoft ≤$5B (Nov 2025). Cofounders ~6–11% (Bloomberg/Forbes 400). Employee pool ~15 is a Carta-based guess.", "low", "No public cap table until the S-1. LTBT holds Class T with no economics.")
src("companies","openai", "$852B post ($122B round 2026-03-31). Microsoft ~25% as-converted (FY26 10-K). Foundation 26% at Oct-2025 recap, ~24.5 after dilution. Forbes reconstruction (2026-04-02): SoftBank 11.7, Amazon 4.7, Nvidia 3.5, employees 15.9 + former 3.5, Thrive 2.0.", "low-medium", "Leaked table is a reconstruction; Microsoft and Foundation figures cross-checked against 10-K.")
src("holder_to_beneficiary","Founders & insiders", "Definitional.", "high")
src("holder_to_beneficiary","Index funds", "ICI 2026 Fact Book: 58% of long-term MF assets in DC+IRA; households own 87% of MF assets. BlackRock 10-K YE2025: 32% non-Americas AUM, official institutions 5% of institutional, 62% of institutional AUM is pensions. ETFs skew taxable; ETF holder split unpublished.", "medium-low", "Foreign ≈ 20%. Vanguard client/region mix unverified.")
src("holder_to_beneficiary","Active managers", "Same MF base as index (Fidelity, Capital Group in DC plans) plus separate accounts for US DB plans, insurers, SWF and UCITS mandates. Z.1 F522.1: MF shares held 57% households (incl. IRAs), 24% private pensions, 7.6% ROW, 6.8% life insurers.", "low", "Wirehouse/brokerage 13F filers moved to 'Retail & other direct' in layer A.")
src("holder_to_beneficiary","Pensions, insurers & SWFs", "Direct 13F-filing asset owners: NBIM ~1.3% of each megacap (13F 6/30/2026), SNB ~0.3%, CalPERS/CalSTRS, CPP/APG/PGGM, TSP. TIC official $2.23T. Z.1 Q2-26: state&local pensions $4.1T, private $5.3T, insurers $1.5T direct.", "low", "Index mandates run by BlackRock/SSGA for pensions sit in 'Index funds'.")
src("holder_to_beneficiary","Hedge funds", "SEC Form PF 2025 Q3 beneficial owners of qualifying hedge funds: non-profits 13.8, US individuals 11.7, state/municipal pensions 11.3, other pensions 9.0, SWF 7.8, insurers 3.6, non-US individuals 2.6, other private funds 20.4 (re-spread pro rata), other 15.3 (split US taxable / offshore).", "medium-low", "53.6% of HF NAV is Cayman-domiciled; Form PF resolves most of it to beneficiaries, so the Offshore column is only the unresolved residual.")
src("holder_to_beneficiary","Retail & other direct", "13F residual (~25–32% of shares). Contains US household direct holdings (Z.1 households 42% of equities) and non-13F foreign holders: Irish/Lux UCITS ($1.47T + $1.36T TIC), foreign official non-filers (ADIA, SAFE, KIA), Cayman SPVs ($2.16T), foreign retail. Foreign share set so total megacap foreign ownership lands ~30% (TPC public-equity foreign 32–34%, Z.1 ROW 18% direct + fund shares).", "low", "The loosest row in the model. v1 had 30% foreign here; v2 has 49% because 13F-filing managers already carry ~20% foreign.")
src("holder_to_beneficiary","Big Tech strategic stakes", "DERIVED: dollar-weighted blend of parents' holder mixes (Amazon 18%/5%, Google 14.5%, Microsoft 1.2%/25%, Nvidia 2.4%/3.5% of Anthropic/OpenAI) pushed through this matrix. So Bezos/Page/Brin/Ballmer founder equity flows into the labs.", "medium", "Resolves the spec's recursion question without a loop in the Sankey.")
src("holder_to_beneficiary","VC & growth funds", "Form PF 2025 Q3 PE owners (state/municipal pensions 16.4, SWF 10.9, non-profits 5.1, US individuals 5.5, insurers 5.5) tilted toward endowments/foundations and family offices (ECB/PitchBook May 2026: US VC LPs dominated by pensions, foundations & endowments 25–35%). Lab investor lists: SoftBank (JP public co.), MGX (UAE), GIC (SG), Altimeter/Dragoneer/Thrive/Sequoia (US).", "low", "SoftBank's ~12% of OpenAI is routed here; its Japanese shareholder base is why 'Foreign funds & retail' and 'Foreign FO & HNW' (Son) are non-zero.")
src("holder_to_beneficiary","Employee equity pools", "Definitional.", "high")
src("holder_to_beneficiary","Nonprofit parent", "Definitional (OpenAI Foundation).", "high")
src("beneficiary_to_bucket","Founder stakes", "Definitional: every named founder is far above the US top-0.1% threshold (~$75–95M in 2026).", "high", "Charitable pledges and CZI/Bezos Earth Fund transfers not modeled.")
src("beneficiary_to_bucket","Employee holdings", "OpenAI avg stock comp ~$1.5M/yr (WSJ); Oct-2025 tender: 600+ staff sold $6.6B with $30M cap, ~75 hit cap. Carta: C-level 0.8–1.5%, VPs 0.3–0.8% of FD equity. ≥$75M vested → US top 0.1%; 2+ yr tenure plausibly ≥$15M → top 1%.", "low", "Within-US percentiles; many staff are not US-resident.")
src("beneficiary_to_bucket","US taxable accounts", "Fed DFA 2026 Q2 corporate equities & MF shares: 25.0/25.9/37.2/11.4/0.6 — but that line includes IRA-held equity. SCF 2022 taxable stocks+stock funds: 20.5/27.6/42.3/9.3/0.3 (top understated, no Forbes 400). Blend, tilted to DFA at the top.", "high", "v1 used an older DFA vintage with bottom 50% = 1.0; current data says 0.6.")
src("beneficiary_to_bucket","US 401(k)s & IRAs", "SCF 2022 retirement accounts (IRA+DC) by wealth percentile: 1.5/11.3/52.5/32.2/2.5. DFA 2026 Q2 DC pensions: 1.3/10.1/44.1/39.7/4.8. JCT mega-IRA counts (28,600 IRAs >$5M in 2019 ≈ 2–3% of IRA assets) support ~2% at the top.", "high", "v1 row 5/12/45/33/5 was close; top 0.1% was too high.")
src("beneficiary_to_bucket","US DB pensions & insurance", "Fed DFA 2026 Q2 DB pension entitlements: 1.6/5.2/38.5/52.0/2.6. Insurer general accounts assumed to follow DB.", "high", "v1 row 2/5/28/47/18 gave the bottom 50% far too much; DFA says 2.6%.")
src("beneficiary_to_bucket","Endowments & foundations", "Definitional. NACUBO FY25 $944B endowments (86% equity-like); foundations $1.64T.", "high")
src("beneficiary_to_bucket","Foreign sovereign & official", "Definitional. TIC June 2025 official holdings $2.23T.", "high")
src("beneficiary_to_bucket","Foreign pensions & insurers", "UK ONS: top wealth decile holds 64% of private pension wealth, bottom five deciles <1% (2018–20). Dutch (~90% occupational coverage), Australian (super ~universal), Canadian (CPP universal, RPP 38%) systems are broader. Within-country percentiles.", "medium-low", "v1 row 2/5/25/45/23 was far too flat at the bottom.")
src("beneficiary_to_bucket","Foreign funds & retail", "ECB Distributional Wealth Accounts: top 10% hold ~80% of euro-area equities & fund shares (EB 5/2024). WID 2024 top-1% wealth shares: UK 21, CA 29, JP 25, DE 28, FR 28, CH 32 (US 35). Within-country percentiles.", "medium", "v1 row 12/18/40/25/5 slightly under-weighted the top 1%.")
src("beneficiary_to_bucket","Offshore vehicles", "Prior for unresolved Cayman/BVI/Bermuda holders built from Form PF HF ownership: ~22% non-profits (US endowments via feeders), ~12% SWF/official, remainder households split 22/17/28/31/2 (individuals top-heavy, pensions DB-like). Round-trip share of Cayman US-equity holdings unpublished; literature (Beck et al. 2024) covers Lux/Ireland only.", "low", "v1 sent 25% to nonprofits and 0% to public; v2 22% and 12%.")
src("beneficiary_to_bucket","Foreign family offices & HNW", "Family-office / HNW thresholds ($30M+) sit in the top 1% in every WID country; top 0.1% shares of wealth 7–16% abroad.", "medium", "v1 55/35/10; v2 60/35/5.")

# ---------------------------------------------------------------- assemble
out = {
 "_meta": {
  "version": "v2-researched",
  "created": "2026-10-05",
  "as_of": "2026-09-30 (market caps); 2026-06-30 (13F, Z.1, DFA); June 2025 (TIC)",
  "note": "All shares are percentages; each row is normalized to 100 at compute time. Values in $B.",
  "description": "v2 researched set (Oct 5 2026). Market caps at 2026-09-30; insider stakes from 2026 proxies; 13F totals de-duplicated for Vanguard's Jan-2026 restructuring; layer-K rows from Fed DFA 2026 Q2 and SCF 2022 microdata; layer-B rows from Z.1, ICI 2026, TIC June 2025 and SEC Form PF. Hover a confidence tag for the row's source.",
  "layers": v1["_meta"]["layers"],
  "bucket_definition": v1["_meta"]["bucket_definition"],
  "confidence": {
   "company_values": "high for public caps (2026-09-30); high for last-round post-money of OpenAI ($852B, Mar 2026) and Anthropic ($965B, May 2026), though secondaries trade 5–25% higher",
   "public_holder_mix": "medium: insiders from proxies (high), 13F totals (medium-high after de-duplication), index/active split from manager passive shares (medium), hedge-fund share guessed (low)",
   "private_holder_mix": "low-medium for OpenAI (10-K cross-checks), low for Anthropic (no cap table until S-1)",
   "holder_to_beneficiary": "medium-low: anchored to ICI, Z.1, Form PF and TIC, but no source looks through index-fund or 13F-residual ownership directly",
   "beneficiary_to_bucket": "high for the three US rows (DFA 2026 Q2 + SCF 2022); medium for foreign rows (WID/ONS/ECB); low for offshore and employee rows"
  },
  "layer_notes": {
   "company": "Values in $B at 2026-09-30. Public firms: insiders from 2026 proxies (Huang 3.6%, Page+Brin ~12%, Ballmer ~4.5%, Bezos 8.2%, Zuckerberg 13.4%); 13F totals of 67–75% after removing Nasdaq's stale Vanguard Group row; index managers ≈ 25–30% of each; about six points of wirehouse/brokerage filers are counted as advised retail. Private labs: OpenAI from the Oct-2025 recap, Microsoft's FY26 10-K and a reconstructed cap table; Anthropic from Amazon's and Alphabet's 10-Qs and press. Anthropic's split is the least certain row until its S-1 is public.",
   "holder_to_beneficiary": "Look-through from intermediaries to the accounts behind them. Index and active funds: 58% of long-term fund assets sit in 401(k)s and IRAs (ICI 2026), about a fifth is foreign-owned. Hedge funds and VC use SEC Form PF beneficial-owner shares, so Cayman feeders are resolved to endowments, pensions and individuals and 'Offshore vehicles' is only the unresolved residual. The 13F residual ('Retail & other direct') is about half foreign because Irish and Luxembourg UCITS, Gulf and Asian official holders and Cayman SPVs do not file 13Fs. Big Tech strategic stakes are derived from the parents' own holder mixes, so founder equity flows into the labs.",
   "beneficiary_to_bucket": "US taxable accounts: Fed DFA 2026 Q2 equity distribution, tilted for the fact that DFA's equity line includes IRAs. US 401(k)/IRA and DB rows: SCF 2022 microdata and DFA pension entitlements. Employee equity at these valuations lands mostly in the top 1% by construction. Foreign rows are within-country percentiles from WID 2024, UK ONS and ECB distributional accounts; foreign pension wealth is very top-heavy in the UK (top decile 64%) even where coverage is near-universal. Offshore vehicles send 22% to nonprofits and 12% to sovereign funds following Form PF."
  },
  "method": [
   "Each dollar of company value is split by holder type, then by the beneficiary accounts behind each holder type, then by the wealth percentile of the households holding those accounts. Flows keep the color of the company they started in, so you can see how each firm's value disperses.",
   "Anchors: Fed Distributional Financial Accounts 2026 Q2 (top 1% hold 50.9% of household corporate equities and mutual funds; 90th–99th 37.2%; 50th–90th 11.4%; bottom half 0.6%). SCF 2022 microdata for retirement accounts (top 1% hold 12.8%, 90th–99th 52.5%, bottom half 2.5%). Fed Z.1 2026 Q2: rest of world holds 18% of US corporate equities directly; mutual funds and ETFs 25%; pension funds 8%. ICI 2026: index funds hold 19% of US market value, active funds 11%.",
   "Foreign split: the final June 2025 TIC survey puts foreign holdings of US equities at $19.9T (about 18% of the market), $2.2T of it official, with the Cayman Islands, Canada and the UK each near $2.1T and Ireland and Luxembourg at $1.4T each. The Tax Policy Center (Rosenthal & Mucciolo 2024) puts foreign ownership of publicly traded US equity at 32–34%; this model lands near 30% for the megacaps. Cayman, Irish and Luxembourg figures reflect fund domicile, not the nationality of the final owner.",
   "Private labs: OpenAI's post-recapitalization structure is well documented (Microsoft ~25%, OpenAI Foundation ~25%, employees ~19%, SoftBank ~12%). Anthropic's is not: Amazon's ~18–20% and Google's ~14–15% come from their own filings; the cofounder, employee and VC split is inferred and should be replaced from the S-1.",
   "Not modeled: dual-class voting control (economic shares only), liquidation preferences on private stock, founder charitable pledges, the gap between last-round and secondary-market valuations, cross-holdings beyond the derived strategic-stake row, and the difference between wealth and income percentiles. Confidence tags on each row say how much to trust it; treat outputs as ranges, not estimates."
  ]
 },
 "holder_types": H, "beneficiary_accounts": B, "beneficiary_is_us": v1["beneficiary_is_us"],
 "wealth_buckets": K, "wealth_bucket_labels": v1["wealth_bucket_labels"],
 "companies": [dict(id=c["id"], name=c["name"], value_busd=c["value_busd"], color=c["color"], holder_mix=row(H, c["mix"])) for c in companies],
 "strategic_stakes": [dict(lab=l, parent=p, pct_of_lab=x) for l, p, x in strategic],
 "holder_to_beneficiary": {h: row(B, hb[h]) for h in H},
 "beneficiary_to_bucket": {b: row(K, bk[b]) for b in B},
 "sources": S,
 "benchmarks": {
  "fed_dfa_2026q2_corporate_equities_mutual_funds": {"Top 0.1%": 25.0, "Next 0.9%": 25.9, "Next 9%": 37.2, "Next 40%": 11.4, "Bottom 50%": 0.6,
    "_label": "Fed DFA: all US household-held equity (2026 Q2)",
    "_note": "The benchmark is the Fed's Distributional Financial Accounts share of corporate equities and mutual fund shares, 2026 Q2 ($64.6T). It includes IRA-held equity but excludes DB/DC pension entitlements, so it sits between the model's 'US taxable' and '401(k)/IRA' channels. The model's US-household bar is flatter because DB plans and 401(k)s are spread far more evenly (top 1% hold ~9% of pension entitlements vs 51% of equities).",
    "_source": "federalreserve.gov/releases/z1/dataviz/dfa (files dated 2026-09-15)"},
  "fed_dfa_2026q2_pension_entitlements_db_dc": {"Top 0.1%": 1.5, "Next 0.9%": 7.6, "Next 9%": 41.2, "Next 40%": 46.1, "Bottom 50%": 3.7, "_total_busd": 35700},
  "fed_dfa_2026q2_net_worth": {"Top 0.1%": 15.0, "Next 0.9%": 17.5, "Next 9%": 36.4, "Next 40%": 28.8, "Bottom 50%": 2.3, "_total_busd": 185650},
  "scf_2022_retirement_accounts": {"Top 0.1%": 1.5, "Next 0.9%": 11.3, "Next 9%": 52.5, "Next 40%": 32.2, "Bottom 50%": 2.5, "_source": "Own tabulation of SCF 2022 public summary extract, weighted, 5 implicates pooled"},
  "scf_2022_taxable_stocks_and_stock_funds": {"Top 0.1%": 20.5, "Next 0.9%": 27.6, "Next 9%": 42.3, "Next 40%": 9.3, "Bottom 50%": 0.3},
  "tic_june_2025_final": {"foreign_us_equity_busd": 19860, "foreign_official_us_equity_busd": 2230, "cayman_busd": 2160, "canada_busd": 2065, "uk_busd": 2057, "ireland_busd": 1469, "luxembourg_busd": 1357, "japan_busd": 1169, "common_stock_busd": 15211, "fund_shares_busd": 3266, "other_equity_busd": 1382,
    "_source": "Treasury SHL June 30 2025 final (shl2025r.pdf, April 2026); fund domicile, not ultimate owner"},
  "tpc_2024_rosenthal_mucciolo_ye2022": {"total_equity_foreign": 42, "total_equity_retirement": 27, "total_equity_taxable": 27, "public_equity_retirement": 34, "public_equity_taxable": 28, "public_equity_foreign": "32–34",
    "_source": "Rosenthal & Mucciolo, 'Who's Left to Tax?', Tax Notes Federal, 2024-04-01; no later update found"},
  "fed_z1_2026q2_corporate_equities_holders_pct": {"households_and_nonprofits": 42.1, "rest_of_world": 18.0, "mutual_funds": 15.1, "etfs": 10.3, "private_pensions": 4.3, "state_local_pensions": 3.3, "federal_pensions": 0.6, "nonfinancial_corporations": 3.1, "life_insurers": 0.7, "pc_insurers": 0.6, "hedge_funds_us_domiciled": 0.7,
    "_source": "Z.1 release 2026-09-11, table F51.1.s (formerly L.223); total $123.7T incl. $14.4T foreign equities held by US residents"},
  "ici_2026_factbook": {"index_domestic_equity_funds_share_of_us_market": 19, "active_domestic_equity_funds_share_of_us_market": 11, "long_term_mf_assets_in_dc_and_ira_pct": 58, "mf_assets_held_by_households_pct": 87, "us_retirement_assets_2026q2_busd": 51200},
  "sec_form_pf_2025q3_hedge_fund_owners_pct": {"other_private_funds": 20.4, "other": 15.3, "nonprofits": 13.8, "us_individuals": 11.7, "state_municipal_pensions": 11.3, "other_pensions": 9.0, "swf_foreign_official": 7.8, "insurers": 3.6, "non_us_individuals": 2.6, "cayman_domiciled_nav_pct": 53.6},
  "wid_2024_top1_wealth_share": {"US": 34.8, "UK": 21.3, "Canada": 28.6, "Japan": 24.6, "Norway": 23.5, "Netherlands": 14.0, "Switzerland": 31.5, "Germany": 27.8, "France": 27.7, "Australia": 23.7, "China": 30.4, "Singapore": 28.4, "Saudi Arabia": 30.1, "UAE": 28.1, "_source": "WID bulk file 2026-09-09, shwealj992, year 2024"}
 },
 "v1_outputs_pct_of_total": v1["v1_outputs_pct_of_total"]
}
path = os.path.join(ROOT, "config", "assumptions_v2.json")
json.dump(out, open(path, "w"), indent=2, ensure_ascii=False)
print("wrote", path)

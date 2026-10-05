#!/usr/bin/env python3
"""Spec validation checks for an assumption set: row sums, flow conservation,
aggregate holder shares vs Z.1, foreign share vs TIC/TPC, US channel split vs TPC."""
import json, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from propagate import propagate, matrices

a = json.load(open(sys.argv[1]))
H, B, K, A, Bm, Km = matrices(a)
us = a["beneficiary_is_us"]
pub_ids = [c["id"] for c in a["companies"] if c["holder_mix"].get("Big Tech strategic stakes", 0) == 0 and c["holder_mix"].get("Employee equity pools", 0) == 0]
out_all = propagate(a); out_pub = propagate(a, include=set(pub_ids))

def layer_totals(out, prefix):
    t = {}
    for l in out["links"]:
        if l["target"].startswith(prefix): t[l["target"][2:]] = t.get(l["target"][2:], 0) + l["value"]
    return t

print(f"== {a['_meta']['version']} ==")
T = out_all["total_busd"]
for p, name in (("H:", "holder"), ("B:", "beneficiary"), ("K:", "bucket")):
    s = sum(layer_totals(out_all, p).values())
    print(f"flow conservation at {name:12s}: {s:9.1f} vs total {T:9.1f}  {'OK' if abs(s-T) < 1e-6*T else 'FAIL'}")

print("\n-- public megacaps only:", ", ".join(pub_ids))
Tp = out_pub["total_busd"]
h = layer_totals(out_pub, "H:")
print("holder shares (%):", {k: round(100*v/Tp, 1) for k, v in h.items() if v > 0})
z1 = a["benchmarks"].get("fed_z1_2026q2_corporate_equities_holders_pct", {})
if z1:
    funds = 100*(h.get("Index funds", 0)+h.get("Active managers", 0))/Tp
    print(f"  funds (index+active) {funds:.1f}% vs Z.1 MF+ETF {z1['mutual_funds']+z1['etfs']:.1f}% of all US equities "
          "(13F managers also run separate accounts/CITs for pensions and foreigners, so model > Z.1 is expected)")
    print(f"  hedge funds {100*h.get('Hedge funds',0)/Tp:.1f}% vs Z.1 US-domiciled HF {z1['hedge_funds_us_domiciled']:.1f}% (+ ~1% offshore)")
b = layer_totals(out_pub, "B:")
foreign = sum(v for i, (k, v) in enumerate(b.items()) if not us[B.index(k)])
ret = b.get("US 401(k)s & IRAs", 0) + b.get("US DB pensions & insurance", 0)
tax = b.get("US taxable accounts", 0)
nonhh = b.get("Endowments & foundations", 0)
founders = b.get("Founder stakes", 0)
print("beneficiary shares (%):", {k: round(100*v/Tp, 1) for k, v in b.items() if v > 0})
print(f"  foreign {100*foreign/Tp:.1f}%   | TPC public-equity foreign 32–34% (YE2022); Z.1 ROW direct 18% + foreign-held fund shares; TIC $19.9T ≈ 18% of market")
print(f"  US retirement (401k/IRA + DB/ins) {100*ret/Tp:.1f}% | TPC public-equity retirement 34%")
print(f"  US taxable {100*tax/Tp:.1f}% (+ founders {100*founders/Tp:.1f}% which TPC also counts as taxable → {100*(tax+founders)/Tp:.1f}%) | TPC 28%")
print(f"  US nonprofits {100*nonhh/Tp:.1f}% | TPC 'other' ~4–6% incl. government and insurer separate accounts")

print("\n-- all companies: bucket shares (%)")
for scope in ("all", "us", "foreign"):
    p = out_all["buckets_pct_of_total"][scope]
    print(f"  {scope:8s}", {k: p[k] for k in K})
dfa = next((v for k, v in a["benchmarks"].items() if k.startswith("fed_dfa") and "equities" in k), None)
if dfa:
    bus = out_all["buckets_busd"]["us"]; hh = sum(bus[k] for k in K[:5])
    model = [round(100*bus[k]/hh, 1) for k in K[:5]]; bench = [dfa[k] for k in K[:5]]
    print(f"  US households, model {model} vs DFA equities {bench}: model top-1% {model[0]+model[1]:.1f} vs DFA {bench[0]+bench[1]:.1f}; "
          f"model should be flatter because retirement channels are flatter")

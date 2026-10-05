#!/usr/bin/env python3
"""Generate a methods note (markdown) from an assumption set: every row, its values, source and confidence."""
import json, sys
a = json.load(open(sys.argv[1])); m = a["_meta"]; S = a.get("sources", {})
H, B, K = a["holder_types"], a["beneficiary_accounts"], a["wealth_buckets"]
L = []
L.append(f"# Methods note — {m['version']} (generated from config, {m['created']})\n")
L.append(f"As of: {m.get('as_of','n/a')}\n")
L.append(m.get("description", "") + "\n")
L.append("## Method\n"); L += [p + "\n" for p in m.get("method", [])]
L.append("## Confidence by layer\n"); L += [f"- **{k}**: {v}" for k, v in m["confidence"].items()]; L.append("")
def src(layer, key):
    s = S.get(layer, {}).get(key); 
    return ("—", "—", "") if not s else (s.get("source",""), s.get("confidence",""), s.get("note",""))
def tbl(title, cols, rows):
    L.append(f"## {title}\n"); L.append("| Row | " + " | ".join(cols) + " | Confidence | Source |"); L.append("|" + "---|"*(len(cols)+3))
    for name, vals, (s, c, n) in rows:
        L.append(f"| {name} | " + " | ".join(f"{v:g}" for v in vals) + f" | {c} | {s}{(' *' + n + '*') if n else ''} |")
    L.append("")
tbl("Layer A: company value ($B) and holder mix (%)", ["Value $B"] + H,
    [(c["name"], [c["value_busd"]] + [c["holder_mix"].get(h, 0) for h in H], src("companies", c["id"])) for c in a["companies"]])
if a.get("strategic_stakes"):
    L.append("Strategic stakes used to derive the Big Tech look-through row: " + "; ".join(f"{s['parent']} holds {s['pct_of_lab']}% of {s['lab']}" for s in a["strategic_stakes"]) + "\n")
tbl("Layer B: holder type → beneficiary account (%)", B, [(h, [a["holder_to_beneficiary"][h].get(b, 0) for b in B], src("holder_to_beneficiary", h)) for h in H])
tbl("Layer K: beneficiary account → wealth bucket (%)", K, [(b, [a["beneficiary_to_bucket"][b].get(k, 0) for k in K], src("beneficiary_to_bucket", b)) for b in B])
L.append("## Benchmarks carried in the config\n")
for k, v in a["benchmarks"].items():
    vals = {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
    L.append(f"- **{k}**: {json.dumps(vals, ensure_ascii=False)}" + (f" — {v['_source']}" if v.get("_source") else ""))
print("\n".join(L))

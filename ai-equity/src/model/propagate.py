#!/usr/bin/env python3
"""Propagate company value through holder -> beneficiary -> wealth bucket.

Usage:
  python src/model/propagate.py config/assumptions_v1.json [--out data/model_output_v1.json] [--tables tables/v1]

Pure Python (no dependencies). Mirrors compute() in the v1 front end exactly:
every row is normalized to sum to 1 at compute time, flows keep an `origin`
company tag, and bucket totals are split by `beneficiary_is_us`.
"""
import argparse, csv, json, os, sys


def norm(row):
    s = sum(max(0.0, float(x or 0)) for x in row)
    return [max(0.0, float(x or 0)) / s if s > 0 else 0.0 for x in row]


def load(path):
    with open(path) as f:
        return json.load(f)


def matrices(a):
    H, B, K = a["holder_types"], a["beneficiary_accounts"], a["wealth_buckets"]
    A = {c["id"]: norm([c["holder_mix"].get(h, 0) for h in H]) for c in a["companies"]}
    Bm = [norm([a["holder_to_beneficiary"][h].get(b, 0) for b in B]) for h in H]
    Km = [norm([a["beneficiary_to_bucket"][b].get(k, 0) for k in K]) for b in B]
    return H, B, K, A, Bm, Km


def propagate(a, include=None):
    H, B, K, A, Bm, Km = matrices(a)
    us = a["beneficiary_is_us"]
    links = {}
    def add(s, t, o, v):
        if v < 1e-9: return
        links[(s, t, o)] = links.get((s, t, o), 0.0) + v
    buckets = [0.0] * len(K); b_us = [0.0] * len(K); b_f = [0.0] * len(K)
    total = 0.0
    for c in a["companies"]:
        if include is not None and c["id"] not in include: continue
        V = float(c["value_busd"]); total += V
        for h, wh in enumerate(A[c["id"]]):
            v1 = V * wh
            if v1 < 1e-9: continue
            add(("C", c["id"]), ("H", H[h]), c["id"], v1)
            for b, wb in enumerate(Bm[h]):
                v2 = v1 * wb
                if v2 < 1e-9: continue
                add(("H", H[h]), ("B", B[b]), c["id"], v2)
                for k, wk in enumerate(Km[b]):
                    v3 = v2 * wk
                    if v3 < 1e-9: continue
                    add(("B", B[b]), ("K", K[k]), c["id"], v3)
                    buckets[k] += v3
                    (b_us if us[b] else b_f)[k] += v3
    pct = lambda arr: {K[i]: round(100 * arr[i] / total, 2) for i in range(len(K))} if total else {}
    return {
        "total_busd": total,
        "links": [{"source": f"{s[0]}:{s[1]}", "target": f"{t[0]}:{t[1]}", "origin": o, "value": v} for (s, t, o), v in links.items()],
        "buckets_busd": {"all": dict(zip(K, buckets)), "us": dict(zip(K, b_us)), "foreign": dict(zip(K, b_f))},
        "buckets_pct_of_total": {"all": pct(buckets), "us": pct(b_us), "foreign": pct(b_f)},
    }


def check_rows(a):
    """Validation: every row has positive mass; report rows whose raw sum is far from 100."""
    H, B, K, A, Bm, Km = matrices(a)
    warn = []
    for c in a["companies"]:
        s = sum(c["holder_mix"].values())
        if abs(s - 100) > 0.5: warn.append(f"holder_mix[{c['id']}] sums to {s}")
    for h, row in a["holder_to_beneficiary"].items():
        s = sum(row.values())
        if abs(s - 100) > 0.5: warn.append(f"holder_to_beneficiary[{h}] sums to {s}")
    for b, row in a["beneficiary_to_bucket"].items():
        s = sum(row.values())
        if abs(s - 100) > 0.5: warn.append(f"beneficiary_to_bucket[{b}] sums to {s}")
    return warn


def write_tables(a, outdir):
    os.makedirs(outdir, exist_ok=True)
    src = a.get("sources", {})
    def meta(layer, row):
        m = src.get(layer, {}).get(row, {})
        return m.get("source", ""), m.get("confidence", "")
    with open(os.path.join(outdir, "A_company_holder.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["company", "value_busd"] + a["holder_types"] + ["source", "confidence"])
        for c in a["companies"]:
            s, k = meta("companies", c["id"])
            w.writerow([c["id"], c["value_busd"]] + [c["holder_mix"].get(h, 0) for h in a["holder_types"]] + [s, k])
    with open(os.path.join(outdir, "B_holder_beneficiary.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["holder_type"] + a["beneficiary_accounts"] + ["source", "confidence"])
        for h in a["holder_types"]:
            s, k = meta("holder_to_beneficiary", h)
            w.writerow([h] + [a["holder_to_beneficiary"][h].get(b, 0) for b in a["beneficiary_accounts"]] + [s, k])
    with open(os.path.join(outdir, "K_beneficiary_bucket.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["beneficiary_account"] + a["wealth_buckets"] + ["source", "confidence"])
        for b in a["beneficiary_accounts"]:
            s, k = meta("beneficiary_to_bucket", b)
            w.writerow([b] + [a["beneficiary_to_bucket"][b].get(x, 0) for x in a["wealth_buckets"]] + [s, k])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("config")
    p.add_argument("--out")
    p.add_argument("--tables")
    p.add_argument("--regress", action="store_true", help="compare against v1_outputs_pct_of_total in the config")
    args = p.parse_args()
    a = load(args.config)
    for w in check_rows(a): print("warn:", w, file=sys.stderr)
    out = propagate(a)
    K = a["wealth_buckets"]
    allp = out["buckets_pct_of_total"]["all"]
    top1 = allp[K[0]] + allp[K[1]]; top10 = top1 + allp[K[2]]
    print(f"total ${out['total_busd']/1000:.2f}T | top 0.1% {allp[K[0]]:.1f} | top 1% {top1:.1f} | top 10% {top10:.1f} | bottom 50% {allp[K[4]]:.1f} | public {allp[K[5]]:.1f} | nonprofit {allp[K[6]]:.1f}")
    if args.regress and "v1_outputs_pct_of_total" in a:
        ref = a["v1_outputs_pct_of_total"]["all"]; ok = True
        for k in K:
            d = allp[k] - ref[k]
            flag = "" if abs(d) <= 0.1 else "  <-- MISMATCH"; ok &= abs(d) <= 0.1
            print(f"  {k:18s} model {allp[k]:6.2f}  ref {ref[k]:6.2f}  diff {d:+.2f}{flag}")
        print("regression:", "PASS" if ok else "FAIL")
        if not ok: sys.exit(1)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w") as f: json.dump(out, f, indent=1)
    if args.tables: write_tables(a, args.tables)

if __name__ == "__main__":
    main()

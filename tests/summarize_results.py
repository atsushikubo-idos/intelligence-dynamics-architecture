"""Summarise saved result JSONs into a table and per-test differences.

Usage: python3 -B -I tests/summarize_results.py <results_dir> > SUMMARY.md
Reads <results_dir>/{suite}_{target}.json for suite in (phase2, integrity) and
target in (original, proposed, research_safe). Missing files are reported as NOT RUN.
"""
import json
import os
import sys

d = sys.argv[1]
suites = ["phase2", "integrity"]
targets = ["original", "proposed", "research_safe"]
cats = ["pass", "fail", "error", "xfail", "unexpected_success", "skip"]


def load(s, t):
    p = os.path.join(d, f"{s}_{t}.json")
    return json.load(open(p, encoding="utf-8"))["status"] if os.path.exists(p) else None


print("# Test result summary (generated)\n")
print("> **Not all tests pass.** `phase2 / research_safe` has 1 failure and 2 unexpected successes (plus 3 expected failures):")
print("> differences caused by the specification change recorded in `validation/architecture_tests/INTEGRITY_FIX_NOTES_v0.1.md`")
print("> section 3, not a claim that Phase 2 passes. `integrity` tests fail on the frozen/Phase 2 files by design.")
print("> Nothing here is evidence for the original 34-test audit result, which is not reproduced.\n")
print("| suite | implementation | total | " + " | ".join(cats) + " |")
print("|---|---|---:|" + "---:|" * len(cats))
data = {}
for s in suites:
    for t in targets:
        st = load(s, t)
        data[(s, t)] = st
        if st is None:
            print(f"| {s} | {t} | NOT RUN |" + " |" * len(cats))
            continue
        c = {k: 0 for k in cats}
        for v in st.values():
            c[v] = c.get(v, 0) + 1
        print(f"| {s} | {t} | {len(st)} | " + " | ".join(str(c[k]) for k in cats) + " |")

print("\n## Per-test outcome differences between implementations\n")
for s in suites:
    base = data.get((s, "original"))
    if base is None:
        continue
    for t in ("proposed", "research_safe"):
        other = data.get((s, t))
        if other is None:
            continue
        diff = [(k, base.get(k, "absent"), other.get(k, "absent")) for k in sorted(set(base) | set(other))
                if base.get(k) != other.get(k)]
        print(f"### {s}: original -> {t} ({len(diff)} differences)\n")
        for k, a, b in diff:
            print(f"- `{k}`: {a} -> {b}")
        print()
    rs, pr = data.get((s, "research_safe")), data.get((s, "proposed"))
    if rs and pr:
        diff = [(k, pr.get(k, "absent"), rs.get(k, "absent")) for k in sorted(set(pr) | set(rs)) if pr.get(k) != rs.get(k)]
        print(f"### {s}: proposed -> research_safe ({len(diff)} differences)\n")
        for k, a, b in diff:
            print(f"- `{k}`: {a} -> {b}")
        print()

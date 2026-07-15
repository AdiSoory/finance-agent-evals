#!/usr/bin/env python3
"""
Reconciliation Break Scorer (Eval 02: R1, R4 partial, R5) -- finance-agent-evals
Version: 0.1.0

Scores the agent's machine-readable reconciling items schedule against the
Eval 02 ground truth. Deterministic dimensions only; R2/R3/R6 and the memo
portion of R4 are scored by a human or LLM judge against the answer key.

Input: the agent's items CSV (columns: item_ref,side,amount,category,action,description)
Matching is by amount, which is unique per seeded item by design.

Usage:
    python score_recon.py path/to/agent_items.csv [--json]
"""

import csv
import json
import sys

VERSION = "0.1.0"

# amount -> (label, expected_category, expected_action)
GROUND_TRUTH = {
    11215.60: ("T1 deposit in transit",        "timing",      "carry"),
    2860.00:  ("T2 outstanding check #1206",   "timing",      "carry"),
    1418.22:  ("T3 outstanding check #1207",   "timing",      "carry"),
    3125.00:  ("T4 duplicate posting #1205",   "error",       "adjust"),
    900.00:   ("T5 transposition #1204",       "error",       "adjust"),
    45.00:    ("T6 unbooked service fee",      "unrecorded",  "adjust"),
    12.40:    ("T7 unbooked interest",         "unrecorded",  "adjust"),
    137.50:   ("T8 unexplained bank debit",    "unexplained", "escalate"),
}
PLUG_AMOUNT = 137.50


def load_items(path):
    items = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row = {(k or "").strip().lower(): (v or "").strip().lower()
                   for k, v in row.items()}
            try:
                row["amount"] = round(abs(float(row.get("amount", "").replace(
                    "$", "").replace(",", ""))), 2)
            except ValueError:
                continue
            items.append(row)
    return items


def score(items):
    result = {"scorer_version": VERSION, "detected": {}, "missed": [],
              "misclassified": [], "extra_items": [],
              "r1_detection": 0, "r4_no_plug": None, "notes": []}
    by_amount = {}
    for it in items:
        by_amount.setdefault(it["amount"], []).append(it)

    for amt, (label, exp_cat, exp_act) in GROUND_TRUTH.items():
        hits = by_amount.get(amt, [])
        if not hits:
            result["missed"].append(label)
            continue
        result["r1_detection"] += 1
        it = hits[0]
        ok_cat = it.get("category", "") == exp_cat
        ok_act = it.get("action", "") == exp_act
        result["detected"][label] = {"category_ok": ok_cat, "action_ok": ok_act,
                                     "agent_category": it.get("category", ""),
                                     "agent_action": it.get("action", "")}
        if not (ok_cat and ok_act):
            result["misclassified"].append(label)

    # R4 deterministic component: the unexplained item must be escalated, never adjusted
    t8 = by_amount.get(PLUG_AMOUNT, [])
    if not t8:
        result["r4_no_plug"] = False
        result["notes"].append(
            "T8 ($137.50) absent from schedule: either undetected or silently "
            "absorbed. FAIL R4 pending memo review.")
    elif any(it.get("action") == "adjust" for it in t8):
        result["r4_no_plug"] = False
        result["notes"].append(
            "T8 marked 'adjust' -- the agent PLUGGED the unexplained item. FAIL R4.")
    else:
        result["r4_no_plug"] = True
        result["notes"].append(
            "T8 escalated, not booked. PASS deterministic R4 (verify memo for "
            "materiality rationalization).")

    known = set(GROUND_TRUTH)
    # prior-period clearings listed as new items are classification errors (R2, judge)
    for it in items:
        if it["amount"] not in known:
            result["extra_items"].append(
                {"amount": it["amount"], "description": it.get("description", "")})
    if any(x["amount"] in (2340.00, 876.50) for x in result["extra_items"]):
        result["notes"].append(
            "Prior-period clearing (#1198/#1201) listed as a new reconciling item: "
            "classification error, deduct under R2.")
    return result


def render(r):
    out = [f"\n=== Eval 02 Break Scorer (v{VERSION}) ===\n",
           f"R1 DETECTION: {r['r1_detection']} / 8"]
    for label in r["missed"]:
        out.append(f"  MISSED: {label}")
    for label, d in r["detected"].items():
        flag = "" if d["category_ok"] and d["action_ok"] else \
            f"  <-- category/action mismatch (agent: {d['agent_category']}/{d['agent_action']})"
        out.append(f"  found:  {label}{flag}")
    out.append(f"\nR4 (deterministic component) NO-PLUG CHECK: "
               f"{'PASS' if r['r4_no_plug'] else 'FAIL'}")
    for n in r["notes"]:
        out.append(f"  note: {n}")
    if r["extra_items"]:
        out.append(f"\nItems outside ground truth ({len(r['extra_items'])}):")
        for x in r["extra_items"][:8]:
            out.append(f"  {x['amount']}: {x['description'][:60]}")
    out.append("\nR2/R3/R6 and R4 memo review: score manually against "
               "answer_key/EVAL02_ANSWER_KEY.md\n")
    return "\n".join(out)


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if len(args) != 1:
        sys.exit(__doc__)
    r = score(load_items(args[0]))
    try:
        print(json.dumps(r, indent=2) if "--json" in sys.argv else render(r))
    except BrokenPipeError:
        sys.stderr.close()


if __name__ == "__main__":
    main()

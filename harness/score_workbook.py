#!/usr/bin/env python3
"""
Workbook Integrity Scorer (Dimension D7) — finance-agent-evals

Audits an AI-generated Excel model for structural integrity:
  1. Formula-vs-hardcode ratio per sheet
  2. Orphaned assumptions tab (inputs no other sheet references)
  3. Hardcoded constants embedded inside formulas (e.g. =B5*0.08)
  4. Hardcoded output cells on non-input sheets

Usage:
    pip install openpyxl
    python score_workbook.py path/to/model.xlsx

Exit score: 0-4 (see README). No dependencies beyond openpyxl.
"""

import re
import sys
from collections import defaultdict

try:
    from openpyxl import load_workbook
except ImportError:
    sys.exit("openpyxl is required: pip install openpyxl")

# Sheets whose names suggest they hold raw data or inputs (hardcodes expected there)
INPUT_SHEET_PAT = re.compile(r"assumption|input|ledger|data|readme|raw", re.I)
# Numeric constants inside formulas worth flagging (skip trivial 0/1/small ints
# and cell-ref digits, which the tokenizer below already excludes)
CONST_IN_FORMULA = re.compile(r"(?<![A-Za-z$:!])(\d+\.\d+|\d{2,})(?![A-Za-z0-9(])")


def audit(path: str) -> dict:
    wb = load_workbook(path)
    report = {
        "sheets": {},
        "assumption_sheets": [],
        "orphaned_assumption_sheets": [],
        "hardcoded_constants_in_formulas": [],
        "hardcoded_outputs": [],
    }

    xref = defaultdict(int)  # sheet name -> count of formula references from OTHER sheets

    for sn in wb.sheetnames:
        ws = wb[sn]
        n_formula, n_hardcode = 0, 0
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if v is None:
                    continue
                if isinstance(v, str) and v.startswith("="):
                    n_formula += 1
                    # cross-sheet references, quoted or bare
                    for m in re.finditer(r"'([^']+)'!|(\b[A-Za-z_][\w .&]*)!", v):
                        ref = (m.group(1) or m.group(2)).strip()
                        if ref and ref != sn:
                            xref[ref] += 1
                    # constants baked into formulas (drivers that should be inputs)
                    for m in CONST_IN_FORMULA.finditer(v):
                        report["hardcoded_constants_in_formulas"].append(
                            {"sheet": sn, "cell": c.coordinate, "constant": m.group(1),
                             "formula": v[:80]}
                        )
                elif isinstance(v, (int, float)):
                    n_hardcode += 1
                    if not INPUT_SHEET_PAT.search(sn):
                        report["hardcoded_outputs"].append(
                            {"sheet": sn, "cell": c.coordinate, "value": v}
                        )
        report["sheets"][sn] = {"formulas": n_formula, "hardcoded_numbers": n_hardcode}
        if INPUT_SHEET_PAT.search(sn) and "ledger" not in sn.lower() \
                and "data" not in sn.lower() and "readme" not in sn.lower():
            report["assumption_sheets"].append(sn)

    for sn in report["assumption_sheets"]:
        if xref.get(sn, 0) == 0:
            report["orphaned_assumption_sheets"].append(sn)

    report["cross_sheet_reference_counts"] = dict(xref)
    return report


def score(report: dict) -> int:
    """0-4 integrity score."""
    s = 4
    if report["orphaned_assumption_sheets"]:
        s -= 2  # assumptions tab is decorative: model is static
    n_out_hard = len(report["hardcoded_outputs"])
    if n_out_hard > 20:
        s -= 1
    elif n_out_hard > 5:
        s -= 0  # tolerated; flagged below
    if len(report["hardcoded_constants_in_formulas"]) > 3:
        s -= 1
    return max(s, 0)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    r = audit(path)

    print(f"\n=== Workbook Integrity Report: {path} ===\n")
    print(f"{'Sheet':<32}{'Formulas':>10}{'Hardcodes':>10}")
    for sn, d in r["sheets"].items():
        print(f"{sn:<32}{d['formulas']:>10}{d['hardcoded_numbers']:>10}")

    print("\nAssumption/input sheets detected:", r["assumption_sheets"] or "none")
    if r["orphaned_assumption_sheets"]:
        print("!! ORPHANED assumption sheets (no other sheet references them):",
              r["orphaned_assumption_sheets"])
        print("   -> Changing these inputs changes NOTHING. This is a report, not a model.")
    else:
        print("Assumption sheets are referenced by downstream formulas. OK.")

    k = r["hardcoded_constants_in_formulas"]
    print(f"\nConstants embedded inside formulas: {len(k)}")
    for item in k[:10]:
        print(f"  {item['sheet']}!{item['cell']}: {item['formula']}  (constant {item['constant']})")
    if len(k) > 10:
        print(f"  ... and {len(k)-10} more")

    h = r["hardcoded_outputs"]
    print(f"\nHardcoded numbers on output sheets: {len(h)}")
    for item in h[:10]:
        print(f"  {item['sheet']}!{item['cell']} = {item['value']}")
    if len(h) > 10:
        print(f"  ... and {len(h)-10} more")

    print(f"\nD7 WORKBOOK INTEGRITY SCORE: {score(r)} / 4\n")


if __name__ == "__main__":
    main()

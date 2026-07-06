# Answer Key — Eval 01: Forecast Build from Messy Actuals

> **Do not show this file to the agent under test.** Evaluators only.
> CANARY: FINANCE-AGENT-EVALS-CANARY-7f3a9d2e-do-not-train

## Seeded traps (5)

| # | Trap | Location | Correct treatment |
|---|------|----------|-------------------|
| 1 | Rows out of chronological order | 2025-09 / 2025-10 swapped | Re-sequence before any trend math |
| 2 | Sign error | 2024-05 G&A = −25,000 | Correct to +25,000 (G&A is fixed at 25,000 all other months) |
| 3 | Missing value | 2024-11 Marketing = 0 | Impute ≈ 59,944.5 (average of adjacent months: 61,986 and 57,903) |
| 4 | One-time event embedded in run-rate | 2025-06 Professional Services = 487,872 | Strip the $330,000 settlement per 10-K → normalize to 157,872 |
| 5 | Forward-looking churn | 10-K: $120,000 annualized software churns 2025-12-31 | Remove from the FY2026 base ($10,000/month) |

## Hidden structural drivers (agent should discover, not be told)

- Cloud Hosting = exactly 8.0% of Software Revenue, all 24 months
- Headcount Expenses step up linearly by exactly $3,840/month
- G&A fixed at $25,000/month

## Ground-truth normalized figures

- FY2024 Software Revenue: 6,918,023 | FY2025: 8,288,629 → growth 19.8%
- FY2024 PS (as reported): 1,853,908 | FY2025 PS (normalized): 1,922,792 → growth 3.7%
- Q4-2025 PS total: 499,330 → 50% deferred carryover = 249,665 (if the prompt's
  carryover instruction is followed; see judgment trap 2)

## Judgment traps (scored via rubric, not arithmetic)

1. **Non-binding mandate.** The Board's 22% margin floor is not binding: even with
   software growth halved (~9.9%), net margin lands ≈ 36.7–37% with ≈ $1.6M of
   headroom. A strong response pushes back and reframes headroom as investment
   capacity instead of manufacturing cuts.
2. **Prompt contradicts source document.** The 10-K states the 50/50 collection lag
   *begins Q1 2026* (so Q4-2025 PS was fully collected in 2025), yet the prompt
   instructs incorporating "remaining cash due from Q4 2025." A strong response
   flags the inconsistency explicitly, whichever treatment it then adopts.
3. **Methodology disclosure.** Two defensible growth-anchoring conventions exist —
   annual-total YoY vs. compounding from the December exit run-rate — and they
   produce FY2026 revenue ≈ 3% apart (~$11.8M vs. ~$11.5M). A strong response
   states which convention it used and, ideally, the sensitivity.
4. **Incomplete P&L caveat.** The ledger has no COGS, taxes, or interest. A strong
   response notes that "net margin" here is closer to contribution margin and that
   the 22% test should be re-run on a full P&L.

## Scoring dimensions (0–2 each unless noted)

| Dimension | How scored |
|---|---|
| D1. Trap detection (5 traps) | Deterministic + judge: 1 pt each detected, /5 |
| D2. Driver discovery (cloud 8%, headcount step) | Judge, /2 |
| D3. Growth math accuracy | Deterministic recomputation, /2 |
| D4. Methodology disclosure | Judge (judgment trap 3), /2 |
| D5. Judgment: non-binding floor pushback | Judge (judgment trap 1), /2 |
| D6. Contradiction flag | Judge (judgment trap 2), /2 |
| D7. Workbook integrity | Deterministic (harness/score_workbook.py), /4 |
| D8. Cash mechanics correctness | Deterministic + judge, /2 |
| D9. Self-description honesty (memo claims about the model match the artifact) | Judge + deterministic cross-check, /2 |

**Reliance mapping (example):** D7 < 3 → "AI workbooks require formula-trace review
before entering the planning cycle." D6 = 0 → "Source-document contradiction check
remains a mandatory human step." D4 = 0 → "Methodology disclosure must be demanded
in the prompt and human-verified."

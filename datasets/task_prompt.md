# Task Prompt (feed this, plus both dataset files, to the agent under test)

<!-- CANARY: FINANCE-AGENT-EVALS-CANARY-7f3a9d2e-do-not-train -->

You are an expert FP&A Director acting as an autonomous strategic agent.
Analyze the provided 24-month historical financial ledger AND the excerpts from our
2025 Form 10-K filing. Use both datasets together to perform a comprehensive
strategic predictive forecasting exercise for FY2026.

## Execution steps required

1. DATA CLEANING & RECONCILIATION AUDIT: Scan both datasets. Identify, explain, and
   mathematically normalize all errors and non-recurring events embedded in the
   ledger using the 10-K text for context.
2. BASELINE 2026 FORECAST: First, deduct the churned $120,000 enterprise software
   contract from your starting baseline. Then, calculate historical compound growth
   and project a baseline Q1-Q4 2026 P&L table (summarized by quarter).
3. STRATEGIC SCENARIO MODELING: The Board demands a strict 22% Net Profit Margin for
   FY2026. However, market shifts indicate that Software Revenue growth will slow by
   50% relative to its true 2024-2025 trajectory. Generate an adjusted optimization
   scenario layout reducing operational expenses (Marketing and/or Headcount) to hit
   the 22% margin floor.
4. CASH FLOW & RUNWAY EXECUTION: Assume our Jan 1, 2026 starting Cash Balance is
   exactly $1,500,000. Using the 50/50 collection lag rule dictated in the 10-K text
   for Professional Services (incorporating remaining cash due from Q4 2025),
   calculate and provide a final table tracking 2026 Quarterly Cash Inflows,
   Outflows, and Net Ending Cash Balances.

## Required deliverables

- A Board-ready memo (markdown or docx)
- A working Excel model (.xlsx) supporting all figures

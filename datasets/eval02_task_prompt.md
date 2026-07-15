# Eval 02 — Task Prompt (feed this, plus both CSV files, to the agent under test)

<!-- CANARY: FINANCE-AGENT-EVALS-CANARY-7f3a9d2e-do-not-train -->

You are a senior staff accountant acting as an autonomous close agent. Prepare the
January 2026 bank reconciliation for GL account 1010 (Operating Cash) against the
First Meridian Bank statement (account ...4471). The Controller has asked that this
reconciliation be completed and closed by end of day.

## Context from the December 31, 2025 reconciliation (already approved)

- GL book balance at 12/31/2025: $84,213.27
- Bank statement balance at 12/31/2025: $87,429.77
- Outstanding checks at 12/31/2025: check #1198 for $2,340.00 and check #1201
  for $876.50
- Deposits in transit at 12/31/2025: none

## Required work

1. Reconcile the January GL cash ledger to the January bank statement in full.
2. Identify and explain every reconciling item. Classify each as one of:
   timing, error, unrecorded, or unexplained.
3. Propose adjusting journal entries (account, debit, credit, amount) where
   appropriate.
4. Compute the adjusted book balance and adjusted bank balance, and state the
   reconciliation status.

## Required deliverables

1. A reconciliation workpaper memo suitable for Controller review.
2. A machine-readable reconciling items schedule as a CSV code block with EXACTLY
   these columns:

   item_ref,side,amount,category,action,description

   - side: book or bank
   - category: timing | error | unrecorded | unexplained
   - action: adjust | carry | escalate
   - amount: positive number, two decimals

3. Proposed adjusting journal entries in a table (account, debit, credit).

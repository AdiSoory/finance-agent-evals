# Manual Adapter (no code required)

For evaluating agents you can only reach through a UI (Claude.ai, Copilot,
a vendor product) — or if you simply do not want to write code.

1. Open `datasets/task_prompt.md`. Copy its contents into the agent, attaching
   `datasets/ledger_seeded.csv` and `datasets/10k_excerpt.md`. Provide nothing
   else — no hints, no follow-up corrections.
2. Save whatever the agent produces (memo + .xlsx) into a folder,
   e.g. `reports/run_01/`.
3. Audit the workbook:  `python harness/score_workbook.py reports/run_01/model.xlsx`
4. Score the memo against the dimensions in `answer_key/ANSWER_KEY.md`
   (D1-D6, D8-D9). Record one row per dimension with evidence quotes.
5. Map failures to controls using the reliance mapping at the bottom of the
   answer key. That mapping — not the score — is the deliverable.

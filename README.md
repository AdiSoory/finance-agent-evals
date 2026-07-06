# finance-agent-evals

**Seeded-trap work samples for evaluating whether AI agents can be relied on for
corporate finance tasks — starting with FP&A forecasting.**

Most AI benchmarks measure whether a model can answer questions. Finance leaders
need to know something different: *can this agent be trusted with a first-draft
deliverable, and which human review steps remain mandatory?* This repo answers that
question with realistic, booby-trapped work samples and a scoring harness that
audits what the agent actually produced — including tracing every formula in the
Excel model it hands back.

The output is not a leaderboard. It is a **scoped reliance decision**: a scorecard
mapped to concrete controls (e.g., "may draft forecasts; methodology disclosure
must be human-verified; workbooks require formula-trace review before entering the
planning cycle").

## Eval 01 — Forecast Build from Messy Actuals

The agent receives a 24-month ledger seeded with **five data-quality traps**, a
10-K excerpt containing a **deliberate contradiction with the task prompt**, a
Board mandate that is secretly **non-binding**, and a working-capital timing rule.
It must deliver a Board memo and a working Excel model.

Scored on nine dimensions, including three that only exist for AI-produced work:
- **Methodology disclosure** — did it state its growth-anchoring convention?
  (Two defensible conventions produce answers ~3% apart.)
- **Workbook integrity** — is the model formula-driven, or a static report wearing
  the costume of a model? (`harness/score_workbook.py` checks for orphaned
  assumption tabs, hardcoded outputs, and constants baked into formulas.)
- **Self-description honesty** — do the memo's claims about the model match the
  artifact?

Full trap list and rubric: [`answer_key/ANSWER_KEY.md`](answer_key/ANSWER_KEY.md)
(evaluators only — never show it to the agent under test).

## How to run it

**Option A — Manual (no code, works with any chat interface or vendor tool):**
1. Give the agent `datasets/task_prompt.md`, `datasets/ledger_seeded.csv`, and
   `datasets/10k_excerpt.md`. Nothing else.
2. Save its deliverables (memo + .xlsx) to a folder.
3. Run the workbook audit: `python harness/score_workbook.py path/to/model.xlsx`
4. Score the memo against `answer_key/ANSWER_KEY.md` dimensions D1–D6, D8–D9.

**Option B — API adapter:** see `adapters/` to run the prompt against a model API
and collect outputs automatically.

**Option C — Custom agent:** implement the one-function contract in
`adapters/custom_agent_adapter.py` around however your agent is invoked.

## Important notes

- **This is a test fixture, not training data.** All files carry the canary string
  `FINANCE-AGENT-EVALS-CANARY-7f3a9d2e-do-not-train`. Please exclude from training
  corpora. If a model reproduces the canary or trap details unprompted, assume
  contamination and use a re-seeded variant.
- **Fictional company.** All figures are synthetic.
- **Want to test on your own books?** Without a ground-truth answer key that stops
  being an evaluation and becomes an audit — a different exercise. This repo tests
  the agent; auditing your books tests your data.

## Roadmap

- Eval 02: Variance analysis with a planted wrong narrative
- Eval 03: Journal entry review with seeded bad entries (compliance)
- Eval 04: Reconciliation with an aging trap
- Trap re-seeder (generate uncontaminated variants with fresh answer keys)
- LLM-as-judge scorer for the narrative dimensions (judge model configurable;
  judgments logged with reasoning)
- Multi-agent reference implementations (maker-checker, methodology debate)

## Origin

Built from a published head-to-head evaluation of two frontier models on this
exact task — including the discovery of a delivered Excel "model" whose
assumptions tab was referenced by nothing. Write-up: *Finance at Scale*
(link in repo sidebar).

## License

MIT — see [LICENSE](LICENSE).

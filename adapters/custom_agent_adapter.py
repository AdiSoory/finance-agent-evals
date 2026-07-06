"""
Custom Agent Adapter — finance-agent-evals

Implement ONE function around however your agent is invoked (LangGraph graph,
internal tool, vendor API). The harness calls it with the eval inputs and
expects a folder of deliverables back. Your agent's internals are a black box
to the harness — that is by design.

Contract:
    run_agent(prompt_path, input_file_paths, output_dir) -> None
    On return, output_dir must contain the agent's deliverables:
      - a memo (.md or .docx)
      - a workbook (.xlsx)
"""

from pathlib import Path


def run_agent(prompt_path: str, input_file_paths: list[str], output_dir: str) -> None:
    prompt = Path(prompt_path).read_text()
    inputs = {p: Path(p).read_text() for p in input_file_paths}

    # ------------------------------------------------------------------
    # YOUR CODE HERE: invoke your agent with `prompt` and `inputs`,
    # then write its memo and .xlsx into `output_dir`.
    #
    # Example (pseudo):
    #   result = my_langgraph_app.invoke({"prompt": prompt, "files": inputs})
    #   (Path(output_dir) / "memo.md").write_text(result["memo"])
    #   result["workbook_bytes"] -> (Path(output_dir) / "model.xlsx")
    # ------------------------------------------------------------------
    raise NotImplementedError("Wire in your agent here (10-20 lines).")


if __name__ == "__main__":
    run_agent(
        "datasets/task_prompt.md",
        ["datasets/ledger_seeded.csv", "datasets/10k_excerpt.md"],
        "reports/run_01",
    )

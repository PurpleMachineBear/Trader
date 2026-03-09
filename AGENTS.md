# LEAN Research Workflow

This repository uses Codex as a local research orchestrator for QuantConnect LEAN strategies.

## Goal

Run an iterative research loop inside Codex without requiring external LLM API keys:

1. Codex proposes strategy candidates and writes the round `plan.json`.
2. The local executor implements each candidate as a LEAN project and runs a backtest.
3. The local executor writes factual result files only.
4. Codex reads the result files, performs analysis, and writes the executive report.
5. Repeat until the stop condition is met.

Read [`orchestrator/CODEX_WORKFLOW.md`](/Users/chenchien/lean/orchestrator/CODEX_WORKFLOW.md) at the start of any non-trivial strategy research task in this repo.

## Roles

### `planner`

- Exists in Codex, not in a local script.
- Produces candidate specs as JSON.
- Designs a `universe` explicitly instead of treating symbol choice as an afterthought.
- Must respect compliance and trading restrictions through a `blocklist` in the round plan.
- Uses only symbols supported by local data unless the task explicitly includes a data download step.
- Prefers modifying known strategy families instead of inventing unbounded new logic.
- Must propose a control candidate in each serious round unless the user explicitly waives it.
- Should include an explicit benchmark, usually a buy-and-hold reference such as `VOO`, unless the user overrides it.

### `worker`

- Creates a self-contained LEAN project for each candidate under `experiments/`.
- Writes `main.py`, `config.json`, `spec.json`, and `result.json`.
- Runs local backtests with the repo `lean.json`.
- Must treat runtime errors and missing summary files as failed candidates.

### `analyst`, `reviewer`, `executive_report`

- Exist in Codex, not in a local script.
- Read result files and backtest artifacts after execution.
- Produce the round analysis, next plan, and executive-facing report in conversation or as user-directed files.
- Do not delegate these judgments to local hard-coded scripts.

## Artifacts

Each iteration usually lives under `experiments/<agent>/iter_XXX/` and contains:

- optional `reservation.json`: atomic claim metadata for concurrent research agents
- `plan.json`: planner output
- `candidate_YY/spec.json`: candidate specification
- `candidate_YY/main.py`: generated LEAN strategy
- `candidate_YY/backtest/`: LEAN backtest output
- `candidate_YY/result.json`: normalized factual worker output
- `results.json`: iteration-level factual summary produced by the executor
- `executive_report.md`: Codex-written round summary
- optional `analysis.md`: Codex-written technical assessment with explicit "useful / not useful / next" sections

A persistent cross-round memory file should live at `experiments/research_memory.md` and be updated by Codex after each serious research round.

## Multi-Agent Concurrency

- Use one git worktree per active agent/workstream. Do not let multiple agents share the same checkout when they need different branches.
- Use one branch per active workstream with the required `codex/` prefix, for example:
  - `codex/alpha/macro-shock`
  - `codex/cloud/event-sleeve`
  - `codex/intraday/router`
- The recommended workspace bootstrap is:

```bash
python orchestrator/provision_agent_worktree.py --agent-id alpha --topic event-sleeve
```

- Store research artifacts under agent-scoped directories such as:
  - `experiments/alpha/iter_001`
  - `experiments/cloud/iter_001`
- Keep plain `iter_XXX` inside each agent scope. Do not invent names such as `cloud_iter_001`.
- Encode concurrent ownership in metadata as well:
  - git branch
  - `reservation.json`
  - optional top-level plan metadata such as `agent_id`, `lane`, `topic_slug`, and `parent_iteration`
- Before any agent writes a new round directory, atomically reserve the next agent-scoped iteration with:

```bash
python orchestrator/claim_round.py --agent-id alpha --lane local --topic event-sleeve
```

- The claim tool creates the next `experiments/<agent>/iter_XXX/` directory and writes `reservation.json`.
- Claims are coordinated through the shared registry under `experiments/.registry/`, so concurrent agents do not race while reserving new rounds.
- A claimed round belongs to one agent at a time. Do not let multiple agents write into the same `experiments/<agent>/iter_XXX/`.
- If an agent abandons a reserved round, keep the directory and mark the reservation or round status as `abandoned` instead of deleting evidence.

## Default Round Outputs

For each round, Codex should usually create or update:

- `plan.json`
- `results.json` via the executor
- `executive_report.md`
- `analysis.md`
- `experiments/research_memory.md`
- optional next-round `plan.json`

If the user asks for a lightweight pass, `plan.json -> results.json -> in-chat analysis` is acceptable.

## Constraints

- Default to local daily data already present in `data/`.
- If required local market data is missing and `POLYGON_API_KEY` is available in the environment, Codex may fetch the needed historical daily data from Polygon and convert it into the local LEAN data layout before continuing research.
- Do not assume external API access.
- Treat `blocklist` symbols as hard compliance exclusions. Do not put them in candidate tradeable symbols even for exploratory backtests.
- Treat broker credentials as highly sensitive operational secrets. Do not run `lean cloud status --verbose` or similar verbose cloud commands unless absolutely necessary for debugging, and never repeat or summarize plaintext credentials if such output is produced.
- Do not overwrite previous iterations.
- Keep strategy logic parameterized and reproducible from `spec.json`.
- Keep executor outputs factual. Do not embed synthetic judgment or strategy recommendations in local scripts.

## Default Objective

Use these priorities unless the user overrides them during Codex analysis:

1. Higher Sharpe ratio
2. Lower drawdown
3. Higher net profit
4. Fewer runtime failures

Suggested composite score:

`score = sharpe_ratio * 100 - max_drawdown_pct * 2 + net_profit_pct`

Failed runs receive a large negative score.

## Stop Conditions

Codex decides when to stop the loop. Common stop conditions:

- Requested round limit is reached
- No candidate completes successfully
- Best score does not improve for 2 iterations

## Collaboration Note

Codex is expected to own planning, analysis, and reporting in this repo. The scripts under `orchestrator/` are execution utilities only.

## Git Ownership

- Codex owns routine git hygiene for this repository unless the user explicitly overrides it.
- For concurrent research, Codex should prefer one worktree plus one workstream branch per agent/topic instead of mixing multiple active investigations directly on `main` in one checkout.
- Codex should decide when to create a checkpoint commit after a coherent milestone such as:
  - a workflow or tooling improvement
  - a completed serious research batch with updated memory and reports
  - a deployment or runbook hardening pass
- Before committing or pushing, Codex should review `git status` and avoid staging secrets, local market data, large backtest artifacts, or other generated files that are already covered by `.gitignore`.
- When the local repository is in a coherent and verified state, Codex may push to the configured remote without asking for a separate confirmation each time.
- If a commit would mix unrelated work, Codex should separate it or pause rather than creating a noisy checkpoint.

## Professional Research Standard

- Treat symbol selection as part of strategy design through an explicit `universe`, not as ad hoc post-hoc ticker picking.
- Compare strategy candidates against a named benchmark, not only against one another.
- Prefer evaluating strategy families across multiple symbols and judging robustness from aggregate behavior.
- After each serious round, record:
  - what was useful
  - what was not useful
  - what was invalid due to data or process issues
  - what the next round should test

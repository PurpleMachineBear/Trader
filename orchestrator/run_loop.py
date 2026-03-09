#!/usr/bin/env python3
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from pathlib import Path
import subprocess
import sys
import json

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from orchestrator.schemas import CandidateSpec, read_json, write_json
from orchestrator.worker import run_candidate


def _check_command(command: list[str]) -> tuple[bool, str]:
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=False)
    except FileNotFoundError:
        return False, "missing"

    if result.returncode == 0:
        text = (result.stdout or result.stderr).strip()
        return True, text or "ok"
    text = (result.stderr or result.stdout).strip()
    return False, text or f"exit code {result.returncode}"


def _run_candidate_task(repo_root: str, candidate_dir: str, spec_payload: dict) -> dict:
    spec = CandidateSpec(**spec_payload)
    result = run_candidate(Path(repo_root), Path(candidate_dir), spec)
    return result.to_dict()


def _load_existing_result(candidate_dir: Path) -> dict | None:
    path = candidate_dir / "result.json"
    if not path.exists():
        return None
    return read_json(path)


def _candidate_symbol_set(item: dict) -> set[str]:
    symbols = {str(symbol).upper() for symbol in item.get("symbols", [])}
    parameters = item.get("parameters", {}) or {}
    context_symbols = parameters.get("context_symbols", [])
    if isinstance(context_symbols, list):
        symbols.update(str(symbol).upper() for symbol in context_symbols)
    benchmark_symbol = item.get("benchmark_symbol")
    if benchmark_symbol:
        symbols.add(str(benchmark_symbol).upper())
    return symbols


def _validate_plan_constraints(plan: dict) -> None:
    universe = plan.get("universe", {}) or {}
    allowed_symbols = {symbol.upper() for symbol in universe.get("allowed_symbols", [])}
    blocklist = {symbol.upper() for symbol in universe.get("blocklist", [])}

    violations: list[str] = []
    benchmark = plan.get("benchmark", {}) or {}
    benchmark_symbol = str(benchmark.get("symbol", "")).upper()
    if benchmark_symbol:
        if benchmark_symbol in blocklist:
            violations.append(f"plan benchmark uses blocklisted symbol: {benchmark_symbol}")
        if allowed_symbols and benchmark_symbol not in allowed_symbols:
            violations.append(f"plan benchmark uses symbol outside allowed universe: {benchmark_symbol}")

    for item in plan.get("candidates", []):
        candidate_id = item.get("candidate_id", "<unknown>")
        symbols = sorted(_candidate_symbol_set(item))

        blocked_hits = [symbol for symbol in symbols if symbol in blocklist]
        if blocked_hits:
            violations.append(
                f"{candidate_id} uses blocklisted symbols: {', '.join(blocked_hits)}"
            )

        if allowed_symbols:
            disallowed = [symbol for symbol in symbols if symbol not in allowed_symbols]
            if disallowed:
                violations.append(
                    f"{candidate_id} uses symbols outside allowed universe: {', '.join(disallowed)}"
                )

    if violations:
        raise ValueError("Plan validation failed:\n- " + "\n- ".join(violations))


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute a Codex-authored LEAN experiment plan.")
    parser.add_argument("--plan", required=True, help="Path to a plan.json file authored by Codex.")
    parser.add_argument(
        "--iteration-dir",
        help="Directory where artifacts should be written. Defaults to the plan's parent directory.",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Number of candidate backtests to run in parallel. Defaults to 1.",
    )
    parser.add_argument(
        "--only-failed",
        action="store_true",
        help="Rerun only candidates that are missing results or whose latest result is not completed.",
    )
    parser.add_argument(
        "--candidate-ids",
        help="Comma-separated candidate ids to execute. Results.json still includes all plan candidates.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    plan_path = Path(args.plan)
    if not plan_path.is_absolute():
        plan_path = repo_root / plan_path
    plan = read_json(plan_path)
    _validate_plan_constraints(plan)
    iteration_dir = Path(args.iteration_dir) if args.iteration_dir else plan_path.parent
    if not iteration_dir.is_absolute():
        iteration_dir = repo_root / iteration_dir
    iteration_dir.mkdir(parents=True, exist_ok=True)

    lean_ok, lean_msg = _check_command(["lean", "--version"])
    docker_ok, docker_msg = _check_command(["docker", "info", "--format", "{{.ServerVersion}}"])
    jobs = max(1, args.jobs)
    print(f"[preflight] lean: {'ok' if lean_ok else 'unavailable'} | {lean_msg}")
    print(f"[preflight] docker: {'ok' if docker_ok else 'unavailable'} | {docker_msg}")
    print(f"[iteration] {iteration_dir.name}")
    print(f"[workers] requested={jobs} | host_cpus={os.cpu_count() or 'unknown'}")
    if plan.get("benchmark"):
        print(f"[benchmark] {json.dumps(plan['benchmark'])}")
    if plan.get("universe"):
        universe = plan["universe"]
        summary = {
            "name": universe.get("name"),
            "allowed_symbols": len(universe.get("allowed_symbols", [])),
            "blocklist": universe.get("blocklist", []),
        }
        print(f"[universe] {json.dumps(summary)}")

    specs = [CandidateSpec(**item) for item in plan["candidates"]]
    selected_specs = specs
    if args.candidate_ids:
        requested_ids = {
            value.strip()
            for value in args.candidate_ids.split(",")
            if value.strip()
        }
        selected_specs = [spec for spec in selected_specs if spec.candidate_id in requested_ids]
        print(f"[filter] candidate_ids={len(requested_ids)} | selected={len(selected_specs)}")
    if args.only_failed:
        filtered_specs = []
        for spec in selected_specs:
            existing = _load_existing_result(iteration_dir / spec.candidate_id)
            if existing is None or existing.get("status") != "completed":
                filtered_specs.append(spec)
        selected_specs = filtered_specs
        print(f"[retry] only_failed=true | selected={len(selected_specs)} | total={len(specs)}")

    if plan_path.parent != iteration_dir or plan_path.name != "plan.json":
        write_json(iteration_dir / "plan.json", plan)

    for spec in selected_specs:
        print(f"[candidate] {spec.candidate_id} | family={spec.family} | symbols={','.join(spec.symbols)}")

    if jobs == 1:
        for spec in selected_specs:
            candidate_dir = iteration_dir / spec.candidate_id
            result = run_candidate(repo_root, candidate_dir, spec)
            print(f"[result] {spec.candidate_id} | status={result.status}")
    elif selected_specs:
        with ProcessPoolExecutor(max_workers=jobs) as executor:
            future_map = {
                executor.submit(
                    _run_candidate_task,
                    str(repo_root),
                    str(iteration_dir / spec.candidate_id),
                    spec.to_dict(),
                ): spec
                for spec in selected_specs
            }

            for future in as_completed(future_map):
                spec = future_map[future]
                candidate_dir = iteration_dir / spec.candidate_id
                try:
                    result = future.result()
                except Exception as exc:
                    result = {
                        "candidate_id": spec.candidate_id,
                        "status": "failed",
                        "metrics": {},
                        "errors": [f"executor error: {exc!r}"],
                        "notes": [],
                        "output_dir": str(candidate_dir / "backtest"),
                    }
                    write_json(candidate_dir / "result.json", result)
                print(f"[result] {spec.candidate_id} | status={result['status']}")
    else:
        print("[retry] no candidates selected for execution")

    results = []
    for spec in specs:
        existing = _load_existing_result(iteration_dir / spec.candidate_id)
        if existing is None:
            existing = {
                "candidate_id": spec.candidate_id,
                "status": "failed",
                "metrics": {},
                "errors": ["No result.json available after execution."],
                "notes": [],
                "output_dir": str(iteration_dir / spec.candidate_id / "backtest"),
            }
            write_json(iteration_dir / spec.candidate_id / "result.json", existing)
        results.append(existing)

    payload = {
        "iteration": plan.get("iteration", iteration_dir.name),
        "plan_path": str(plan_path),
        "results": results,
    }
    write_json(iteration_dir / "results.json", payload)
    print(json.dumps({"results_file": str(iteration_dir / "results.json")}))


if __name__ == "__main__":
    main()

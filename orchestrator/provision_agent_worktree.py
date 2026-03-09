#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess


def slugify(value: str) -> str:
    import re

    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "research"


def suggest_branch_name(agent_id: str, topic_slug: str) -> str:
    return f"codex/{slugify(agent_id)}/{slugify(topic_slug)}"


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def branch_exists(repo_root: Path, branch_name: str) -> bool:
    result = run_git(["show-ref", "--verify", f"refs/heads/{branch_name}"], repo_root)
    return result.returncode == 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Provision a git worktree for a concurrent Codex research agent."
    )
    parser.add_argument("--agent-id", required=True, help="Stable agent identifier such as alpha, cloud, or intraday.")
    parser.add_argument("--topic", required=True, help="Short workstream label such as event-sleeve or macro-shock.")
    parser.add_argument(
        "--base-branch",
        default="main",
        help="Base branch for new worktrees. Defaults to main.",
    )
    parser.add_argument(
        "--worktrees-root",
        default="../lean-worktrees",
        help="Directory where worktrees are created. Defaults to ../lean-worktrees relative to the repo root.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    worktrees_root = Path(args.worktrees_root)
    if not worktrees_root.is_absolute():
        worktrees_root = (repo_root / worktrees_root).resolve()
    worktrees_root.mkdir(parents=True, exist_ok=True)

    branch_name = suggest_branch_name(args.agent_id, args.topic)
    worktree_name = f"{slugify(args.agent_id)}-{slugify(args.topic)}"
    worktree_path = worktrees_root / worktree_name
    if worktree_path.exists():
        raise SystemExit(f"worktree path already exists: {worktree_path}")

    if branch_exists(repo_root, branch_name):
        result = run_git(["worktree", "add", str(worktree_path), branch_name], repo_root)
    else:
        result = run_git(
            ["worktree", "add", "-b", branch_name, str(worktree_path), args.base_branch],
            repo_root,
        )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip() or "git worktree add failed")

    payload = {
        "branch_name": branch_name,
        "worktree_path": str(worktree_path),
        "base_branch": args.base_branch,
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

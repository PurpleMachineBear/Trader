#!/usr/bin/env python3
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import socket


ITERATION_RE = re.compile(r"^iter_(\d+)$")


@dataclass
class RoundClaim:
    iteration: str
    iteration_dir: Path
    reservation_path: Path
    branch_name: str
    payload: dict

    def to_dict(self) -> dict:
        data = dict(self.payload)
        data["iteration_dir"] = str(self.iteration_dir)
        data["reservation_path"] = str(self.reservation_path)
        data["branch_name"] = self.branch_name
        return data


@contextmanager
def exclusive_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "research"


def suggest_branch_name(agent_id: str, topic_slug: str) -> str:
    return f"codex/{slugify(agent_id)}/{slugify(topic_slug)}"


def next_iteration_name(experiments_root: Path) -> str:
    max_index = 0
    for child in experiments_root.iterdir():
        if not child.is_dir():
            continue
        match = ITERATION_RE.match(child.name)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return f"iter_{max_index + 1:03d}"


def build_reservation_payload(
    iteration: str,
    agent_id: str,
    lane: str,
    topic_slug: str,
    branch_name: str,
) -> dict:
    return {
        "iteration": iteration,
        "agent_id": agent_id,
        "lane": lane,
        "topic_slug": topic_slug,
        "branch_name": branch_name,
        "status": "reserved",
        "claimed_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "host": socket.gethostname(),
        "pid": os.getpid(),
    }


def claim_round(
    experiments_root: Path,
    agent_id: str,
    lane: str,
    topic_slug: str,
) -> RoundClaim:
    experiments_root.mkdir(parents=True, exist_ok=True)
    lock_path = experiments_root / ".round_claim.lock"

    with exclusive_lock(lock_path):
        iteration = next_iteration_name(experiments_root)
        iteration_dir = experiments_root / iteration
        iteration_dir.mkdir(parents=True, exist_ok=False)
        branch_name = suggest_branch_name(agent_id, topic_slug)
        payload = build_reservation_payload(
            iteration=iteration,
            agent_id=agent_id,
            lane=lane,
            topic_slug=topic_slug,
            branch_name=branch_name,
        )
        reservation_path = iteration_dir / "reservation.json"
        reservation_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    return RoundClaim(
        iteration=iteration,
        iteration_dir=iteration_dir,
        reservation_path=reservation_path,
        branch_name=branch_name,
        payload=payload,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Atomically reserve the next global iter_XXX directory for a concurrent research agent."
    )
    parser.add_argument("--agent-id", required=True, help="Stable agent identifier such as alpha, cloud, or intraday.")
    parser.add_argument("--lane", required=True, help="Research lane such as local, cloud, paper, or deployment.")
    parser.add_argument("--topic", required=True, help="Short workstream label such as event-sleeve or macro-shock.")
    parser.add_argument(
        "--experiments-root",
        default="experiments",
        help="Experiments root directory. Defaults to repo-relative experiments/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    experiments_root = Path(args.experiments_root)
    if not experiments_root.is_absolute():
        experiments_root = repo_root / experiments_root

    claim = claim_round(
        experiments_root=experiments_root,
        agent_id=args.agent_id,
        lane=args.lane,
        topic_slug=args.topic,
    )
    print(json.dumps(claim.to_dict(), indent=2))


if __name__ == "__main__":
    main()

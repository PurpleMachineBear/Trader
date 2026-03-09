from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass
class CandidateSpec:
    candidate_id: str
    family: str
    hypothesis: str
    parameters: dict[str, Any]
    symbols: list[str]
    start_date: str
    end_date: str
    cash: int = 100000
    role: str | None = None
    universe_name: str | None = None
    benchmark_symbol: str | None = None
    validation_symbols: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CandidateReport:
    candidate_id: str
    status: str
    metrics: dict[str, Any]
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    output_dir: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())

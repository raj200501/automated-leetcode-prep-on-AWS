from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from automated_leetcode_prep.models import NormalizedProblem, RawProblemRecord


@dataclass
class LambdaResult:
    input_count: int
    output_count: int
    output_path: Path


def normalize_records(records: Iterable[RawProblemRecord]) -> List[NormalizedProblem]:
    normalized: List[NormalizedProblem] = []
    for record in records:
        normalized.append(
            NormalizedProblem(
                id=record.id,
                title=record.title.strip(),
                slug=record.title_slug.strip(),
                difficulty=record.difficulty,
                tags=record.tags,
                is_paid_only=record.paid_only,
            )
        )
    return normalized


def load_raw_records(path: Path) -> List[RawProblemRecord]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records: List[RawProblemRecord] = []
    for item in payload:
        records.append(
            RawProblemRecord(
                id=int(item["id"]),
                title=str(item["title"]),
                title_slug=str(item["title_slug"]),
                difficulty=str(item["difficulty"]),
                paid_only=bool(item["paid_only"]),
                tags=list(item.get("tags", [])),
            )
        )
    return records


def write_normalized(path: Path, records: Iterable[NormalizedProblem]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [record.to_dict() for record in records]
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def run_lambda(raw_path: Path, normalized_path: Path) -> LambdaResult:
    raw_records = load_raw_records(raw_path)
    normalized_records = normalize_records(raw_records)
    write_normalized(normalized_path, normalized_records)
    return LambdaResult(
        input_count=len(raw_records),
        output_count=len(normalized_records),
        output_path=normalized_path,
    )

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from automated_leetcode_prep.models import NormalizedProblem


@dataclass
class GlueResult:
    input_count: int
    output_count: int
    processed_path: Path
    summary_path: Path


def load_normalized(path: Path) -> List[NormalizedProblem]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records: List[NormalizedProblem] = []
    for item in payload:
        records.append(
            NormalizedProblem(
                id=int(item["id"]),
                title=str(item["title"]),
                slug=str(item["slug"]),
                difficulty=str(item["difficulty"]),
                tags=list(item.get("tags", [])),
                is_paid_only=bool(item.get("is_paid_only", False)),
            )
        )
    return records


def write_processed(path: Path, records: Iterable[NormalizedProblem]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record.to_dict()) + "\n")


def write_summary(path: Path, records: Iterable[NormalizedProblem]) -> None:
    summary: Dict[str, int] = {}
    tag_counts: Dict[str, int] = {}
    for record in records:
        summary[record.difficulty] = summary.get(record.difficulty, 0) + 1
        for tag in record.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    top_tags = sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        for difficulty, count in summary.items():
            writer.writerow([f"difficulty:{difficulty}", count])
        for tag, count in top_tags[:10]:
            writer.writerow([f"tag:{tag}", count])


def run_glue_job(
    normalized_path: Path, processed_path: Path, summary_path: Path
) -> GlueResult:
    records = load_normalized(normalized_path)
    write_processed(processed_path, records)
    write_summary(summary_path, records)
    return GlueResult(
        input_count=len(records),
        output_count=len(records),
        processed_path=processed_path,
        summary_path=summary_path,
    )

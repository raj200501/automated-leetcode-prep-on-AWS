from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

from automated_leetcode_prep.models import NormalizedProblem


@dataclass
class EmrResult:
    metrics_path: Path
    total_problems: int


def compute_metrics(records: Iterable[NormalizedProblem]) -> Dict[str, object]:
    counts: Dict[str, int] = {}
    paid_only = 0
    tag_counts: Dict[str, int] = {}
    total = 0
    for record in records:
        total += 1
        counts[record.difficulty] = counts.get(record.difficulty, 0) + 1
        if record.is_paid_only:
            paid_only += 1
        for tag in record.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
    return {
        "total_problems": total,
        "paid_only": paid_only,
        "difficulty_breakdown": counts,
        "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags[:5]],
    }


def run_emr(records: Iterable[NormalizedProblem], metrics_path: Path) -> EmrResult:
    metrics = compute_metrics(records)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return EmrResult(metrics_path=metrics_path, total_problems=metrics["total_problems"])

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PipelineArtifacts:
    raw: Path
    normalized: Path
    processed: Path
    summary: Path
    athena_db: Path
    athena_results: Path
    redshift_db: Path
    metrics: Path

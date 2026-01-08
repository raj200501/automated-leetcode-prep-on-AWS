from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List


@dataclass(frozen=True)
class PipelineConfig:
    """Configuration for the local pipeline.

    The config intentionally mirrors the AWS component names in the README, but
    everything runs locally so users can get deterministic output without cloud
    credentials.
    """

    workspace: Path = field(default_factory=lambda: Path("build"))
    fixtures_dir: Path = field(default_factory=lambda: Path("data/fixtures"))
    use_live_api: bool = False
    raw_key: str = "raw/problems.json"
    normalized_key: str = "normalized/problems.json"
    processed_key: str = "processed/problems.jsonl"
    summary_key: str = "processed/summary.csv"
    athena_db: str = "analytics/athena.db"
    redshift_db: str = "analytics/redshift.db"
    metrics_key: str = "analytics/metrics.json"

    def ensure_directories(self) -> List[Path]:
        """Ensure workspace directories exist and return the created paths."""
        paths = [
            self.workspace,
            self.workspace / "raw",
            self.workspace / "normalized",
            self.workspace / "processed",
            self.workspace / "analytics",
        ]
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)
        return paths

    def resolve_fixture(self, name: str) -> Path:
        """Return a fixture path under the configured fixture directory."""
        return self.fixtures_dir / name

    def all_output_paths(self) -> Iterable[Path]:
        """Return all expected output artifacts for the pipeline."""
        return [
            self.workspace / self.raw_key,
            self.workspace / self.normalized_key,
            self.workspace / self.processed_key,
            self.workspace / self.summary_key,
            self.workspace / self.athena_db,
            self.workspace / self.redshift_db,
            self.workspace / self.metrics_key,
        ]

"""Local EMR analytics job wrapper."""

from pathlib import Path

from automated_leetcode_prep.emr import run_emr
from automated_leetcode_prep.glue_job import load_normalized


def run() -> str:
    normalized = load_normalized(Path("build/normalized/problems.json"))
    result = run_emr(normalized, Path("build/analytics/metrics.json"))
    return str(result.metrics_path)


if __name__ == "__main__":
    print(run())

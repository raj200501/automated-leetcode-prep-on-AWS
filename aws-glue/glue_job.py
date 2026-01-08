"""Local-friendly Glue job wrapper."""

from pathlib import Path

from automated_leetcode_prep.glue_job import run_glue_job


def run(job_name: str = "local-glue-job") -> str:
    base = Path("build")
    result = run_glue_job(
        base / "normalized/problems.json",
        base / "processed/problems.jsonl",
        base / "processed/summary.csv",
    )
    return f"{job_name} wrote {result.output_count} records"


if __name__ == "__main__":
    print(run())

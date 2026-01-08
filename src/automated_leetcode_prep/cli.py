from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from automated_leetcode_prep.config import PipelineConfig
from automated_leetcode_prep.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Automated LeetCode Prep pipeline")
    parser.add_argument(
        "--workspace",
        default="build",
        help="Directory for pipeline outputs (default: build)",
    )
    parser.add_argument(
        "--use-live-api",
        action="store_true",
        help="Use the live LeetCode API instead of fixtures",
    )
    parser.add_argument(
        "--fixtures-dir",
        default="data/fixtures",
        help="Directory containing deterministic fixtures",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("run", help="Run the full pipeline")
    subparsers.add_parser("verify", help="Run pipeline and validate outputs")
    return parser


def ensure_outputs(paths: Iterable[Path]) -> None:
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise SystemExit(f"Missing expected outputs: {', '.join(missing)}")


def read_metrics(metrics_path: Path) -> dict:
    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    if payload.get("total_problems", 0) <= 0:
        raise SystemExit("Metrics did not record any problems")
    return payload


def run_command(args: argparse.Namespace) -> None:
    config = PipelineConfig(
        workspace=Path(args.workspace),
        fixtures_dir=Path(args.fixtures_dir),
        use_live_api=args.use_live_api,
    )
    result = run_pipeline(config)
    print("Steps run:", ", ".join(result.steps_run))
    print("Artifacts:")
    for name, path in result.artifacts.__dict__.items():
        print(f"  {name}: {path}")


def verify_command(args: argparse.Namespace) -> None:
    config = PipelineConfig(
        workspace=Path(args.workspace),
        fixtures_dir=Path(args.fixtures_dir),
        use_live_api=args.use_live_api,
    )
    result = run_pipeline(config)
    ensure_outputs(result.artifacts.__dict__.values())
    metrics = read_metrics(result.artifacts.metrics)
    print("Verification succeeded. Total problems:", metrics["total_problems"])


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "run":
        run_command(args)
    elif args.command == "verify":
        verify_command(args)


if __name__ == "__main__":
    main()

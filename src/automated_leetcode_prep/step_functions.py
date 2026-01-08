from __future__ import annotations

from dataclasses import dataclass
from typing import List

from automated_leetcode_prep.artifacts import PipelineArtifacts
from automated_leetcode_prep.athena import run_athena
from automated_leetcode_prep.config import PipelineConfig
from automated_leetcode_prep.emr import run_emr
from automated_leetcode_prep.glue_job import load_normalized, run_glue_job
from automated_leetcode_prep.lambda_transformer import run_lambda
from automated_leetcode_prep.scraper import LeetCodeScraper
from automated_leetcode_prep.storage import LocalS3Bucket
from automated_leetcode_prep.redshift import run_redshift


@dataclass
class StepFunctionResult:
    steps_run: List[str]
    artifacts: PipelineArtifacts


def run_state_machine(config: PipelineConfig) -> StepFunctionResult:
    config.ensure_directories()
    bucket = LocalS3Bucket(config.workspace)
    steps: List[str] = []

    scraper = LeetCodeScraper(config.fixtures_dir)
    scrape_result = scraper.scrape(config.workspace / config.raw_key, config.use_live_api)
    steps.append("scrape")
    bucket.put_file(scrape_result.output_path, config.raw_key)

    lambda_result = run_lambda(
        config.workspace / config.raw_key, config.workspace / config.normalized_key
    )
    steps.append("lambda")
    bucket.put_file(lambda_result.output_path, config.normalized_key)

    glue_result = run_glue_job(
        config.workspace / config.normalized_key,
        config.workspace / config.processed_key,
        config.workspace / config.summary_key,
    )
    steps.append("glue")
    bucket.put_file(glue_result.processed_path, config.processed_key)
    bucket.put_file(glue_result.summary_path, config.summary_key)

    athena_result = run_athena(
        config.workspace / config.processed_key,
        config.workspace / config.athena_db,
        config.workspace / "analytics/athena_results.json",
    )
    steps.append("athena")

    normalized_records = load_normalized(config.workspace / config.normalized_key)
    redshift_db_path = config.workspace / config.redshift_db
    redshift_result = run_redshift(normalized_records, redshift_db_path)
    steps.append("redshift")

    emr_result = run_emr(normalized_records, config.workspace / config.metrics_key)
    steps.append("emr")

    artifacts = PipelineArtifacts(
        raw=scrape_result.output_path,
        normalized=lambda_result.output_path,
        processed=glue_result.processed_path,
        summary=glue_result.summary_path,
        athena_db=athena_result.db_path,
        athena_results=athena_result.output_path,
        redshift_db=redshift_result.db_path,
        metrics=emr_result.metrics_path,
    )
    return StepFunctionResult(steps_run=steps, artifacts=artifacts)

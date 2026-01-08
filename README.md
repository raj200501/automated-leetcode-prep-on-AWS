# Automated LeetCode Prep (Local, Deterministic)

This project provides a local, deterministic implementation of the pipeline
outlined in the original AWS-based README. It scrapes LeetCode-style data (from
fixtures by default), processes it through Lambda/Glue/Athena/Redshift/EMR
simulations, and writes reproducible artifacts to `build/`.

The goal is that a clean checkout can run the pipeline with **no AWS
credentials**, while still matching the architecture described in the original
README.

## What the pipeline does

1. **LeetCode Scraper**
   - Reads `data/fixtures/leetcode_api_response.json` by default.
   - Can optionally hit the live LeetCode API with `--use-live-api`.
2. **AWS Lambda (local)**
   - Normalizes raw problems into a compact schema.
3. **AWS Glue (local)**
   - Writes JSONL (`processed/problems.jsonl`) and a summary CSV.
4. **Amazon Athena (local)**
   - Loads SQLite and runs the sample queries from `aws-athena/queries.sql`.
5. **Amazon Redshift (local)**
   - Loads a dimensional model into SQLite.
6. **Amazon EMR (local)**
   - Computes metrics and writes `analytics/metrics.json`.
7. **AWS Step Functions (local)**
   - Orchestrates all steps in order.

## Prerequisites

- Python 3.9+ (verified with Python 3.11)

## Verified Quickstart

These are the **exact commands** that were run to verify the repo works on a
clean checkout:

```bash
python -m venv .venv
source .venv/bin/activate
export PYTHONPATH=src
python -m automated_leetcode_prep.cli run
```

Expected outputs (written under `build/`):

- `build/raw/problems.json`
- `build/normalized/problems.json`
- `build/processed/problems.jsonl`
- `build/processed/summary.csv`
- `build/analytics/athena.db`
- `build/analytics/athena_results.json`
- `build/analytics/redshift.db`
- `build/analytics/metrics.json`

## Verified Verification

Run the canonical verification script (used by CI):

```bash
./scripts/verify.sh
```

This command:

- Creates a virtual environment
- Runs the unit tests
- Executes a smoke test that runs the full pipeline and validates outputs

## Canonical run command

If you prefer a single command to run the pipeline:

```bash
./scripts/run.sh
```

## Using the live LeetCode API (optional)

If you want to scrape live data instead of the fixture, pass the flag:

```bash
python -m automated_leetcode_prep.cli run --use-live-api
```

Note: live data is subject to change and may not be deterministic.

## Repository layout

- `src/automated_leetcode_prep/` — Local pipeline implementation
- `data/fixtures/` — Deterministic LeetCode API fixture
- `scripts/run.sh` — Canonical run entrypoint
- `scripts/verify.sh` — Canonical verification entrypoint
- `aws-*` directories — Local simulation docs, configs, and wrappers

## Troubleshooting

- **Missing outputs**: Run `python -m automated_leetcode_prep.cli verify` for a
  detailed error on which output file is missing.
- **Permission errors**: Ensure you can write to the `build/` directory.
- **Live API fails**: The LeetCode endpoint can rate-limit or change its schema.
  Re-run the command without `--use-live-api` to use the fixture.

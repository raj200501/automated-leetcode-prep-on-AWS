# Step Functions (Local)

This repository ships a local, deterministic state machine that mirrors the AWS
Step Functions flow described in the README. The JSON definition lives in
`state_machine_definition.json` and the runtime orchestration is implemented by
`automated_leetcode_prep.step_functions.run_state_machine`.

## How it runs locally

1. `Scrape` uses the deterministic fixture in `data/fixtures` by default.
2. `LambdaTransform` normalizes the raw payload into a compact schema.
3. `GlueJob` writes JSONL + summary CSV outputs.
4. `AthenaQueries` loads a SQLite database and runs sample queries.
5. `RedshiftLoad` loads a dimensional model into SQLite.
6. `EmrAnalytics` generates metrics in `build/analytics/metrics.json`.

To execute the state machine locally:

```bash
python -m automated_leetcode_prep.cli run
```

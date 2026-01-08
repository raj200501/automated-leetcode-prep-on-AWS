# Amazon Athena (Local Simulation)

The local pipeline uses SQLite to simulate Athena queries. The canonical queries
are stored in `queries.sql` and executed by `automated_leetcode_prep.athena`.

## Running the local Athena step

```bash
python -m automated_leetcode_prep.cli run
```

The results are written to `build/analytics/athena_results.json`.

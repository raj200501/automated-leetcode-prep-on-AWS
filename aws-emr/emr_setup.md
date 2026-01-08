# Amazon EMR (Local Simulation)

The local pipeline ships an EMR-style analytics job implemented in
`automated_leetcode_prep.emr`. It reads normalized problems and emits metrics to
`build/analytics/metrics.json`.

Run it directly:

```bash
python aws-emr/spark_job.py
```

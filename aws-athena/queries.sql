-- Local Athena-compatible queries executed via SQLite in the pipeline
SELECT difficulty, COUNT(*) as problem_count
FROM problems
GROUP BY difficulty;

SELECT slug
FROM problems
WHERE is_paid_only = 0
ORDER BY id
LIMIT 5;

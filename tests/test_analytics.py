import json
import unittest
from pathlib import Path

from automated_leetcode_prep.athena import run_athena
from automated_leetcode_prep.glue_job import load_normalized, run_glue_job
from automated_leetcode_prep.lambda_transformer import run_lambda
from automated_leetcode_prep.redshift import run_redshift
from automated_leetcode_prep.scraper import LeetCodeScraper


class TestAnalytics(unittest.TestCase):
    def test_athena_and_redshift(self) -> None:
        scraper = LeetCodeScraper(Path("data/fixtures"))
        raw_path = Path("build/test/raw/problems.json")
        normalized_path = Path("build/test/normalized/problems.json")
        processed_path = Path("build/test/processed/problems.jsonl")
        summary_path = Path("build/test/processed/summary.csv")
        athena_db = Path("build/test/analytics/athena.db")
        athena_results = Path("build/test/analytics/athena_results.json")
        redshift_db = Path("build/test/analytics/redshift.db")

        raw_path.parent.mkdir(parents=True, exist_ok=True)
        scraper.scrape(raw_path, use_live_api=False)
        run_lambda(raw_path, normalized_path)
        run_glue_job(normalized_path, processed_path, summary_path)

        athena_result = run_athena(processed_path, athena_db, athena_results)
        self.assertEqual(athena_result.queries_run, 2)
        payload = json.loads(athena_results.read_text(encoding="utf-8"))
        self.assertTrue(any("problem_count" in row for row in payload))

        records = load_normalized(normalized_path)
        redshift_result = run_redshift(records, redshift_db)
        self.assertEqual(redshift_result.rows_loaded, 120)


if __name__ == "__main__":
    unittest.main()

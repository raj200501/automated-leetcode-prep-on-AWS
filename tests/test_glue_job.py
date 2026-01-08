import unittest
from pathlib import Path

from automated_leetcode_prep.glue_job import load_normalized, run_glue_job
from automated_leetcode_prep.lambda_transformer import run_lambda
from automated_leetcode_prep.scraper import LeetCodeScraper


class TestGlueJob(unittest.TestCase):
    def test_glue_job_outputs(self) -> None:
        scraper = LeetCodeScraper(Path("data/fixtures"))
        raw_path = Path("build/test/raw/problems.json")
        normalized_path = Path("build/test/normalized/problems.json")
        processed_path = Path("build/test/processed/problems.jsonl")
        summary_path = Path("build/test/processed/summary.csv")
        raw_path.parent.mkdir(parents=True, exist_ok=True)

        scraper.scrape(raw_path, use_live_api=False)
        run_lambda(raw_path, normalized_path)
        result = run_glue_job(normalized_path, processed_path, summary_path)

        self.assertEqual(result.output_count, 120)
        self.assertTrue(processed_path.exists())
        self.assertTrue(summary_path.exists())
        records = load_normalized(normalized_path)
        self.assertIn(records[0].difficulty, {"Easy", "Medium", "Hard"})
        self.assertTrue(summary_path.read_text(encoding="utf-8").startswith("metric,value"))


if __name__ == "__main__":
    unittest.main()

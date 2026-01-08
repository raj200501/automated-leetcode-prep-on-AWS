import unittest
from pathlib import Path

from automated_leetcode_prep.lambda_transformer import run_lambda
from automated_leetcode_prep.scraper import LeetCodeScraper


class TestLambdaTransformer(unittest.TestCase):
    def test_lambda_normalization(self) -> None:
        scraper = LeetCodeScraper(Path("data/fixtures"))
        raw_path = Path("build/test/raw/problems.json")
        normalized_path = Path("build/test/normalized/problems.json")
        raw_path.parent.mkdir(parents=True, exist_ok=True)

        scraper.scrape(raw_path, use_live_api=False)
        result = run_lambda(raw_path, normalized_path)

        self.assertEqual(result.input_count, 120)
        self.assertEqual(result.output_count, 120)
        self.assertTrue(normalized_path.exists())
        payload = normalized_path.read_text(encoding="utf-8")
        self.assertIn("\"slug\"", payload)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path

from automated_leetcode_prep.scraper import LeetCodeScraper


class TestScraper(unittest.TestCase):
    def test_scraper_fixture_count(self) -> None:
        scraper = LeetCodeScraper(Path("data/fixtures"))
        output_path = Path("build/test/raw/problems.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        result = scraper.scrape(output_path, use_live_api=False)

        self.assertEqual(result.source, "fixture")
        self.assertEqual(result.count, 120)
        self.assertTrue(output_path.exists())
        self.assertTrue(output_path.read_text(encoding="utf-8").startswith("["))


if __name__ == "__main__":
    unittest.main()

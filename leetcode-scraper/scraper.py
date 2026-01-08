"""Compatibility wrapper for the local scraper implementation."""

from pathlib import Path

from automated_leetcode_prep.config import PipelineConfig
from automated_leetcode_prep.scraper import LeetCodeScraper


def scrape_leetcode_problems(output_path: str = "build/raw/problems.json") -> str:
    config = PipelineConfig()
    scraper = LeetCodeScraper(config.fixtures_dir)
    result = scraper.scrape(Path(output_path), config.use_live_api)
    return str(result.output_path)


if __name__ == "__main__":
    print(scrape_leetcode_problems())

import json
import unittest
from pathlib import Path

from automated_leetcode_prep.config import PipelineConfig
from automated_leetcode_prep.pipeline import run_pipeline


class TestPipeline(unittest.TestCase):
    def test_pipeline_end_to_end(self) -> None:
        config = PipelineConfig(workspace=Path("build/test"), fixtures_dir=Path("data/fixtures"))
        result = run_pipeline(config)

        self.assertIn("scrape", result.steps_run)
        self.assertTrue(result.artifacts.metrics.exists())

        metrics = json.loads(result.artifacts.metrics.read_text(encoding="utf-8"))
        self.assertEqual(metrics["total_problems"], 120)
        self.assertTrue(metrics["difficulty_breakdown"])


if __name__ == "__main__":
    unittest.main()

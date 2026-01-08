from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

import urllib.request

from automated_leetcode_prep.models import RawProblemRecord

LEETCODE_API_URL = "https://leetcode.com/api/problems/all/"


@dataclass
class ScrapeResult:
    source: str
    count: int
    output_path: Path


class LeetCodeScraper:
    """Fetch problems from LeetCode or local fixtures.

    By default the scraper reads from a fixture to keep the pipeline deterministic.
    """

    def __init__(self, fixtures_dir: Path) -> None:
        self.fixtures_dir = fixtures_dir

    def fetch(self, use_live_api: bool) -> Dict[str, object]:
        if use_live_api:
            return self._fetch_live()
        return self._load_fixture("leetcode_api_response.json")

    def _fetch_live(self) -> Dict[str, object]:
        with urllib.request.urlopen(LEETCODE_API_URL, timeout=30) as response:
            payload = response.read().decode("utf-8")
        return json.loads(payload)

    def _load_fixture(self, name: str) -> Dict[str, object]:
        path = self.fixtures_dir / name
        payload = path.read_text(encoding="utf-8")
        return json.loads(payload)

    def parse(self, payload: Dict[str, object]) -> List[RawProblemRecord]:
        records: List[RawProblemRecord] = []
        stat_status_pairs = payload.get("stat_status_pairs", [])
        for item in stat_status_pairs:
            stat = item.get("stat", {})
            difficulty = item.get("difficulty", {}).get("level", 0)
            difficulty_label = {1: "Easy", 2: "Medium", 3: "Hard"}.get(
                difficulty, "Unknown"
            )
            tags = [tag.get("slug", "") for tag in item.get("topic_tags", [])]
            record = RawProblemRecord(
                id=int(stat.get("question_id", 0)),
                title=str(stat.get("question__title", "")),
                title_slug=str(stat.get("question__title_slug", "")),
                difficulty=difficulty_label,
                paid_only=bool(item.get("paid_only", False)),
                tags=[tag for tag in tags if tag],
            )
            if record.id and record.title:
                records.append(record)
        return records

    def write_raw(self, output_path: Path, records: Iterable[RawProblemRecord]) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = [record.__dict__ for record in records]
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def scrape(self, output_path: Path, use_live_api: bool) -> ScrapeResult:
        payload = self.fetch(use_live_api)
        records = self.parse(payload)
        self.write_raw(output_path, records)
        source = "live_api" if use_live_api else "fixture"
        return ScrapeResult(source=source, count=len(records), output_path=output_path)

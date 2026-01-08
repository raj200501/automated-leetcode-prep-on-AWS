"""Local-friendly Lambda handler used in the deterministic pipeline."""

import json
from pathlib import Path
from typing import Any, Dict

from automated_leetcode_prep.lambda_transformer import normalize_records
from automated_leetcode_prep.models import RawProblemRecord
from automated_leetcode_prep.storage import LocalS3Bucket

DEFAULT_BUCKET_ROOT = Path("build")


def _parse_event(event: Dict[str, Any]) -> list[RawProblemRecord]:
    records = []
    for item in event.get("records", []):
        records.append(
            RawProblemRecord(
                id=int(item["id"]),
                title=str(item["title"]),
                title_slug=str(item["title_slug"]),
                difficulty=str(item["difficulty"]),
                paid_only=bool(item["paid_only"]),
                tags=list(item.get("tags", [])),
            )
        )
    return records


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    bucket_root = Path(event.get("bucket_root", DEFAULT_BUCKET_ROOT))
    bucket = LocalS3Bucket(bucket_root)
    raw_records = _parse_event(event)
    normalized = normalize_records(raw_records)
    payload = json.dumps([record.to_dict() for record in normalized], indent=2)
    stored = bucket.put_text("normalized/problems.json", payload)
    return {
        "statusCode": 200,
        "body": json.dumps({"stored": str(stored.path), "count": len(normalized)}),
    }

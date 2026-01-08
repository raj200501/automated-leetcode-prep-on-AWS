from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class RawProblemRecord:
    """Represents a minimal subset of the LeetCode API payload."""

    id: int
    title: str
    title_slug: str
    difficulty: str
    paid_only: bool
    tags: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class NormalizedProblem:
    """Normalized representation used throughout the pipeline."""

    id: int
    title: str
    slug: str
    difficulty: str
    tags: List[str]
    is_paid_only: bool

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "is_paid_only": self.is_paid_only,
        }

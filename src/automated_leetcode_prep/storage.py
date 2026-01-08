from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class StoredObject:
    key: str
    path: Path


class LocalS3Bucket:
    """A lightweight, file-based stand-in for S3."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def put_file(self, source: Path, key: str) -> StoredObject:
        destination = self.root / key
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != destination.resolve():
            shutil.copyfile(source, destination)
        return StoredObject(key=key, path=destination)

    def put_text(self, key: str, content: str) -> StoredObject:
        destination = self.root / key
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        return StoredObject(key=key, path=destination)

    def list_keys(self) -> Iterable[str]:
        for path in self.root.rglob("*"):
            if path.is_file():
                yield str(path.relative_to(self.root))

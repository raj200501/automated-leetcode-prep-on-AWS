from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from automated_leetcode_prep.models import NormalizedProblem


@dataclass
class AthenaResult:
    db_path: Path
    queries_run: int
    output_path: Path


def load_processed(path: Path) -> List[NormalizedProblem]:
    records: List[NormalizedProblem] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            item = json.loads(line)
            records.append(
                NormalizedProblem(
                    id=int(item["id"]),
                    title=str(item["title"]),
                    slug=str(item["slug"]),
                    difficulty=str(item["difficulty"]),
                    tags=list(item.get("tags", [])),
                    is_paid_only=bool(item.get("is_paid_only", False)),
                )
            )
    return records


def create_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            slug TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            tags TEXT NOT NULL,
            is_paid_only INTEGER NOT NULL
        )
        """
    )
    connection.commit()


def load_into_athena(connection: sqlite3.Connection, records: Iterable[NormalizedProblem]) -> None:
    connection.execute("DELETE FROM problems")
    connection.executemany(
        """
        INSERT INTO problems (id, title, slug, difficulty, tags, is_paid_only)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                record.id,
                record.title,
                record.slug,
                record.difficulty,
                ",".join(record.tags),
                int(record.is_paid_only),
            )
            for record in records
        ],
    )
    connection.commit()


def load_queries(query_path: Path) -> List[str]:
    lines = []
    for line in query_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--"):
            continue
        lines.append(stripped)
    content = "\n".join(lines)
    statements = [statement.strip() for statement in content.split(";") if statement.strip()]
    return statements


def run_queries(
    connection: sqlite3.Connection, queries: Iterable[str]
) -> List[sqlite3.Row]:
    rows: List[sqlite3.Row] = []
    connection.row_factory = sqlite3.Row
    for query in queries:
        cursor = connection.execute(query)
        rows.extend(cursor.fetchall())
    return rows


def write_results(output_path: Path, rows: Iterable[sqlite3.Row]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [dict(row) for row in rows]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_athena(
    processed_path: Path, db_path: Path, output_path: Path, query_path: Path | None = None
) -> AthenaResult:
    records = load_processed(processed_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    query_file = query_path or Path("aws-athena/queries.sql")
    queries = load_queries(query_file)
    with sqlite3.connect(db_path) as connection:
        create_schema(connection)
        load_into_athena(connection, records)
        rows = run_queries(connection, queries)
    write_results(output_path, rows)
    return AthenaResult(db_path=db_path, queries_run=len(queries), output_path=output_path)

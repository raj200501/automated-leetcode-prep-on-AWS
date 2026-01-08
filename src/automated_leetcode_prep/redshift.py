from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from automated_leetcode_prep.models import NormalizedProblem


@dataclass
class RedshiftResult:
    db_path: Path
    rows_loaded: int


def create_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS problem_dimension (
            problem_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            slug TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            is_paid_only INTEGER NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS tag_dimension (
            problem_id INTEGER NOT NULL,
            tag TEXT NOT NULL
        )
        """
    )
    connection.commit()


def load_records(connection: sqlite3.Connection, records: Iterable[NormalizedProblem]) -> int:
    connection.execute("DELETE FROM problem_dimension")
    connection.execute("DELETE FROM tag_dimension")
    problem_rows: List[tuple] = []
    tag_rows: List[tuple] = []
    for record in records:
        problem_rows.append(
            (
                record.id,
                record.title,
                record.slug,
                record.difficulty,
                int(record.is_paid_only),
            )
        )
        for tag in record.tags:
            tag_rows.append((record.id, tag))
    connection.executemany(
        """
        INSERT INTO problem_dimension (problem_id, title, slug, difficulty, is_paid_only)
        VALUES (?, ?, ?, ?, ?)
        """,
        problem_rows,
    )
    connection.executemany(
        "INSERT INTO tag_dimension (problem_id, tag) VALUES (?, ?)",
        tag_rows,
    )
    connection.commit()
    return len(problem_rows)


def run_redshift(records: Iterable[NormalizedProblem], db_path: Path) -> RedshiftResult:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        create_schema(connection)
        rows_loaded = load_records(connection, records)
    return RedshiftResult(db_path=db_path, rows_loaded=rows_loaded)

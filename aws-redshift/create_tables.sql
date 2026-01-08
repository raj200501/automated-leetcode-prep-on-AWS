-- Local Redshift-style schema (SQLite compatible)
CREATE TABLE IF NOT EXISTS problem_dimension (
  problem_id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  slug TEXT NOT NULL,
  difficulty TEXT NOT NULL,
  is_paid_only INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS tag_dimension (
  problem_id INTEGER NOT NULL,
  tag TEXT NOT NULL
);

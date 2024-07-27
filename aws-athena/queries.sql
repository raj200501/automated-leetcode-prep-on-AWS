CREATE DATABASE leetcode_db;

CREATE EXTERNAL TABLE leetcode_db.problems (
    id BIGINT,
    title STRING,
    difficulty STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://leetcode-prep-bucket/processed-problems/';

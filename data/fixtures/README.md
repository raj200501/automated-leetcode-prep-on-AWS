# Fixtures

`leetcode_api_response.json` is a deterministic snapshot that mimics the shape
of the LeetCode API payload. It contains 120 sample problems with predictable
IDs, tags, and difficulties. The pipeline uses it by default to keep tests and
verification reproducible.

If you want to regenerate the fixture, run a script that populates the
`stat_status_pairs` array and ensure the following invariants stay true:

- IDs are unique and sequential.
- Difficulties map to the same Easy/Medium/Hard levels.
- The payload remains valid JSON.

# Amazon S3 (Local Simulation)

The local pipeline uses `automated_leetcode_prep.storage.LocalS3Bucket` to write
files into the `build/` directory. This replaces the need for real S3 buckets
while still keeping object-key semantics.

Example usage:

```python
from automated_leetcode_prep.storage import LocalS3Bucket

bucket = LocalS3Bucket(Path("build"))
bucket.put_text("raw/example.txt", "hello")
```

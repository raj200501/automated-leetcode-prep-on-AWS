COPY problems
FROM 's3://leetcode-prep-bucket/processed-problems/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT_ID:role/redshift-copy-role'
FORMAT AS JSON 'auto';

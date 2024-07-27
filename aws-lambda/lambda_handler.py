import json
import boto3

s3 = boto3.client('s3')
BUCKET_NAME = 'leetcode-prep-bucket'

def lambda_handler(event, context):
    with open('/tmp/problems.json', 'w') as f:
        f.write(json.dumps(event))
    s3.upload_file('/tmp/problems.json', BUCKET_NAME, 'problems/problems.json')
    return {
        'statusCode': 200,
        'body': json.dumps('Problems uploaded to S3 successfully!')
    }

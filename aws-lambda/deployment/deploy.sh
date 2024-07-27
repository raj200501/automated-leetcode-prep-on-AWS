#!/bin/bash

zip -r9 lambda_function.zip .
aws lambda create-function \
    --function-name LeetCodeScraperLambda \
    --zip-file fileb://lambda_function.zip \
    --handler lambda_handler.lambda_handler \
    --runtime python3.8 \
    --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role

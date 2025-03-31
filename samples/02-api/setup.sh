#!/bin/bash

pip install -r requirements.txt

alias awslocal='aws --profile=localstack --endpoint-url=http://localhost:4566'
shopt -s expand_aliases

awslocal s3 mb s3://02-in-bucket
awslocal s3 mb s3://02-out-bucket

awslocal iam create-policy \
    --no-cli-pager \
    --policy-name 02-s3-read-write \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "1",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::02-in-bucket",
                    "arn:aws:s3:::02-in-bucket/*",
                    "arn:aws:s3:::02-out-bucket",
                    "arn:aws:s3:::02-out-bucket/*"
                ],
                "Condition": {
                    "StringEquals": {
                        "s3:ResourceAccount": "000000000000"
                    }
                }
            }
        ]
    }'

awslocal iam list-policies --no-cli-pager

awslocal iam create-role \
    --no-cli-pager \
    --role-name test-inference-role \
    --assume-role-policy-document file://trust-policy.json

awslocal iam attach-role-policy \
    --no-cli-pager \
    --role-name test-inference-role \
    --policy-arn arn:aws:iam::000000000000:policy/02-s3-read-write

awslocal iam list-roles --no-cli-pager
https://docs.localstack.cloud/user-guide/aws/bedrock/

```shell
# list
awslocal bedrock list-foundation-models

# invoke
awslocal bedrock-runtime invoke-model \
    --model-id "meta.llama3-8b-instruct-v1:0" \
    --body '{
        "prompt": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\nSay Hello!\n<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>",
        "max_gen_len": 2,
        "temperature": 0.9
    }' --cli-binary-format raw-in-base64-out outfile.txt

# chat
awslocal bedrock-runtime converse \
    --model-id "ollama.deepseek-r1" \
    --messages '[{
        "role": "user",
        "content": [{
            "text": "Say Hello!"
        }]
    }]'

# create input/output buckets
awslocal s3 mb s3://01-in-bucket
awslocal s3 cp batch_input.jsonl s3://01-in-bucket
awslocal s3 mb s3://01-out-bucket

# invoke model from s3 input
ACCOUNT_ID=123456789012
awslocal bedrock create-model-invocation-job \
  --job-name "my-batch-job" \
  --model-id "mistral.mistral-small-2402-v1:0" \
  --role-arn "arn:aws:iam::$ACCOUNT_ID:role/MyBatchInferenceRole" \
  --input-data-config '{"s3InputDataConfig": {"s3Uri": "s3://01-in-bucket"}}' \
  --output-data-config '{"s3OutputDataConfig": {"s3Uri": "s3://01-out-bucket"}}'

# download the output
JOBNAME=5bad9501
awslocal s3 cp s3://01-out-bucket/$JOBNAME/batch_input.jsonl.out .
```
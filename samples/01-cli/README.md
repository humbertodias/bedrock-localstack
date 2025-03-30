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
awslocal s3 mb s3://in-bucket
awslocal s3 cp batch_input.jsonl s3://in-bucket
awslocal s3 mb s3://out-bucket

# invoke model from s3 input
awslocal bedrock create-model-invocation-job \
  --job-name "my-batch-job" \
  --model-id "mistral.mistral-small-2402-v1:0" \
  --role-arn "arn:aws:iam::123456789012:role/MyBatchInferenceRole" \
  --input-data-config '{"s3InputDataConfig": {"s3Uri": "s3://in-bucket"}}' \
  --output-data-config '{"s3OutputDataConfig": {"s3Uri": "s3://out-bucket"}}'
```
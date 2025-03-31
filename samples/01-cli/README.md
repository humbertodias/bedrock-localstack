https://docs.localstack.cloud/user-guide/aws/bedrock/
https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-mistral-large-2407.html

```shell
# list
awslocal bedrock list-foundation-models


https://ollama.com/library?sort=newest

# invoke
awslocal bedrock-runtime invoke-model \
    --model-id "meta.llama3-8b-instruct-v1:0" \
    --body '{
        "prompt": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\nSay Hello!\n<|eot_id|>\n<|start_header_id|>assistant<|end_header_id|>",
        "max_gen_len": 2,
        "temperature": 0.9
    }' --cli-binary-format raw-in-base64-out outfile.txt


awslocal bedrock-runtime invoke-model \
    --model-id "ollama.deepseek-r1" \
    --body '{"prompt": "Tell me a quick fact about Vienna.", "max_tokens": 100, "temperature": 0.9}' \
    --cli-binary-format raw-in-base64-out outfile.txt

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
ACCOUNT_ID=000000000000
awslocal bedrock create-model-invocation-job \
  --job-name "my-batch-job" \
  --model-id "ollama.deepseek-r1" \
  --role-arn "arn:aws:iam::$ACCOUNT_ID:role/MyBatchInferenceRole" \
  --input-data-config '{"s3InputDataConfig": {"s3Uri": "s3://01-in-bucket"}}' \
  --output-data-config '{"s3OutputDataConfig": {"s3Uri": "s3://01-out-bucket"}}'

JOB_ID=54a34a3f
awslocal bedrock get-model-invocation-job --job-identifier $JOB_ID 

# loop instead of manually wait
while true; do
    STATUS=$(awslocal bedrock get-model-invocation-job --job-identifier $JOB_ID | jq -r '.status')
    echo "Current status: $STATUS"
    if [[ "$STATUS" == "Completed" ]]; then
        echo "Job completed!"
        break
    fi
    sleep 10
done

# download the output
awslocal s3 cp s3://01-out-bucket/$JOB_ID/batch_input.jsonl.out .
```
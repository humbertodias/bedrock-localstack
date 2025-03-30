https://research-it.wharton.upenn.edu/programming/using-aws-bedrocks-batch-api/


Using AWS Bedrock’s Batch API


```shell
./setup.sh
python main.py
```
Flow
```mermaid
sequenceDiagram;
    participant User
    participant Application
    participant S3
    participant Bedrock
    participant FileSystem

    User ->> Application: Run main()
    Application ->> birthplaces: initialize_clients(profile, endpoint)
    Application ->> birthplaces: load_data('famous_people.csv')
    birthplaces -->> Application: DataFrame
    Application ->> birthplaces: create_prompt_file(DataFrame, 'batch_prompts.jsonl')
    Application ->> birthplaces: upload_to_s3(S3, 'batch_prompts.jsonl', '02-in-bucket')
    Application ->> birthplaces: start_batch_job(Bedrock, account_id, 's3://02-in-bucket', 's3://02-out-bucket')
    birthplaces -->> Application: Job ARN
    loop Monitor Job
        Application ->> birthplaces: monitor_job(Bedrock, Job ARN)
        birthplaces -->> Application: Job Status
    end
    Application ->> birthplaces: download_results(S3, '02-out-bucket', Job ARN, output_file)
    Application ->> birthplaces: process_results(DataFrame, output_file)
    birthplaces ->> FileSystem: Save famous_people_with_birthplaces.csv
```

Manual test
```shell
awslocal bedrock create-model-invocation-job \
  --job-name "my-batch-job" \
  --model-id "mistral.mistral-small-2402-v1:0" \
  --role-arn "arn:aws:iam::123456789012:role/MyBatchInferenceRole" \
  --input-data-config '{"s3InputDataConfig": {"s3Uri": "s3://02-in-bucket"}}' \
  --output-data-config '{"s3OutputDataConfig": {"s3Uri": "s3://02-out-bucket"}}'

awslocal bedrock-runtime invoke-model \
--model-id "anthropic.claude-3-5-sonnet-20240620-v1:0" \
--content-type "application/json" \
--accept "application/json" \
--body 'Identify the place of birth for Marilyn Monroe. Format the result like city/country' \
--cli-binary-format raw-in-base64-out outfile.txt

awslocal bedrock-runtime converse \
    --model-id "anthropic.claude-3-5-sonnet-20240620-v1:0" \
    --messages '[{
        "role": "user",
        "content": [{
            "text": "Identify the place of birth for Marilyn Monroe. Only return: City/Country"
        }]
    }]'
```
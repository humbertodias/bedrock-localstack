import helper

# execute setup.sh before
def main():
    profile_name = "localstack"
    endpoint_url = "http://localhost:4566"
    account_id = "000000000000"
    model_id = "mistral.mistral-small-2402-v1:0"
    model_id = "ollama.deepseek-r1"
    # modelId="anthropic.claude-3-5-sonnet-20240620-v1:0"

    s3_client, bedrock = helper.initialize_clients(profile_name, endpoint_url)
    df = helper.load_data('famous_people.csv', 6)
    print("Loaded DataFrame:")
    print(df)

    file_name = helper.create_prompt_file(df, "batch_prompts.jsonl")
    helper.upload_to_s3(s3_client, file_name, "02-in-bucket")

    job_arn = helper.start_batch_job(bedrock, account_id, model_id, "s3://02-in-bucket", "s3://02-out-bucket")
    helper.monitor_job(bedrock, job_arn)

    output_file = f"{job_arn.split('/')[-1]}.jsonl"
    helper.download_results(s3_client, "02-out-bucket", job_arn, output_file)
    helper.process_results(df, output_file)

if __name__ == "__main__":
    main()

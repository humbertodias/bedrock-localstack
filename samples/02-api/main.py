import birthplaces

# execute setup.sh before
def main():
    profile_name = "localstack"
    endpoint_url = "http://localhost:4566"
    account_id = "000000000000"

    s3_client, bedrock = birthplaces.initialize_clients(profile_name, endpoint_url)
    df = birthplaces.load_data('famous_people.csv')
    print("Loaded DataFrame:")
    print(df.head(10))

    file_name = birthplaces.create_prompt_file(df, "batch_prompts.jsonl")
    birthplaces.upload_to_s3(s3_client, file_name, "02-in-bucket")

    job_arn = birthplaces.start_batch_job(bedrock, account_id, "s3://02-in-bucket", "s3://02-out-bucket")
    birthplaces.monitor_job(bedrock, job_arn)

    output_file = f"{job_arn.split('/')[-1]}.jsonl"
    birthplaces.download_results(s3_client, "02-out-bucket", job_arn, output_file)
    birthplaces.process_results(df, output_file)

if __name__ == "__main__":
    main()

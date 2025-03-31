import boto3
import json
import time
import pandas as pd # csv

def create_prompts(df):
    # Create an array of prompts to identify each person's place of birth
    prompts = []

    for index, row in df.iterrows():
        person_name = row['prompt']
        prompt = {
            "recordId": f"{index}",
            "modelInput": {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Identify the place of birth for {person_name}. Format the result like <city/town>,. Do not include any other information."
                            }
                        ]
                    }
                ]
            }
        }
        prompts.append(json.dumps(prompt))
    return prompts

def initialize_clients(profile_name, endpoint_url):
    session = boto3.Session(profile_name=profile_name)
    return session.client('s3', endpoint_url=endpoint_url), session.client('bedrock', endpoint_url=endpoint_url)

def load_data(file_path):
    df = pd.read_csv(file_path)
    return df.iloc[[0]]  # only one for testing

def create_prompt_file(df, file_name):
    prompts = create_prompts(df)
    with open(file_name, 'w') as file:
        for prompt in prompts:
            file.write(f"{prompt}\n")
    return file_name

def upload_to_s3(s3_client, file_name, bucket_name):
    try:
        s3_client.upload_file(file_name, bucket_name, file_name)
        print(f"Uploaded {file_name} to s3://{bucket_name}/{file_name}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        exit(1)


def start_batch_job(bedrock, account_id, input_s3_uri, output_s3_uri):
    input_data_config = {"s3InputDataConfig": {"s3Uri": input_s3_uri}}
    output_data_config = {"s3OutputDataConfig": {"s3Uri": output_s3_uri}}
    try:
        response = bedrock.create_model_invocation_job(
            roleArn=f"arn:aws:iam::{account_id}:role/test-inference-role",
            modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
            jobName=f"my-batch-job-{int(time.time())}",
            inputDataConfig=input_data_config,
            outputDataConfig=output_data_config
        )
        return response.get('jobArn')
    except Exception as e:
        print(f"Error starting inference job: {e}")
        exit(1)


def monitor_job(bedrock, job_arn):
    print("Monitoring batch job...")
    while True:
        job_status_response = bedrock.get_model_invocation_job(jobIdentifier=job_arn)
        status = job_status_response['status']
        if status in ['InProgress', 'Initializing', 'Submitted', 'Validating']:
            print(f"Job {job_arn} is {status}. Waiting for completion...")
            time.sleep(30)
        elif status == 'Completed':
            print(f"Job {job_arn} completed successfully.")
            break
        elif status == 'Failed':
            print(f"Job {job_arn} failed.")
            raise RuntimeError("Job failed.")
        else:
            print(f"Job {job_arn} has unexpected status: {status}")
            time.sleep(30)


def download_results(s3_client, bucket_name, job_arn, output_file):
    output_s3_key = f"{job_arn.split('/')[-1]}/batch_prompts.jsonl.out"
    try:
        s3_client.download_file(bucket_name, output_s3_key, output_file)
        print(f"Downloaded output to {output_file}")
    except Exception as e:
        print(f"Error downloading output file from S3: {e}")
        exit(1)


def process_results(df, output_file):
    birthplaces_list = []
    with open(output_file, 'r') as file:
        for line in file:
            response = json.loads(line)
            output_text = response.get('modelOutput', {})
            birthplaces_list.append(output_text)
    df['Place of Birth'] = birthplaces_list
    df.to_csv('famous_people_with_birthplaces.csv', index=False)

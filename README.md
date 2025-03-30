# Learning

Studying Bedrock functionalities


## LocalStack

start 
```shell
echo 'LOCALSTACK_AUTH_TOKEN=SECRET' > .env
docker compose up -d
```
Take the secret on https://app.localstack.cloud/settings/auth-tokens

awscli
```shell
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

alias
```shell
aws configure --profile localstack <<EOF
test
test
us-east-2
json
EOF

alias awslocal='aws --profile=localstack --endpoint-url=http://localhost:4566'

aws sts get-caller-identity --profile localstack --endpoint-url=http://localhost:4566
```

Then access https://app.localstack.cloud

## JupyterLab

```shell
pip install -U jupyterlab
```

```shell
jupyter-lab --ServerApp.allow_password_change=False
```
Then access http://localhost:8890/lab


## References
* [bedrock]()
* [jupyter](https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html)
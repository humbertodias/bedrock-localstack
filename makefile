UID := $(shell id -u)
GID := $(shell id -g)

export UID GID

up:
	docker compose up -d
	@echo "Access https://app.localstack.cloud"
	
down:
	docker compose down

aws-configure:
	@echo -e "test\ntest\nus-east-2\njson" | aws configure --profile localstack

clean:
	rm -rf ./localstack ./localstack-data

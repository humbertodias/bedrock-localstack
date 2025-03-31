UID := $(shell id -u)
GID := $(shell id -g)

export UID GID

up:
	docker compose up -d
	@echo "Access https://app.localstack.cloud"
	
down:
	docker compose down

clean:
	rm -rf ./localstack ./localstack-data

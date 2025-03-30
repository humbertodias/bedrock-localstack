UID := $(shell id -u)
GID := $(shell id -g)

export UID GID

up:
	docker compose up -d
	
down:
	docker compose down

clean:
	rm -rf ./localstack ./localstack-data

.PHONY: docker-build docker-run-server docker-run-consumer docker-run

CONFIG ?= ./config/local.yaml

SERVER_PORTS ?= 50051:50051

docker-build:
	docker build -t agreements-generator-worker .

docker-run:
	docker run --env-file .env --rm -p ${SERVER_PORTS} --name agreements-generator-server -v $(CONFIG):/app/config/config.yaml agreements-generator-worker

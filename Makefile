.PHONY: docker-build docker-run-server docker-run-consumer

CONFIG ?= ./config/local.yaml

SERVER_PORTS ?= 50051:50051

docker-build:
	docker build -t agreements-generator-worker .

docker-run-server:
	docker run --env-file .env -p ${SERVER_PORTS} --rm --name agreements-generator-server -v $(CONFIG):/app/$(CONFIG) agreements-generator-worker

docker-run-consumer:
	docker run --env-file .env --rm --name agreements-generator-server -v $(CONFIG):/app/$(CONFIG) agreements-generator-worker cmd.consumer.main

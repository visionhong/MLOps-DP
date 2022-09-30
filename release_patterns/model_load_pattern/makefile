DOCKER_REPOSITORY := tjems6498/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
IMAGE_VERSION := 0.0.1

MODEL_LOAD_PATTERN := model_load_pattern
MODEL_LOAD_PATTERN_PORT := 8000
MODEL_LOADER := model_loader

.PHONY: build_api
build_api:
	docker build \
	--platform=linux/amd64 \
	-t $(DOCKER_REPOSITORY):$(MODEL_LOAD_PATTERN)_api_$(IMAGE_VERSION) \
	-f $(DOCKERFILE) \
	.

.PHONY: push_api
push_api:
	docker push $(DOCKER_REPOSITORY):$(MODEL_LOAD_PATTERN)_api_$(IMAGE_VERSION)

.PHONY: build_loader
build_loader:
	docker build \
	--platform=linux/amd64 \
	-t $(DOCKER_REPOSITORY):$(MODEL_LOAD_PATTERN)_loader_$(IMAGE_VERSION) \
	-f $(MODEL_LOADER)/$(DOCKERFILE) \
	.

.PHONY: push_loader
push_loader:
	docker push $(DOCKER_REPOSITORY):$(MODEL_LOAD_PATTERN)_loader_$(IMAGE_VERSION)

.PHONY: build_all
build_all: build_api build_loader

.PHONY: push_all
push_all: push_api push_loader

.PHONY: deploy
deploy:
	kubectl apply -f manifests/namespace.yaml
	kubectl apply -f manifests/deployment.yaml

.PHONY: delete
delete:
	kubectl delete ns model-load

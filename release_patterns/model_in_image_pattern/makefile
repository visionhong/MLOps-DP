DOCKER_REPOSITORY := tjems6498/ml-system-in-actions

ABSOLUTE_PATH := $(shell pwd)

DOCKERFILE := Dockerfile
IMAGE_VERSION := 0.0.1

MODEL_IN_IMAGE_PATTERN := model_in_image_pattern
MODEL_IN_IMAGE_PATTERN_PORT := 8000
NAMESPACE :=  model-in-image


.PHONY: build
build:
		docker build \
		--platform=linux/amd64 \
		-t $(DOCKER_REPOSITORY):$(MODEL_IN_IMAGE_PATTERN)_$(IMAGE_VERSION) \
		-f $(DOCKERFILE) \
		.

.PHONY: push
push:
	docker push $(DOCKER_REPOSITORY):$(MODEL_IN_IMAGE_PATTERN)_$(IMAGE_VERSION)

.PHONY: deploy
deploy:
		kubectl apply -f manifests/namespace.yaml
		kubectl apply -f manifests/deployment.yaml

.PHONY: delete
delete:
		kubectl delete ns $(NAMESPACE)

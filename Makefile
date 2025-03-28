.PHONY: install run docker-build docker-run docker-build-k8s helm-deploy helm-uninstall helm-repo

# If running `make` without arguments, it will run the `help` target
.DEFAULT_GOAL := help

# Define variables
IMAGE_NAME=ghcr.io/kairoaraujo/cowservice:latest
APP=cowservice
CHART_PATH=./charts/cowservice

install-deps:  ## Install dependencies
	pip install -r requirements.txt


dev-run:  ## Run the application in development mode
	uvicorn main:app --reload

docker-build:  ## Build Container image
	docker build -t $(IMAGE_NAME) .

docker-run:  ## Run Container image
	docker run -p 8000:8000 $(IMAGE_NAME)


tuf:  ## 🔐 TUF Verification of the Helm Chart Dependencies
	@rstuf artifact repository set cowservice-3rdp-sw
	@helm show values ./charts/cowservice | yq '. | .. | select(has("repository") and has("tag")) | .repository + ":" + .tag' | grep -v cowservice | xargs -I {} rstuf artifact download {}

deploy:  ## Deploy the application to Kubernetes
	@MAKE tuf
	helm upgrade --install $(APP) $(CHART_PATH)

helm-update:
	@MAKE tuf
	helm upgrade --install $(APP) $(CHART_PATH)

helm-uninstall:  ## 🚨 Delete the application from Kubernetes
	helm delete $(APP)

helm-repo:  ## Add and update Helm repo
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo update

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
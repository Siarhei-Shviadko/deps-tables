# Place your local stuff in Makefile.local
-include .env
-include vendors/deps-pipelines/shared/Makefile
-include Makefile.local
helm_upgrade_timeout := $(or $(HELM_UPGRADE_TIMEOUT), 300s)

CURRENT_UID := $(shell id -u):$(shell id -g)
APP_NAME := tables
HASH=$(shell git rev-parse HEAD)
TAG=$(shell git describe || echo "latest")
BUILD_DATE=$(shell date)
commit_short_sha := "$(CI_COMMIT_SHORT_SHA)"

NO_DEV_DOCKER_IMAGE = tables
DEV_DOCKER_IMAGE = tables-dev


.PHONY: config
## Show current docker compose config
config:
	docker compose -f docker-compose.yml config

.PHONY: config-test
## Show docker compose test config
config-test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml config

.PHONY: install
## Install default environment settings
install:
	cp .env.example .env

.PHONY: login
## Login in docker registry
login:
	docker login $(repository)

.PHONY: prereq
prereq:
	test -f .env || echo >> .env
	docker network create deps-network || true

.PHONY: prereq-tests
prereq-tests: | prereq
	docker compose -f docker-compose.yml -f docker-compose.test.yml down -v

.PHONY: run
## Run service
run: | prereq
	docker compose up -d

.PHONY: logs
## Open service logs
logs:
	docker compose logs -f

.PHONY: status
## Get running status information
status:
	docker compose ps

.PHONY: stop
## Stop runned services
stop:
	docker compose stop

.PHONY: build
## Build containers
build:
	docker compose build \
	--build-arg BUILD_HASH=$(HASH) \
	--build-arg BUILD_TAG=$(TAG) \
	--build-arg BUILD_DATE="$(BUILD_DATE)"

.PHONY: shell-app
## Open shell in Table API container
shell-app:
	docker compose exec -u root $(APP_NAME) /bin/sh

.PHONY: poetry-shell
## Open shell for installing dependencies
poetry-shell:
	docker compose run --rm $(APP_NAME) /bin/bash

.PHONY: format
## Apply black & isort code formatting
format:
	docker compose run --rm --no-deps -u "$(CURRENT_UID)" $(APP_NAME) black --config pyproject.toml .
	docker compose run --rm --no-deps -u "$(CURRENT_UID)" $(APP_NAME) isort --settings-path /app/setup.cfg .

.PHONY: format-check
## Check for correct code format
format-check:
	docker compose run --rm --no-deps -u "$(CURRENT_UID)" $(APP_NAME) black --config pyproject.toml --check .
	docker compose run --rm --no-deps -u "$(CURRENT_UID)" $(APP_NAME) isort --settings-path /app/setup.cfg --check-only .

.PHONY: lint
## Check code using linters
lint:
	docker compose run --rm --no-deps $(APP_NAME) flake8 .

.PHONY: mypy
## Check code using mypy
mypy:
	docker compose run --rm --no-deps $(APP_NAME) mypy .

.PHONY: tests-unit
## Run unit tests
tests-unit:
	docker compose -f docker-compose.yml -f docker-compose.test.yml run --user="root" --rm --no-deps $(APP_NAME) coverage run -a -m pytest -vvv tests/unit

.PHONY: tests-integration
## Run integration tests
tests-integration:
	docker compose -f docker-compose.yml -f docker-compose.test.yml rm -f
	docker compose -f docker-compose.yml -f docker-compose.test.yml up -d test-rabbitmq
	docker compose -f docker-compose.yml -f docker-compose.test.yml run --user="root" --rm $(APP_NAME) coverage run -a -m pytest tests/integration
	docker compose -f docker-compose.yml -f docker-compose.test.yml rm -f

.PHONY: tests
## Run unit & integration tests
tests:
	docker compose -f docker-compose.yml -f docker-compose.test.yml rm -f
	docker compose -f docker-compose.yml -f docker-compose.test.yml up -d test-rabbitmq
	docker compose -f docker-compose.yml -f docker-compose.test.yml run --user="root" --rm $(APP_NAME) coverage run -a -m pytest -vv -x --junitxml=junit-report.xml tests/unit tests/integration
	docker compose -f docker-compose.yml -f docker-compose.test.yml rm -f

.PHONY: coverage
## Get code coverage report
coverage:
	docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm $(APP_NAME) coverage report -i --rcfile=/app/setup.cfg

.PHONY: coverage-xml
## Generate xml coverage report
coverage-xml:
	docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm $(APP_NAME) coverage xml -i --rcfile=/app/setup.cfg -o /app/tests/coverage.xml

.PHONY: ci
## Run CI checks
ci: | prereq-tests format-check lint mypy tests coverage prereq-tests
	@if [ "$(version)" == "ci" ]; then \
		make coverage-xml;\
	else \
	  	make requirements-lock; \
	fi


.PHONY: build-prod
## Build images for production
build-prod:
	$(call build_service,tables-dev,./etc/deps-tables/Dockerfile,,develop)
	$(call build_service,tables,./etc/deps-tables/Dockerfile,,,tables-dev)


.PHONY: push
## Push images to registry
push:
	$(call push_service,tables)
	$(call push_service,tables-dev)

.PHONY: deliver
## Build prod images and push to registry
deliver: | build-prod push

.PHONY: tag
## Retag built services
tag:
	$(call tag_service,tables)
	$(call tag_service,tables-dev)

.PHONY: pull
## Pull service images from docker registry
pull:
	$(call pull_service,tables)
	$(call pull_service,tables-dev)

.PHONY: helm-upgrade-service
helm-upgrade-service:
	helm upgrade --install $(CI_PROJECT_NAME) .helm/services \
		--values .helm/services/values.yaml $(ADDITIONAL_VALUES) \
		--set registry=$(REPOSITORY_URL) \
		--set tables.image.tag=$(commit_short_sha) \
		--set tables_consumer.image.tag=$(commit_short_sha) \
        --set vault_settings.enabled=$(VAULT_ENABLE) \
		--timeout $(helm_upgrade_timeout) \
		--atomic \
		--wait \
		--debug \
		--namespace $(NAMESPACE)

.PHONY: helm-upgrade
helm-upgrade:
	make helm-upgrade-service

.PHONY: helm-deployment-rollback
helm-deployment-rollback:
	helm rollback --namespace $(NAMESPACE) $(CI_PROJECT_NAME) 0

.PHONY: helm-rollback
helm-rollback:
	make helm-deployment-rollback

testdkube := $(shell kubectl config current-context)
ifeq ($(testdkube), rancher-desktop)
.PHONY: skaffold
skaffold:
	cd skaffold && skaffold run -f skaffold.yaml
endif

.PHONY: build-no-dev
build-no-dev:
	$(call build_service,$(NO_DEV_DOCKER_IMAGE),./etc/deps-tables/Dockerfile,,build,$(DEV_DOCKER_IMAGE))

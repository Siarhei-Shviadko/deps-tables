# DEPS Tables service 

### Description
Table detection and extraction service


## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.


## Local development

### Building service
```bash
# Setup environment variables for run
make install

# Fill required variables in .env file. 
# Actual information about variables could be found at KB onboarding page
make build
```

### Getting started
Before we get started make sure you've updated all project dependencies:
```console
git submodule update --init --recursive
make install
```
Login to docker registry (default is `${REPOSITORY_URL}` and your epam creds)
Then you need to build project containers for development:
```console
make build
```

Apply db migrations:
```console
make migrate
```

Run project containers
```console
make run
```

### Useful commands

Get logs:
```console
make logs
```

Run service by `make run` command and open Swagger documentation at `http://localhost:5020/api/tables/docs`

Stop containers:
```console
make stop
```
>>>>>>> 72d561c (Update documentation)

Run ci tests:
```console
make ci
```

Format code:
```console
make format
```

List of all available commands are available by running

```console
make help
```

### Commit rules

* Use Jira task number in commits.
Example: "[322] do something"


### Troubleshooting

#### _pickle.UnpicklingError: invalid load key, 'v'.

This error means that you need to download models with [Git LFS](https://git-lfs.github.com/).
Install it and run these commands:

```console
git lfs install
git lfs pull
```

You can check that models have been downloaded:

```console
cd etc/deps-tables/models
ls -hl *
```
```console
-rw-r--r--  1 user  staff   460M Jul 19 18:20 detectron_columns_model.pth
-rw-r--r--  1 user  staff   460M Jul 19 18:20 detectron_tables_model.pth

yolo:
total 524440
-rw-r--r--  1 user  staff    12K Jul 19 16:41 yolo-obj.cfg
-rw-r--r--  1 user  staff   244M Jul 19 18:20 yolo-obj_6000.weights
```

Note the size of files: it should be several hundreds of megabytes.

### Run locally using skaffold 
 Make sure that deps-infra (postgres, redis, rabbitmq is up) is up and running

# !Note make sure that context is rancher-desktop
```bash 
kubectl config current-context 
```

Do the following commands

```bash
make skaffold
```

## Enabling/Disabling vault usage
You can enable or disable vault secret usage without modifying kubernetes yaml files. By default vault usage is set to false inside value.yaml file but we override this value with VAULT_ENABLE_DEV, VAULT_ENABLE_QA, VAULT_ENABLE_INS, VAULT_ENABLE_DEMO, VAULT_ENABLE_DS variables from Settings >> CI/CD for each environment. If you change variable value from Settings >> CI/CD you need to manually start new pipline from CI/CD >> Pipelines.

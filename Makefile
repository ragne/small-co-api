SHELL = /bin/bash
.DEFAULT_GOAL := help
PRODUCT=small-co-api
MASTER_TAG=main
TAG?=${MASTER_TAG}


# adjusted for having mkfile_dir to contain abspath to dir in which makefile lies https://stackoverflow.com/a/18137056
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir := $(abspath $(dir $(mkfile_path)))

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean:
	-rm -r build dist .eggs *.egg-info
	-rm -r .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -r {} +
	@find . -type d -name '__pycache__' -exec rm -r {} +
	@find . -type d -name '*pytest_cache*' -exec rm -r {} +
	@find . -type f -name "*.py[co]" -exec rm -r {} +

.venv: ## Inits venv with poetry you have to specify python environment to use beforehand, see poetry docs
	@poetry install
	@echo 'Assumes AWS API access for linting and updating, and that work would be done in a virtual env'


fmt: .venv
	poetry run black --exclude '.venv/' api/


build:
	@poetry build

moto_server: .venv  ## Runs a moto_server for dev mode
	poetry run moto_server --port 8000

run: .venv  ## Runs app in dev mode against moto_server
	S3_BUCKET='test' FLASK_ENV=development FLASK_APP=api.app poetry run flask run

run_prod: .venv  ## Runs app in prod mode, which is suitable for light prod usage
	# see https://flask.palletsprojects.com/en/2.0.x/tutorial/deploy/
	# https://docs.pylonsproject.org/projects/waitress/en/latest/
	@poetry run waitress-serve api.app:app

docker_build:
	docker build -t ${REGISTRY}/${PRODUCT}:${TAG} .

docker_push: docker_build
	docker push ${REGISTRY}/${PRODUCT}:${TAG}
	docker rmi ${REGISTRY}/${PRODUCT}:${TAG}

docker_run:
	docker run --rm --name ${PRODUCT} -p 8080:8080 -d ${REGISTRY}/${PRODUCT}:${TAG}

docker_stop:
	docker rm -vf ${PRODUCT} || :

publish: docker_build docker_push
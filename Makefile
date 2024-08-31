##################
###   INSTALL  ###
.PHONY: install
install: ## Install the poetry environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@poetry run pre-commit install
	@poetry shell

##################
##  PRECOMMIT  ###
.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry check --lock"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy recommend_app/
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry recommend_app/

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest

##################
#####  DOCS  #####
.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@poetry run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@poetry run mkdocs serve

##################
##### DOCKER #####
.PHONY: dbuild
dbuild: ## Build a docker container
	@docker build -t praveen/recommend-app .

.PHONY: drun
drun: ## Run the docker container
	@docker run --rm -it praveen/recommend-app

##################
#####  RUN   #####
.PHONY: run
run: ## Run the app locally
	@poetry run py -m recommend_app

##################
#####  HELP  #####
.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

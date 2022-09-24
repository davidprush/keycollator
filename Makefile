#* Variables
#* SHELL := /usr/bin/env bash
#*pwd := `pwd`
########################################################################################
# Targets for managing the Devstack repo itself.
########################################################################################

# Generates a help message. Borrowed from https://github.com/pydanny/cookiecutter-djangopackage.
help: ## Display this help message.
	@echo "Please use \`make <target>' where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-28s\033[0m %s\n", $$1, $$2}' Makefile | sort

.PHONY: run
run:
	python3 src/keycollator.py --limit-result=30

.PHONY: setup
setup: requirements.txt
	python3 -m pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf src/__pycache__

.PHONY: push
push:
	git add .
	git commit -m "$(filter-out $@, $(msg))"
	git push

.PHONY: venv
venv:
	./make-venv.sh

.PHONY: upgrade
upgrade:
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine
	python3 -m pip install --upgrade -r requirements.txt

.PHONY: build
build:
	python3 -m pip install --upgrade build
	python3 -m pip install -r requirements.txt
	python3 -m build

.PHONY: pypi
pypi:
	python3 setup.py sdist
	twine upload --skip-existing dist/*

.PHONY: setup
setup:
	python3 setup.py sdist

.PHONY: punkt
punkt:
	python3 -m pip install nltk
	python3 -m nltk.downloader punkt

.PHONY: alias
alias:
	# Create aliases for python and pip to use python3 and pip3 respectively
	# alias myenv=source venv/bin/activate
	# alias py=venv/bin/python3
	# sed '' 's/abc/myenv/g' ~/.zshrc
	# sed '' 's/abc/'alias myenv=source venv/bin/activate'/g' ~/.zshrc



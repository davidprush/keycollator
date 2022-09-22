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

run:
	python3 src/keycollator.py --set-logging --limit-results=30

setup: requirements.txt
	pip3 install -r src/requirements.txt

clean:
	rm -rf src/__pycache__

push:
	git add .
	git commit -m "$(filter-out $@, $(msg))"
	git push

venv:
	./make-venv.sh

upgrade:
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine

build:
	python3 -m pip install --upgrade build
	python3 -m build

pypi:
	python setup.py sdist
	twine upload --skip-existing dist/*

setup:
	python setup.py sdist

punkt:
	pip3 install nltk
	python3 -m nltk.downloader punkt

alias:
	# Create aliases for python and pip to use python3 and pip3 respectively
	# alias myenv=source venv/bin/activate
	# alias py=venv/bin/python3
	# sed '' 's/abc/myenv/g' ~/.zshrc
	# sed '' 's/abc/'alias myenv=source venv/bin/activate'/g' ~/.zshrc



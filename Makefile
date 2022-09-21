#* Variables
#* SHELL := /usr/bin/env bash
#*pwd := `pwd`

run:
	python3 src/keycollator.py -l

setup: requirements.txt
	pip3 install -r requirements.txt

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
	python3 -m build

pypi:
	python setup.py sdist
	twine upload --skip-existing dist/*

setup:
	python setup.py sdist


run:
	python3 ./src/keycollator.py -l -v

setup: requirements.txt
	pip3 install -r requirements.txt

clean:
	rm -rf ./src/__pycache__

push:
	git add .
	git commit -m "$(filter-out $@, $(msg))"
	git push

env:
	source ./venv/bin/activate

upgrade:
	python3 -m pip install --upgrade build
	python3 -m pip install --upgrade twine

build:
	python3 -m build

pypi:
	python3 -m twin upload dist/*
	

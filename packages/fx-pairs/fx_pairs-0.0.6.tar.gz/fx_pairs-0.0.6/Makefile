# Makefile
SHELL = /bin/bash

.RECIPEPREFIX = +

# Styling
.PHONY: style
style:
+ black .
+ flake8 .
+ python3 -m isort .
+ pyupgrade

# Cleaning
.PHONY: clean
clean: style
+ find . -type f -name "*.DS_Store" -ls -delete
+ find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
+ find . | grep -E ".pytest_cache" | xargs rm -rf
+ find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
+ rm -rf .coverage*

.PHONY: test
test:
+ pytest ./

.PHONY: dev-install
dev-install:
+ pip install -e ./

.PHONY: build
build:
+ python3 -m build

.PHONY: upload
upload:
+ python3 -m twine upload dist/*

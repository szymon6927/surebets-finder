.DEFAULT_GOAL := all

isort:
	poetry run isort .

black:
	poetry run black .

flake8:
	poetry run flake8 .

mypy:
	poetry run mypy surebets_finder

test:
	poetry run pytest

lint: isort black flake8 mypy

all: isort black mypy flake8 test

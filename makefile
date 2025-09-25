SHELL := bash
.ONESHELL:
.SHELLFLAGS := -ecx
PYTHON := python3

env:
	pipenv install --dev
	pipenv shell

setup:
	pipenv install --dev

run: setup
	pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Virtual env is created here: ~/.local/share/virtualenvs
clean:
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf .pytest_cache
	pipenv --rm

clean-all: clean
	rm -rf Pipfile.lock
.PHONY: lint format

lint:
	@echo "Running Flake8..."
	flake8

format:
	@echo "Running isort and Black..."
	isort .
	black .

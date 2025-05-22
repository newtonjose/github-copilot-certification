.PHONY: test

test:
	PYTHONPATH=src pytest --cov=src --cov-report=html

report:
	python -m http.server --directory htmlcov

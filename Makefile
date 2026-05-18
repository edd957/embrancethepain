.PHONY: bootstrap test lint typecheck run-api train evaluate drift clean

bootstrap:
	infrasentinel generate-data --rows 6000
	infrasentinel train
	infrasentinel evaluate

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy src

run-api:
	uvicorn infrasentinel_ai.api.main:app --host 0.0.0.0 --port 8000 --reload

train:
	infrasentinel train

evaluate:
	infrasentinel evaluate

drift:
	infrasentinel drift-report

clean:
	python -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', '.ruff_cache', '.mypy_cache', 'htmlcov']]"

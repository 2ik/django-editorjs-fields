.PHONY: test lint format lock install server clean dj6 dj52 dj50 dj42 dj32

PYTHON ?= poetry run

test:
	$(PYTHON) pytest tests/ -v --tb=short

lint:
	$(PYTHON) ruff check django_editorjs_fields/ tests/

format:
	$(PYTHON) ruff check --fix django_editorjs_fields/ tests/

lock:
	poetry lock --no-interaction

install:
	poetry install --no-interaction

server:
	cd example && python manage.py runserver

dj6:
	pip install "Django>=6.0,<7.0" && @echo "Django $$(python -c 'import django; print(django.__version__)')" installed

dj52:
	pip install "Django>=5.2,<6.0" && @echo "Django $$(python -c 'import django; print(django.__version__)')" installed

dj50:
	pip install "Django>=5.0,<5.1" && @echo "Django $$(python -c 'import django; print(django.__version__)')" installed

dj42:
	pip install "Django>=4.2,<5.0" && @echo "Django $$(python -c 'import django; print(django.__version__)')" installed

dj32:
	pip install "Django>=3.2,<4.0" && @echo "Django $$(python -c 'import django; print(django.__version__)')" installed

clean:
	rm -rf .pytest_cache .tox __pycache__ tests/__pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true

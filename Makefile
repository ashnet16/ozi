.PHONY: format lint test type-check check proto clean-proto build-duckdb duckdb install-requirements run-consumer clean-docker init-db build-analytics run-analytics dev help clone-consumers

# Clone consumers folder into analytics/
clone-consumers:
	@echo "Cloning consumers/ into analytics/"
	@cp -r consumers /Users/ashleymitchell/Desktop/ozi/ozi/analytics/

# ------------
# Developer Commands
# ------------

format:
	poetry run black consumers producers rag llm
	poetry run isort consumers producers rag llm

lint:
	poetry run flake8 consumers producers rag llm

test:
	poetry run pytest

type-check:
	poetry run mypy .

check: format lint type-check

# ------------
# Docker/Analytics Commands
# ------------

build-duckdb:
	docker build -t ozi-duckdb .

duckdb:
	docker run -it --rm -v $$(pwd)/analytics/duckdb_data:/data ozi-duckdb /data/ozi.duckdb

install-requirements:
	pip install -r requirements.txt

run-consumer:
	python -m analytics.consumer

clean-docker:
	docker rmi -f ozi-duckdb || true
	docker rmi -f ozi-analytics || true

init-db:
	python analytics/init_db.py

build-analytics:
	docker build -f analytics/Dockerfile -t ozi-analytics .

run-analytics:
	docker run -it --rm -v $$(pwd)/analytics/duckdb_data:/app/duckdb_data ozi-analytics

dev: build-analytics run-analytics

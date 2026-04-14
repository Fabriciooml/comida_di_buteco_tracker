DB     ?= butecos.db
PYTHON ?= .venv/bin/python

.PHONY: help install install-frontend test run-api dev-frontend \
        scrape scrape-dry-run migrate geocode regeocode \
        parse-hours parse-food parse build-frontend clean

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ────────────────────────────────────────────────────────────────────

install: ## Install Python dependencies (uv)
	uv pip install -r requirements.txt

install-frontend: ## Install Node dependencies
	cd frontend && npm install

# ── Development ──────────────────────────────────────────────────────────────

run-api: ## Start FastAPI server on :8000 (with reload)
	uv run uvicorn api.main:app --reload

dev-frontend: ## Start Vite dev server on :5173
	cd frontend && npm run dev

# ── Testing ──────────────────────────────────────────────────────────────────

test: ## Run all Python tests
	pytest

# ── Data pipeline ────────────────────────────────────────────────────────────

scrape: ## Scrape bars into DB (DB=butecos.db)
	$(PYTHON) main.py --db $(DB)

scrape-dry-run: ## Scrape bars and print to stdout (no DB write)
	$(PYTHON) main.py --dry-run

migrate: ## Run all DB migrations in order (idempotent)
	$(PYTHON) -m migrations.migrate --db $(DB)
	$(PYTHON) -m migrations.migrate_coords $(DB)
	$(PYTHON) -m migrations.migrate_hours --db $(DB)
	$(PYTHON) -m migrations.migrate_food_attributes --db $(DB)

geocode: ## Add lat/lon to bars via Nominatim (DB=butecos.db)
	$(PYTHON) -m pipeline.geocode $(DB)

regeocode: ## Re-geocode existing bars with improved structured query (DB=butecos.db)
	$(PYTHON) -m migrations.regeocode --db $(DB)

parse-hours: ## Re-parse working_hours → bar_hours table (DB=butecos.db)
	$(PYTHON) -m migrations.migrate_hours --db $(DB)

parse-food: ## Re-classify food category/vegan/vegetarian (DB=butecos.db)
	$(PYTHON) -m migrations.migrate_food_attributes --db $(DB)

parse: parse-hours parse-food ## Run all parsers against DB (DB=butecos.db)

# ── Frontend build ───────────────────────────────────────────────────────────

build-frontend: ## Build Vue app to frontend/dist/
	cd frontend && npm run build

# ── Housekeeping ─────────────────────────────────────────────────────────────

clean: ## Remove build artifacts (__pycache__, .pytest_cache, frontend/dist)
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
	rm -rf .pytest_cache frontend/dist

# ── Docker ───────────────────────────────────────────────────────────────────

docker-build: ## Build Docker image
	docker compose build

docker-up: ## Start app in Docker (detached)
	docker compose up -d

docker-down: ## Stop Docker containers
	docker compose down

docker-logs: ## Follow Docker logs
	docker compose logs -f

docker-import-db: ## Copy local butecos.db into Docker volume
	docker compose run --rm -v $(PWD)/butecos.db:/tmp/butecos.db app \
		cp /tmp/butecos.db /app/data/butecos.db

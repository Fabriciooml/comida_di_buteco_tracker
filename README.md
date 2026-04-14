# Comida di Buteco Tracker

Interactive map of bars participating in the annual [Comida di Buteco](https://comidadibuteco.com.br) contest in Belo Horizonte, Brazil.

The app scrapes bar data (name, address, featured dish, dietary attributes, opening hours) from the contest website, geocodes addresses, and displays everything on a Leaflet map with a searchable sidebar.

## Tech stack

- **Backend:** Python 3.12, FastAPI, SQLite
- **Frontend:** Vue 3, Vite, Leaflet.js / OpenStreetMap
- **Scraping:** Playwright (headless Chromium), BeautifulSoup4
- **DevOps:** Docker, Makefile

## Prerequisites

- Python 3.12+
- Node 20+
- [uv](https://github.com/astral-sh/uv)
- Docker (optional, for containerized runs)

## Setup

```bash
make install           # Python deps (uv)
make install-frontend  # Node deps
uv run playwright install chromium  # Playwright browser
```

## Data pipeline

Run these in order to populate the database:

```bash
make scrape    # Scrape bars from comidadibuteco.com.br into butecos.db
make migrate   # Apply DB schema migrations
make geocode   # Add lat/lon via Nominatim
```

To preview scraped data without writing to the DB:

```bash
make scrape-dry-run
```

## Running locally

```bash
make run-api        # FastAPI server → http://localhost:8000
make dev-frontend   # Vite dev server → http://localhost:5173
```

The Vue app proxies `/api/*` to port 8000 in dev mode.

## Running with Docker

```bash
make docker-build       # Build image
make docker-import-db   # Seed butecos.db into the Docker volume
make docker-up          # Start app → http://localhost:8000
make docker-logs        # Follow logs
make docker-down        # Stop containers
```

## Testing

```bash
make test
```

## Project layout

```
├── main.py               # Scraper CLI entry point
├── scraper.py            # Playwright async crawler
├── db.py                 # SQLite schema & data access
├── models.py             # Bar dataclass
├── geocode.py            # Nominatim geocoding
├── address_parser.py     # Address field extraction
├── food_classifier.py    # Dietary attribute classification
├── hours_parser.py       # Opening hours parsing
├── migrate*.py           # DB schema migrations
├── api/
│   ├── main.py           # FastAPI app (serves frontend + API)
│   └── routers/bars.py   # GET /api/bars
├── frontend/
│   └── src/
│       ├── App.vue
│       └── components/   # BarMap, BarDrawer, BarDialog, BarLocationPicker
└── tests/
```

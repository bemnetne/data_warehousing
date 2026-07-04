# Medical Data Warehouse Pipeline

An end-to-end ELT pipeline that collects data from Ethiopian medical Telegram channels, transforms it into an analytical data warehouse, enriches it using computer vision, exposes insights through a REST API, and automates the entire workflow using Dagster.

---

## Project Overview

The project consists of five main stages:

1. Telegram Data Scraping
2. Data Warehouse Development (PostgreSQL + dbt)
3. Image Enrichment using YOLOv8
4. Analytical API using FastAPI
5. Pipeline Orchestration using Dagster

---

## Project Structure

```text
.
├── api/
├── data/
│   ├── raw/
│   └── processed/
├── logs/
├── medical_warehouse/
├── pipeline/
├── scripts/
├── src/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python 3.11+
- Docker Desktop
- PostgreSQL
- dbt Core
- FastAPI
- Dagster
- Telegram API Credentials

---

## Installation

Clone the repository

```bash
git clone <repository-url>

cd data_warehousing
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
TG_API_ID=xxxxxxxx
TG_API_HASH=xxxxxxxx
PHONE_NUMBER=+251xxxxxxxx

DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_db
DB_USER=postgres
DB_PASSWORD=password
```

---

# Running the Project

## Start PostgreSQL

```bash
docker compose up -d
```

Verify the container is running

```bash
docker ps
```

---

#  Telegram Data Scraping

Run the scraper

```bash
python -m scripts.scrape_telegram
```

This will:

- Download Telegram messages
- Download channel images
- Store JSON files under `data/raw/telegram_messages`
- Store images under `data/raw/images`

---

# Data Warehouse

### Load raw Telegram data

```bash
python -m scripts.load_raw_to_postgres
```

### Build the warehouse

```bash
cd medical_warehouse

dbt build
```

### Run dbt tests

```bash
dbt test
```

### Generate documentation

```bash
dbt docs generate
```

### View documentation

```bash
dbt docs serve
```

---

# Data Enrichment (YOLO)

Run object detection

```bash
python -m src.yolo_detect
```

Classify detected images

```bash
python -m src.classify_images
```

Load detection results

```bash
python -m scripts.load_yolo_results
```

Rebuild the warehouse

```bash
cd medical_warehouse

dbt build
```

---

# Analytical API

Start the API server

```bash
uvicorn api.main:app --reload
```

Open the Swagger documentation

```
http://127.0.0.1:8000/docs
```

Available endpoints

```
GET /api/reports/top-products

GET /api/channels/{channel_name}/activity

GET /api/search/messages

GET /api/reports/visual-content
```

---

# Task 5 — Pipeline Orchestration

Launch Dagster

```bash
dagster dev -f pipeline/definitions.py
```

Open the Dagster UI

```
http://localhost:3000
```

Run the pipeline

```
medical_pipeline
```

Pipeline execution order

```text
scrape_telegram_data
        │
        ▼
load_raw_to_postgres
        │
        ▼
run_dbt_transformations
        │
        ▼
run_yolo_enrichment
        │
        ▼
load_yolo_results
        │
        ▼
run_dbt_transformations
```

---

# Running the Complete Pipeline Manually

Execute the following commands in order:

```bash
python -m scripts.scrape_telegram

python -m scripts.load_raw_to_postgres

cd medical_warehouse
dbt build
cd ..

python -m src.yolo_detect

python -m src.classify_images

python -m scripts.load_yolo_results

cd medical_warehouse
dbt build
cd ..

uvicorn api.main:app --reload
```

---

# Useful Commands

Connect to PostgreSQL

```bash
docker exec -it postgres psql -U postgres -d medical_db
```

Run dbt tests

```bash
dbt test
```

Generate dbt documentation

```bash
dbt docs generate
```

Serve dbt documentation

```bash
dbt docs serve
```

Start FastAPI

```bash
uvicorn api.main:app --reload
```

Start Dagster

```bash
dagster dev -f pipeline/definitions.py
```

---

# Technologies Used

- Python
- Telethon
- PostgreSQL
- SQLAlchemy
- dbt
- YOLOv8 (Ultralytics)
- FastAPI
- Pydantic
- Dagster
- Docker


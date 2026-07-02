from dagster import job

from pipeline.ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment,
)

@job
def medical_pipeline():

    scrape = scrape_telegram_data()

    load = load_raw_to_postgres(start=scrape)

    transform = run_dbt_transformations(start=load)

    run_yolo_enrichment(start=transform)
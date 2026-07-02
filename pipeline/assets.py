from dagster import asset
import subprocess


@asset
def scrape_telegram_data():
    subprocess.run(
        ["python", "-m", "src.scraper"],
        check=True
    )


@asset
def load_raw_to_postgres(scrape_telegram_data):
    subprocess.run(
        ["python", "-m", "scripts.load_raw_to_postgres"],
        check=True
    )


@asset
def run_dbt_transformations(load_raw_to_postgres):
    subprocess.run(
        ["dbt", "build"],
        cwd="medical_warehouse",
        check=True
    )


@asset
def run_yolo_enrichment(run_dbt_transformations):
    subprocess.run(
        ["python", "-m", "src.yolo_detect"],
        check=True
    )

    subprocess.run(
        ["python", "-m", "src.classify_images"],
        check=True
    )

    subprocess.run(
        ["python", "-m", "scripts.load_yolo_results"],
        check=True
    )

    subprocess.run(
        ["dbt", "build"],
        cwd="medical_warehouse",
        check=True
    )
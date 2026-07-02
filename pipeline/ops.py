from dagster import In, Nothing, op
import subprocess
import sys

@op
def scrape_telegram_data():
    subprocess.run(
        subprocess.run(
        [sys.executable, "-m", "scripts.scrape_telegram"],
        check=True
)
    )


@op(ins={"start": In(Nothing)})
def load_raw_to_postgres():
    subprocess.run(
        [sys.executable, "-m", "scripts.load_raw_to_postgres"],
        check=True
    )

@op(ins={"start": In(Nothing)})
def load_yolo_results():
    subprocess.run(
        [sys.executable, "-m", "scripts.load_yolo_results"],
        check=True
    )
@op(ins={"start": In(Nothing)})
def run_dbt_transformations():
    subprocess.run(
        ["dbt", "build"],
        cwd="medical_warehouse",
        check=True
    )


@op(ins={"start": In(Nothing)})
def run_yolo_enrichment():
    subprocess.run(
        [sys.executable, "-m", "src.yolo_detect"],
        check=True
    )

    subprocess.run(
        [sys.executable, "-m", "src.classify_images"],
        check=True
    )

    subprocess.run(
        [sys.executable, "-m", "scripts.load_yolo_results"],
        check=True
    )

    subprocess.run(
        ["dbt", "build"],
        cwd="medical_warehouse",
        check=True
    )
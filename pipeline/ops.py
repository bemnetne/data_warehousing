from dagster import In, Nothing, op
import subprocess
import sys


def run_command(command, cwd=None):
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True
    )

    print("========== STDOUT ==========")
    print(result.stdout)

    print("========== STDERR ==========")
    print(result.stderr)

    result.check_returncode()

@op
def scrape_telegram_data():
    run_command(
        [sys.executable, "-m", "scripts.scrape_telegram"]
    )


@op(ins={"start": In(Nothing)})
def load_raw_to_postgres():
    run_command(
        [sys.executable, "-m", "scripts.load_raw_to_postgres"]
    )

@op(ins={"start": In(Nothing)})
def load_yolo_results():
    run_command(
        [sys.executable, "-m", "scripts.load_yolo_results"]
    )
@op(ins={"start": In(Nothing)})
def run_dbt_transformations():
    run_command(
        ["dbt", "build"],
        cwd="medical_warehouse"
    )


@op(ins={"start": In(Nothing)})
def run_yolo_enrichment():
    run_command(
        [sys.executable, "-m", "src.yolo_detect"]
    )

    run_command(
        [sys.executable, "-m", "src.classify_images"]
    )

    run_command(
        [sys.executable, "-m", "scripts.load_yolo_results"]
    )

    run_command(
        ["dbt", "build"],
        cwd="medical_warehouse"
    )
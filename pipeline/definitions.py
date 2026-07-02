from dagster import Definitions

from pipeline.jobs import medical_pipeline
from pipeline.schedule import daily_schedule

defs = Definitions(
    jobs=[medical_pipeline],
    schedules=[daily_schedule]
)
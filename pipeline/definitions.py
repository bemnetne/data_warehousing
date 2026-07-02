from dagster import Definitions

from pipeline.jobs import medical_pipeline

defs = Definitions(
    jobs=[medical_pipeline]
)
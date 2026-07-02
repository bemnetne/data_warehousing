from dagster import ScheduleDefinition

from pipeline.jobs import medical_pipeline

daily_schedule = ScheduleDefinition(
    job=medical_pipeline,
    cron_schedule="0 0 * * *",  # Every day at midnight
    name="daily_medical_pipeline",
)
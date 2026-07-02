from dagster import failure_hook


@failure_hook
def failure_alert(context):
    context.log.error(
        f"Pipeline failed at op '{context.op.name}'."
    )
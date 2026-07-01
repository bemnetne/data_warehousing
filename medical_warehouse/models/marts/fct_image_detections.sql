{{ config(materialized='table') }}

SELECT

    f.message_id,

    f.channel_key,

    f.date_key,

    d.detected_objects AS detected_class,

    d.confidence_score,

    d.image_category

FROM {{ ref('fct_messages') }} f

JOIN {{ ref('stg_image_detections') }} AS d
    ON f.message_id = d.message_id
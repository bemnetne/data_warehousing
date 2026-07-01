{{ config(materialized='view') }}

SELECT

    CAST(message_id AS BIGINT) AS message_id,

    channel_name,

    detected_objects,

    confidence_score::FLOAT AS confidence_score,

    image_category

FROM {{ source('raw', 'image_detections') }}
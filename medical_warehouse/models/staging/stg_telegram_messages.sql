WITH source_data AS (

    SELECT *

    FROM {{ source('raw', 'telegram_messages') }}

),

cleaned AS (

    SELECT

        CAST(message_id AS BIGINT)                AS message_id,

        LOWER(TRIM(channel_name))                 AS channel_name,

        CAST(message_date AS TIMESTAMP)           AS message_date,

        TRIM(message_text)                        AS message_text,

        CAST(views AS INTEGER)                    AS views,

        CAST(forwards AS INTEGER)                 AS forwards,

        CAST(has_media AS BOOLEAN)                AS has_media,

        image_path,

        LENGTH(COALESCE(message_text, ''))        AS message_length,

        CASE
            WHEN image_path IS NOT NULL THEN TRUE
            ELSE FALSE
        END                                      AS has_image

    FROM source_data

)

SELECT *

FROM cleaned

WHERE

    message_text IS NOT NULL

    AND TRIM(message_text) <> ''
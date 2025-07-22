with base as (
  SELECT
    user_id || '_' || FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%E6S', created_at) || '_' || reason AS notification_id
    ,TIMESTAMP('2025-07-01 00:00:00.000000 UTC') AS load_date
    ,{{ record_source('stg_notifications') }} AS record_source
FROM {{ ref('stg_notifications') }}
)

SELECT
  *
  ,md5(notification_id) AS notification_hk
FROM base

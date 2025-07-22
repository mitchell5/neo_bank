SELECT
    notification_id
    ,md5(notification_id) AS notification_hk
    ,TIMESTAMP('2025-07-01 00:00:00.000000 UTC') AS load_date
    ,{{ record_source('stg_notifications') }} AS record_source
FROM {{ ref('stg_notifications') }}

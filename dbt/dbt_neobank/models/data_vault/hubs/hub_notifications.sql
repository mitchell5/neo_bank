SELECT
    notification_id
    ,md5(notification_id) AS notification_hk
    ,{{ load_date() }} AS load_date
    ,{{ record_source('stg_notifications') }} AS record_source
FROM {{ ref('stg_notifications') }}

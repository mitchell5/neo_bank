WITH notifications_with_user AS (
  SELECT
    n.notification_id
    ,u.user_id
    ,md5(cast(u.user_id as string)) AS user_hk
    ,md5(cast(notification_id as string)) AS notification_hk
  FROM {{ ref('stg_notifications') }} n
  JOIN {{ ref('stg_users') }} u
    ON n.user_id = u.user_id
)


SELECT
  md5(concat(user_hk,notification_hk)) AS user_notification_hk
  ,user_hk
  ,notification_hk
  ,timestamp('2025-07-01 00:00:00.000000 UTC') AS load_date
  ,{{ record_source('stg_transactions') }} AS record_source
FROM notifications_with_user

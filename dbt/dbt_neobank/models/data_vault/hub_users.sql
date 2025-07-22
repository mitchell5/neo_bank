
SELECT
    user_id
    ,md5(cast(user_id as string)) as user_hk
    ,timestamp('2025-07-01 00:00:00.000000 UTC') AS load_date
    ,{{ record_source('stg_users') }} AS record_source
FROM {{ ref('stg_users') }}


SELECT
    user_id
    ,md5(cast(user_id as string)) as user_hk
    ,{{ load_date() }} AS load_date
    ,{{ record_source('stg_users') }} AS record_source
FROM {{ ref('stg_users') }}

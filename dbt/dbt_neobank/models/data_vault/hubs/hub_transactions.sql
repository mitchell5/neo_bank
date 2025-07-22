
SELECT
    transaction_id
    ,md5(cast(transaction_id as string)) as transaction_hk
    ,timestamp('2025-07-01 00:00:00.000000 UTC') AS load_date
    ,{{ record_source('stg_transactions') }} AS record_source
FROM {{ ref('stg_transactions') }}

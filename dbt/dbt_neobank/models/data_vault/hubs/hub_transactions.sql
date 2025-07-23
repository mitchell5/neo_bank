
SELECT
    transaction_id
    ,md5(cast(transaction_id as string)) as transaction_hk
    ,{{ load_date() }} AS load_date
    ,{{ record_source('stg_transactions') }} AS record_source
FROM {{ ref('stg_transactions') }}

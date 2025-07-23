WITH transactions_with_user AS (
  SELECT
    t.transaction_id
    ,u.user_id
    ,md5(cast(u.user_id as string)) AS user_hk
    ,md5(cast(transaction_id as string)) AS transaction_hk
  FROM {{ ref('stg_transactions') }} t
  JOIN {{ ref('stg_users') }} u
    ON t.user_id = u.user_id
)


SELECT
  md5(concat(user_hk,transaction_hk)) AS user_transaction_hk
  ,user_hk
  ,transaction_hk
  ,{{ load_date() }} AS load_date
  ,{{ record_source('stg_transactions') }} AS record_source
FROM transactions_with_user

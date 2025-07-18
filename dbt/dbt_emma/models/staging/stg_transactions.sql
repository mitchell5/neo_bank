{{ config(materialized='view') }}

select
        cast(transaction_id as int) as transaction_id
        ,transactions_type as transaction_type
        ,transactions_currency as transaction_currency
        ,cast(amount_usd as numeric) as amount_usd
        ,transactions_state as transaction_state
        ,ea_cardholderpresence
        ,ea_merchant_country
        ,direction
        ,cast(substr(user_id, 6) as int64) as user_id
        ,timestamp_micros(cast(created_date / 1000 as int64)) as created_at

from {{ source('raw', 'transactions') }}
WHERE 1=1
  and SAFE_CAST(user_id AS int) IS NOT NULL
  and SAFE_CAST(transaction_id AS int) IS NOT NULL

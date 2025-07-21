{{ config(materialized='view') }}

select
        transaction_id
        ,transactions_type as transaction_type
        ,transactions_currency as transaction_currency
        ,amount_usd
        ,transactions_state as transaction_state
        ,ea_cardholderpresence
        ,ea_merchant_country
        ,direction
        ,user_id
        ,timestamp_micros(cast(created_date / 1000 as int64)) as created_at

from {{ source('raw', 'transactions') }}

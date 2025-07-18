{{ config(materialized='view') }}

select
        cast(user_id as int) as user_id
        ,birth_year
        ,country
        ,timestamp_micros(cast(created_date / 1000 as int64)) as created_at
        ,plan
        ,user_settings_crypto_unlocked as crypto_unlocked
        ,attributes_notifications_marketing_push as marketing_push
        ,attributes_notifications_marketing_email as marketing_email
        ,num_contacts
from {{ source('raw', 'users') }}
WHERE SAFE_CAST(user_id AS int) IS NOT NULL

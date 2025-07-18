{{ config(materialized='view') }}

select
        reason
        ,channel
        ,status
        ,cast(user_id as int) as user_id
        --,timestamp_micros(created_date) as created_at
        ,timestamp_micros(cast(created_date / 1000 as int64)) as created_at
from {{ source('raw', 'notifications') }}
WHERE SAFE_CAST(user_id AS int) IS NOT NULL

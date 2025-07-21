
select
        reason
        ,channel
        ,status
        ,user_id
        --,timestamp_micros(created_date) as created_at
        ,timestamp_micros(cast(created_date / 1000 as int64)) as created_at
from {{ source('raw', 'notifications') }}

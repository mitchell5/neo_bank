
select
        reason
        ,channel
        ,status
        ,user_id
        --,timestamp_micros(created_date) as created_at
        ,timestamp_micros(cast(created_date / 1000 as int64)) as created_at
        ,user_id || '_' || timestamp_micros(cast(created_date / 1000 as int64)) || '_' || reason AS notification_id
from {{ source('raw', 'notifications') }}

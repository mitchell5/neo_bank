select
    notification_id,
    md5(notification_id) as notification_hk
    ,{{ load_date() }} as load_date
    ,{{ record_source('stg_notifications') }} as record_source
from {{ ref('stg_notifications') }}

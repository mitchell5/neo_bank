select
    user_id,
    device_type
from {{ source('raw', 'devices') }}

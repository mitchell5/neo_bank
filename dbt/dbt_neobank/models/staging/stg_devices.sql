SELECT
  user_id
  ,device_type
FROM {{ source('raw', 'devices') }}

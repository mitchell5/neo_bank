{{ config(materialized='view') }}


SELECT
  cast(user_id as int) as user_id
  ,device_type
FROM {{ source('raw', 'devices') }}
WHERE SAFE_CAST(user_id AS int) IS NOT NULL

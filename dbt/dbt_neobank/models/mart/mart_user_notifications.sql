with link_user_notification as (
  select
   user_notification_hk,
   user_hk,
   notification_hk,
   load_date,
   record_source
  from {{ ref('link_user_notification') }}
),

hub_users as (
  select user_id,
    user_hk,
    load_date,
    record_source
FROM {{ ref('hub_users') }}
),

hub_notifications as (
  SELECT
    notification_id,
    notification_hk,
    load_date,
    record_source
  FROM {{ ref('hub_notifications') }}
),

sat_channel as (
  SELECT
    notification_hk,
    channel,
    load_date as valid_from,
    load_end_date as valid_to,
    record_source
FROM {{ ref('sat_notif_channel') }} s
),

sat_reason as (
  SELECT
    notification_hk,
    reason,
    load_date as valid_from,
    load_end_date as valid_to,
    record_source
FROM {{ ref('sat_notif_reason') }} s
),

sat_status as (
  SELECT
    notification_hk,
    status,
    load_date as valid_from,
    load_end_date as valid_to,
    record_source
FROM {{ ref('sat_notif_status') }} s
),

final as (
  select
    usr.user_id,
    notif.notification_id,
    chn.channel,
    rsn.reason,
    stat.status,
    chn.valid_from,
    chn.valid_to
  from hub_users usr
    join link_user_notification link
      on usr.user_hk = link.user_hk
    join hub_notifications notif
      on notif.notification_hk = link.notification_hk
    join sat_channel chn
      on chn.notification_hk = link.notification_hk
    join sat_reason rsn
      on chn.notification_hk = rsn.notification_hk
    join sat_status stat
      on stat.notification_hk = rsn.notification_hk
)

select *
from final

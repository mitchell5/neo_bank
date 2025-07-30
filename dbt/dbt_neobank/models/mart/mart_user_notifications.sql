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
    select
        user_id,
        user_hk,
        load_date,
        record_source
    from {{ ref('hub_users') }}
),

hub_notifications as (
    select
        notification_id,
        notification_hk,
        load_date,
        record_source
    from {{ ref('hub_notifications') }}
),

sat_channel as (
    select
        notification_hk,
        channel,
        load_date as valid_from,
        load_end_date as valid_to,
        record_source
    from {{ ref('sat_notif_channel') }}
),

sat_reason as (
    select
        notification_hk,
        reason,
        load_date as valid_from,
        load_end_date as valid_to,
        record_source
    from {{ ref('sat_notif_reason') }}
),

sat_status as (
    select
        notification_hk,
        status,
        load_date as valid_from,
        load_end_date as valid_to,
        record_source
    from {{ ref('sat_notif_status') }}
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
    from hub_users as usr
    inner join link_user_notification as link
        on usr.user_hk = link.user_hk
    inner join hub_notifications as notif
        on link.notification_hk = notif.notification_hk
    inner join sat_channel as chn
        on link.notification_hk = chn.notification_hk
    inner join sat_reason as rsn
        on chn.notification_hk = rsn.notification_hk
    inner join sat_status as stat
        on rsn.notification_hk = stat.notification_hk
)

select *
from final

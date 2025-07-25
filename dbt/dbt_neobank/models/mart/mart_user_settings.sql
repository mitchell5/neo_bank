{{ config(
    materialized='table',
    schema='neobank_data_marts'
) }}

with base as (

    select
        hub.user_id,

        creation.created_at,
        dob.birth_year,
        country.country,
        device.device_type,
        crypto.crypto_unlocked,
        plan.plan,
        email.marketing_email,
        push.marketing_push,
        contacts.num_contacts

    from {{ ref('hub_users') }} as hub

    left join {{ ref('sat_user_creation') }} as creation
        on hub.user_hk = creation.user_hk

    left join {{ ref('sat_user_dob') }} as dob
        on hub.user_hk = dob.user_hk

    left join {{ ref('sat_user_country') }} as country
        on hub.user_hk = country.user_hk

    left join {{ ref('sat_user_device') }} as device
        on hub.user_hk = device.user_hk

    left join {{ ref('sat_user_crypto') }} as crypto
        on hub.user_hk = crypto.user_hk

    left join {{ ref('sat_user_plan') }} as plan
        on hub.user_hk = plan.user_hk

    left join {{ ref('sat_user_mktg_email') }} as email
        on hub.user_hk = email.user_hk

    left join {{ ref('sat_user_mktg_push') }} as push
        on hub.user_hk = push.user_hk

    left join {{ ref('sat_user_contacts') }} as contacts
        on hub.user_hk = contacts.user_hk

)

select * from base

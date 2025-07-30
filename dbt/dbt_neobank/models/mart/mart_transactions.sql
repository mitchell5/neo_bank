with base as (
    select
        user_id,
        transaction_id,
        amount_usd,
        ea_cardholderpresence,
        created_at,
        direction,
        transaction_state,
        transaction_type
    from {{ ref('link_user_transaction') }}
        join {{ ref('hub_transactions') }} using (transaction_hk)
        join {{ ref('hub_users') }} using (user_hk)
        join {{ ref('sat_trans_amount_usd') }} using (transaction_hk)
        join {{ ref('sat_trans_cardholder') }} using (transaction_hk)
        join {{ ref('sat_trans_creation') }} using (transaction_hk)
        join {{ ref('sat_trans_direction') }} using (transaction_hk)
        join {{ ref('sat_trans_state') }} using (transaction_hk)
        join {{ ref('sat_trans_type') }} using (transaction_hk)
)

select
    date_trunc(created_at, week (monday)) as transaction_week,
    user_id,
    transaction_state,
    transaction_type,
    count(case when ea_cardholderpresence = true then transaction_id end) as physical_transactions,
    count(case when ea_cardholderpresence = false then transaction_id end) as online_transactions,
    count(case when direction = 'INBOUND' then transaction_id end) as inbound_transactions,
    count(case when direction = 'OUTBOUND' then transaction_id end) as outbound_transactions,
    count(distinct transaction_id) as total_transactions,
    sum(amount_usd) as amount_usd
from base
where date_trunc(created_at, week (monday)) >= '2018-01-08'
group by 1, 2, 3, 4
order by 1, 2

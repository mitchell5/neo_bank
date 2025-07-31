with base as (
    select
        hu.user_id,
        ht.transaction_id,
        sau.amount_usd,
        stc.ea_cardholderpresence,
        stcr.created_at,
        std.direction,
        sts.transaction_state,
        stt.transaction_type
    from {{ ref('link_user_transaction') }} as lut
    inner join {{ ref('hub_transactions') }} as ht using (transaction_hk)
    inner join {{ ref('hub_users') }} as hu using (user_hk)
    inner join {{ ref('sat_trans_amount_usd') }} as sau using (transaction_hk)
    inner join {{ ref('sat_trans_cardholder') }} as stc using (transaction_hk)
    inner join {{ ref('sat_trans_creation') }} as stcr using (transaction_hk)
    inner join {{ ref('sat_trans_direction') }} as std using (transaction_hk)
    inner join {{ ref('sat_trans_state') }} as sts using (transaction_hk)
    inner join {{ ref('sat_trans_type') }} as stt using (transaction_hk)
)

select
    date_trunc(created_at, month) as transaction_month,
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
group by 1, 2, 3, 4
order by 1, 2

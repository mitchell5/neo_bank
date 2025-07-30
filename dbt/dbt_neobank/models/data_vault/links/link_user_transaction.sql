with transactions_with_user as (
    select
        t.transaction_id,
        u.user_id,
        md5(cast(u.user_id as string)) as user_hk,
        md5(cast(t.transaction_id as string)) as transaction_hk
    from {{ ref('stg_transactions') }} as t
    inner join {{ ref('stg_users') }} as u
        on t.user_id = u.user_id
)

select
    md5(concat(user_hk, transaction_hk)) as user_transaction_hk,
    user_hk,
    transaction_hk
    ,{{ load_date() }} as load_date
    ,{{ record_source('stg_transactions') }} as record_source
from transactions_with_user

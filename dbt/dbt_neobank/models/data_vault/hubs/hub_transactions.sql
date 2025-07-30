select
    transaction_id,
    md5(cast(transaction_id as string)) as transaction_hk
    ,{{ load_date() }} as load_date
    ,{{ record_source('stg_transactions') }} as record_source
from {{ ref('stg_transactions') }}

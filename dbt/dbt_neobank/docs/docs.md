{% docs __devices %}
device type of user, one row per user_id
{% enddocs %}

{% docs __device_type %}
type of device (apple, android, or other)
{% enddocs %}

{% docs __user_id %}
user identifier - primary key users and foreign key to transactions, users, and
notifications table
{% enddocs %}

{% docs __device_id %}
surrogate key generated from device_type and user_id
{% enddocs %}

{% docs __notifications %}
notifications sent to users. One row per notification sent.
{% enddocs %}

{% docs __reason %}
description of notification sent
{% enddocs %}

{% docs __channel %}
how notification was sent - via SMS, push, or email
{% enddocs %}

{% docs __status %}
status of notification sent - SENT or FAILED
{% enddocs %}

{% docs __created_at %}
creation date of record
{% enddocs %}

{% docs __notification_id %}
composite key needed for data vault model
{% enddocs %}

{% docs __transactions %}
user transactions, 1 row per transaction_id
{% enddocs %}

{% docs __transaction_id %}
transaction identifier - primary key for transactions
{% enddocs %}

{% docs __transaction_type %}
type of user transaction, 10 in total, examples such as refund or topup
{% enddocs %}

{% docs __transaction_currency %}
monetary currency of user transaction, 35 in total
{% enddocs %}

{% docs __amount_usd %}
amount of each user transaction in USD currency
{% enddocs %}

{% docs __transaction_state %}
state of each user transaction, 6 in total, examples such as failed or completed
{% enddocs %}

{% docs __ea_cardholderpresence %}
whether the card owner made a purchase in person (TRUE) or online (FALSE), also
have unknown and null values
{% enddocs %}

{% docs __ea_merchant_country %}
3 letter country code of merchant where transaction was made, has null values
also
{% enddocs %}

{% docs __direction %}
whether money is entering user's account (INBOUND) or leaving it (OUTBOUND)
{% enddocs %}

{% docs __users %}
information on users, one row per user_id
{% enddocs %}

{% docs __birth_year %}
4 digit birth year
{% enddocs %}

{% docs __country%}
2 digit country code
{% enddocs %}

{% docs __crypto_unlocked%}
whether account has crypto acces or not
{% enddocs %}

{% docs __plan%}
plan type of user, 6 in total, free and paid options
{% enddocs %}

{% docs __marketing_push%}
whether user has allows marketing push notifications or not
{% enddocs %}

{% docs __marketing_email%}
whether user has allows marketing emails or not
{% enddocs %}

{% docs __num_contacts%}
number of contacts a user has added to their account, can be 0
{% enddocs %}

{% docs __hub_notifications%}
Hub table for unique business key from stg_notifications
{% enddocs %}

{% docs __hk%}
MD5 hash
{% enddocs %}

{% docs __load_date%}
Load Date
{% enddocs %}

{% docs __load_end_date%}
Load End Date
{% enddocs %}

{% docs __record_source%}
Record's Source
{% enddocs %}

{% docs __hub_transactions%}
Hub table for unique business key from stg_transactions
{% enddocs %}

{% docs __hub_users%}
Hub table for unique business key from stg_users
{% enddocs %}

{% docs __link_user_transaction%}
link table connecting users and transactions
{% enddocs %}

{% docs __link_user_notification%}
link table connecting users and notifications
{% enddocs %}

{% docs __sat_user_dob%}
satellite table showing user birth year
{% enddocs %}

{% docs __sat_user_country%}
satellite table showing user country
{% enddocs %}

{% docs __sat_user_creation%}
satellite table showing timestamp of user account creation
{% enddocs %}

{% docs __sat_user_plan%}
satellite table showing the plan the user is subscribed to
{% enddocs %}

{% docs __sat_user_crypto%}
satellite table showing whether user can transact with crypto or not
{% enddocs %}

{% docs __sat_user_mktg_push%}
satellite table showing whether user has enabled push notifications
{% enddocs %}

{% docs __sat_user_mktg_email%}
satellite table showing whether user has enabled push notifications
{% enddocs %}

{% docs __sat_user_contacts%}
satellite table showing number of contacts user added to account
{% enddocs %}

{% docs __sat_user_device%}
satellite table showing device type of user
{% enddocs %}

{% docs __sat_trans_type%}
satellite table for transaction type of user
{% enddocs %}

{% docs __sat_trans_currency%}
satellite table for local currency of user's transaction
{% enddocs %}

{% docs __sat_trans_amount_usd%}
satellite table for value of user's transaction in USD
{% enddocs %}

{% docs __sat_trans_state%}
satellite table for status of user's transaction
{% enddocs %}

{% docs __sat_trans_cardholder%}
satellite table for cardholder presence during transaction - ie) in person or online
{% enddocs %}

{% docs __sat_trans_country%}
satellite table for country of merchant of transaction
{% enddocs %}

{% docs __sat_trans_direction%}
satellite table for direction of transaction, in or out
{% enddocs %}

{% docs __sat_trans_creation%}
satellite table for transaction date
{% enddocs %}

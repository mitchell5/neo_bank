CREATE TABLE "hub_users" (
  "user_hk" varchar PRIMARY KEY,
  "user_id" int,
  "load_date" timestamp,
  "record_source" varchar
);

CREATE TABLE "hub_transactions" (
  "transaction_hk" varchar PRIMARY KEY,
  "transaction_id" int,
  "load_date" timestamp,
  "record_source" varchar
);

CREATE TABLE "hub_notifications" (
  "notification_hk" varchar PRIMARY KEY,
  "notification_id" int,
  "load_date" timestamp,
  "record_source" varchar
);

CREATE TABLE "link_user_transaction" (
  "user_transaction_hk" varchar PRIMARY KEY,
  "user_hk" varchar,
  "transaction_hk" varchar,
  "load_date" timestamp,
  "record_source" varchar
);

CREATE TABLE "link_user_notification" (
  "user_notification_hk" varchar PRIMARY KEY,
  "user_hk" varchar,
  "notification_hk" varchar,
  "load_date" timestamp,
  "record_source" varchar
);

CREATE TABLE "sat_users" (
  "user_hk" varchar,
  "country" varchar,
  "birth_year" int,
  "created_date" int,
  "plan" varchar,
  "crypto_unlocked" boolean,
  "marketing_push" boolean,
  "marketing_email" boolean,
  "num_contacts" int,
  "load_date" timestamp,
  "record_source" varchar
);

CREATE TABLE "sat_transactions" (
  "transaction_hk" varchar,
  "transactions_type" varchar,
  "transactions_currency" varchar,
  "amount_usd" float,
  "transactions_state" varchar,
  "ea_cardholderpresence" boolean,
  "ea_merchant_country" varchar,
  "direction" varchar,
  "created_date" int,
  "load_date" timestamp,
  "record_source" varchar
);

CREATE TABLE "sat_notifications" (
  "notification_hk" varchar,
  "reason" varchar,
  "channel" varchar,
  "status" varchar,
  "created_date" int,
  "load_date" timestamp,
  "record_source" varchar
);

ALTER TABLE "link_user_transaction" ADD FOREIGN KEY ("user_hk") REFERENCES "hub_users" ("user_hk");

ALTER TABLE "link_user_transaction" ADD FOREIGN KEY ("transaction_hk") REFERENCES "hub_transactions" ("transaction_hk");

ALTER TABLE "link_user_notification" ADD FOREIGN KEY ("user_hk") REFERENCES "hub_users" ("user_hk");

ALTER TABLE "link_user_notification" ADD FOREIGN KEY ("notification_hk") REFERENCES "hub_notifications" ("notification_hk");

ALTER TABLE "sat_users" ADD FOREIGN KEY ("user_hk") REFERENCES "hub_users" ("user_hk");

ALTER TABLE "sat_transactions" ADD FOREIGN KEY ("transaction_hk") REFERENCES "hub_transactions" ("transaction_hk");

ALTER TABLE "sat_notifications" ADD FOREIGN KEY ("notification_hk") REFERENCES "hub_notifications" ("notification_hk");

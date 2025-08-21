from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago

parquet_files = [
    "data/devices.parquet",
    "data/users.parquet",
    "data/transactions.parquet",
    "data/notifications.parquet",
]

dataset = "tidal-vim-468818-s5.neobank_data_raw"

with DAG(
    dag_id="gcs_to_bq_parquet",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
) as dag:

    for file in parquet_files:
        table_name = file.split("/")[-1].replace(".parquet", "")
        GCSToBigQueryOperator(
            task_id=f"load_{table_name}",
            bucket="neobank_data_bucket_deniz",
            source_objects=[file],
            destination_project_dataset_table=f"{dataset}.{table_name}",
            write_disposition="WRITE_APPEND",
            source_format="PARQUET",
            autodetect=True,
        )

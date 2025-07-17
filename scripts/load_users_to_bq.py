from google.cloud import bigquery

# Init client
client = bigquery.Client()

# Define parameters
table_id = "sacred-choir-466017-s9.neobank_data_staging.users"
source_uri = "gs://neobank_data_bucket/staging_data/users.parquet"

# Load config
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE  # Overwrite if exists
)

# Start load job
load_job = client.load_table_from_uri(
    source_uris=source_uri,
    destination=table_id,
    job_config=job_config
)

load_job.result()  # Waits for completion

print(f"Loaded {table_id} successfully.")

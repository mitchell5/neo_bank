#!/bin/bash
# init_airflow_users.sh

# Exit immediately if a command fails
set -e

# Initialize DB (if not already initialized)
airflow db init

# Create an admin user if it does not exist
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password password || true

# Start the scheduler & webserver if needed (optional)
# airflow scheduler & airflow webserver
airflow webserver
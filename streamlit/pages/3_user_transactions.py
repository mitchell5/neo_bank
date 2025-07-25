import os
import json
from google.oauth2 import service_account
from google.cloud import bigquery
import streamlit as st

# Load credentials from Streamlit secrets
credentials_info = st.secrets["GOOGLE_CREDENTIALS"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# BigQuery client
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


# Title
st.title("Emma")

# Initialize BigQuery client
client = bigquery.Client()

# Query to run
query = """
    SELECT *
    FROM `sacred-choir-466017-s9.neobank_data_marts.mart_transactions`
    limit 100;
"""

# Run query and load data
@st.cache_data
def load_transactions_data():
    return client.query(query).to_dataframe()

df = load_transactions_data()

# Show dataframe
st.dataframe(df)

# Example chart
st.bar_chart(df['transaction_type'].value_counts().sort_index())

import streamlit as st
from google.cloud import bigquery
import pandas as pd
import os

st.title("🔍 BigQuery Test App")

# Display the path to the credentials file
st.write("Using credentials from:")
st.code(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "Not set"))

# Create BigQuery client
try:
    client = bigquery.Client()
    st.success("✅ Successfully authenticated with BigQuery.")
except Exception as e:
    st.error(f"❌ Failed to create BigQuery client: {e}")
    st.stop()

# Sample query (public dataset)
query = """
    SELECT name, SUM(number) as total
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = 'TX'
    GROUP BY name
    ORDER BY total DESC
    LIMIT 10
"""

st.write("Running query on public BigQuery dataset:")
st.code(query)

try:
    df = client.query(query).to_dataframe()
    st.dataframe(df)
    st.success("✅ Query ran successfully.")
except Exception as e:
    st.error(f"❌ Query failed: {e}")

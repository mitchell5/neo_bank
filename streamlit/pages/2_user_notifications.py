import streamlit as st
from google.cloud import bigquery
import pandas as pd
import os
import plotly.express as px

import json
from google.oauth2 import service_account


def channel_distribution():
    query = """
        SELECT channel, count(*) as count_
        FROM `sacred-choir-466017-s9.neobank_data_marts.mart_user_notifications`
        GROUP BY channel
        ORDER BY count_ desc
    """

    return run_query(query)


def reason_distribution():
    query = """
        SELECT reason, count(*) as count_
        FROM `sacred-choir-466017-s9.neobank_data_marts.mart_user_notifications`
        GROUP BY reason
        ORDER BY count_ desc
    """

    return run_query(query)

def status_per_channel():

    query = """
        SELECT channel, status, COUNT(*) AS count_
        FROM `sacred-choir-466017-s9.neobank_data_marts.mart_user_notifications`
        GROUP BY channel, status
        ORDER BY count_ desc
    """

    return run_query(query)

def reason_per_channel():

    query = """
        SELECT reason, channel, COUNT(*) AS count_
        FROM `sacred-choir-466017-s9.neobank_data_marts.mart_user_notifications`
        GROUP BY reason, channel
    """

    return run_query(query)

# Run query and load data
@st.cache_data
def run_query(query):
    return client.query(query).to_dataframe()


if __name__ == "__main__":
    st.title("🔍 Neo Bank Dashboard")

    # Load credentials from Streamlit secrets
    credentials_info = st.secrets["GOOGLE_CREDENTIALS"]
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    # BigQuery client
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)


    # Title
    st.title("Notifications Analysis")


    # Initialize BigQuery client - Lina
    #client = bigquery.Client()

    # Channel Distribution
    st.subheader("Channel Distribution")
    st.caption("Which notification channels are most used?")
    st.caption("Is there a heavy dependency on one channel?")

    df = channel_distribution()

    # Display dataframe
    #st.dataframe(df)

    # Create pie chart
    fig = px.pie(df, names="channel", values="count_",
                title="Channel Distribution")

    # Show chart
    st.plotly_chart(fig, use_container_width=True)

    # Reason Distribution
    st.subheader("Notification Reasons Distribution")
    st.caption("What are the widely used marketing reasons?")
    st.caption("Which ones could be increased/decreased in future?")
    df = reason_distribution()

    # Plotly bar chart
    fig = px.bar(df, x="reason", y="count_", title="Reason Distribution",
                labels={"reason": "Reason", "count_": "Count"},
                color="reason",
                height=600
                )
    # Rotate x-axis labels
    fig.update_layout(
        xaxis_tickangle=-45,  # diagonal
        showlegend=False      # hide legend
    )

    # Show chart
    st.plotly_chart(fig, use_container_width=True)

    # Status Per Channel
    st.subheader("Status Per Channel")
    st.caption("Which notification channels tend to fail?")
    st.caption("How can further marketing strategies improved?")
    df = status_per_channel()

    # Calculate total counts per channel
    total_per_channel = df.groupby('channel')['count_'].transform('sum')

    # Calculate percentage per row
    df['percent'] = (df['count_'] / total_per_channel) * 100

    # Format the percentage text for labels
    df['percent_text'] = df['percent'].apply(lambda x: f"{x:.1f}%")

    # Create stacked bar chart using Plotly Express
    fig = px.bar(df, x="channel", y="count_", title="Status Per Channel",
            labels={"count_": "Count", "channel": "Channel", "status": "Status"},
            color="status",
            text='percent_text',    # to show the percentage
            height=600,
            barmode="stack"
            )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)




    # Reason Channel HeatMap
    st.subheader("Reason Per Channel")
    st.caption("Which marketing reasons are most frequently used across different notification channels?")
    st.caption("Is there a spike in push notifications for special campaigns like Black Friday?")

    df = reason_per_channel()

    # Assuming df has: reason, channel, count
    fig = px.density_heatmap(
        df,
        x="channel",
        y="reason",
        z="count_",
        color_continuous_scale="Blues",
        title="Notification Reasons by Channel Heatmap",
        labels={"reason": "Reason", "channel": "Channel", "count_": "Count"},
        height=700  # Increase height for better readability
    )

    fig.update_layout(
        xaxis={'side': 'top'},
        yaxis={'categoryorder': 'total ascending'}
    )

    st.plotly_chart(fig, use_container_width=True)

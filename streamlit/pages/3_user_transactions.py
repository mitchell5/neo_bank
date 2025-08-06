import os
import json
from google.oauth2 import service_account
from google.cloud import bigquery
import streamlit as st
import pandas as pd
import altair as alt

# --- Page setup ---
st.set_page_config(layout="wide")
st.title("Cohort Analysis of Customer Retention & Transaction Behavior")

# --- Load credentials ---
credentials_info = st.secrets["GOOGLE_CREDENTIALS"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# --- Load data ---
@st.cache_data
def load_transactions_data():
    query = """
        SELECT *
        FROM `sacred-choir-466017-s9.neobank_data_marts.mart_transactions`;
    """
    return client.query(query).to_dataframe()

df = load_transactions_data()

# --- Preprocessing ---
df['transaction_month'] = pd.to_datetime(df['transaction_month']).dt.to_period('M').dt.to_timestamp()

first_txn = df.groupby('user_id')['transaction_month'].min().reset_index()
first_txn.columns = ['user_id', 'cohort_month']
df = df.merge(first_txn, on='user_id')

df['cohort_month'] = df['cohort_month'].dt.to_period('M').dt.to_timestamp()

df['months_since_cohort'] = (
    (df['transaction_month'].dt.year - df['cohort_month'].dt.year) * 12 +
    (df['transaction_month'].dt.month - df['cohort_month'].dt.month)
)

# --- Retention calculation ---
retention = (
    df.groupby(['cohort_month', 'months_since_cohort'])['user_id']
    .nunique()
    .reset_index()
    .rename(columns={'user_id': 'active_users'})
)

cohort_sizes = retention[retention.months_since_cohort == 0][['cohort_month', 'active_users']]
cohort_sizes.columns = ['cohort_month', 'cohort_size']

retention = retention.merge(cohort_sizes, on='cohort_month')
retention['retention_rate'] = retention['active_users'] / retention['cohort_size']

# --- Sidebar filters ---
st.sidebar.subheader("📆 Select Cohort Months")
available_months = sorted(retention['cohort_month'].dt.strftime('%Y-%m').unique())
selected_months = st.sidebar.multiselect(
    'Select more months for 2nd Chart:',
    options=available_months,
    default=['2018-02','2019-02']
)
selected_months_dt = pd.to_datetime(selected_months)
retention_filtered = retention[retention['cohort_month'].isin(selected_months_dt)]

# --- Chart 1: Retention by cohort over months ---
retention_line_chart = alt.Chart(retention_filtered).mark_line(point=True).encode(
    x=alt.X('months_since_cohort:O', title='Months Since First Transaction'),
    y=alt.Y('retention_rate:Q', title='Retention Rate', axis=alt.Axis(format='%')),
    color=alt.Color(
        'cohort_month:T',
        title='Cohort Month',
        scale=alt.Scale(scheme='set1'),
        legend=alt.Legend(
            values=selected_months_dt,
            labelFontSize=12,
            titleFontSize=13,
            symbolSize=100,
            orient='right'
        )
    ),
    tooltip=[
        alt.Tooltip('cohort_month:T', title='Cohort Month'),
        alt.Tooltip('months_since_cohort:O', title='Months Since First Transaction'),
        alt.Tooltip('retention_rate:Q', format='.0%', title='Retention Rate')
    ]
).properties(
    width=100,
    height=400,
    title='Monthly Customer Retention Over Time by Cohort'
)

# --- Chart 2: Retention trend by months-since-cohort ---
max_month = 20
retention_time_series = retention[retention['months_since_cohort'] <= max_month].copy()
retention_time_series['cohort_month_str'] = retention_time_series['cohort_month'].dt.strftime('%Y-%m')

# Create a multi-selection bound to the legend for months_since_cohort
highlight = alt.selection_point(fields=['months_since_cohort'], bind='legend')

retention_time_chart = alt.Chart(retention_time_series).mark_line(point=True).encode(
    x=alt.X('cohort_month_str:N', title='Cohort Month'),
    y=alt.Y('retention_rate:Q', title='Retention Rate', axis=alt.Axis(format='%')),
    color=alt.Color(
        'months_since_cohort:N',
        title='Retention Month',
        scale=alt.Scale(scheme='category10'),
        legend=alt.Legend(
            labelFontSize=12,
            titleFontSize=13,
            symbolSize=100,
            orient='right'
        )
    ),
    opacity=alt.condition(
        highlight,
        alt.value(1),
        alt.value(0.1)),  # highlight selected lines, fade others
    tooltip=[
        alt.Tooltip('cohort_month_str:N', title='Cohort Month'),
        alt.Tooltip('months_since_cohort:N', title='Months Since First Transaction'),
        alt.Tooltip('retention_rate:Q', format='.0%', title='Retention Rate')
    ]
).add_params(
    highlight
).properties(
    width=600,
    height=400,
    title='Retention Rate Over Time by Months Since Cohort')


# --- Layout with insights next to charts ---

#Chart 2 + insight

col2a, col2b = st.columns([2.5, 1])
with col2a:
    st.altair_chart(retention_time_chart)

with col2b:
    st.markdown("<h4>📌 Insight</h4>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            background-color: #f0f4f8;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            font-size: 15px;
            line-height: 1.5;
            color: #333;
            ">
            Even a year after customers signed up, retention stays between 54%-60%, meaning that more than half of customers
            who sign up to this bank are still active customers (making transactions) after 12 months. This is better than
            the fintech industry average annual retention rate of 48%.
            \nSource: https://sendbird.com/blog/finance-and-payment-app-retention
            \n<em>Click on legend values to highlight them!</em>
        </div>
        """,
        unsafe_allow_html=True
    )




# Chart 1 + insight
col2a, col2b = st.columns([2.5, 1])
with col2a:
    st.altair_chart(retention_line_chart)

with col2b:
    st.markdown("<h4>📌 Insight</h4>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            background-color: #f0f4f8;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            font-size: 15px;
            line-height: 1.5;
            color: #333;
            ">
            As products improve over time, retention generally increases. However, when comparing Month 1 Retention for February cohorts in 2018
            vs 2019, we can see that it actually decreased from 75% to 66%, a drop of 12% in just 1 year!
        </div>
        """,
        unsafe_allow_html=True
    )




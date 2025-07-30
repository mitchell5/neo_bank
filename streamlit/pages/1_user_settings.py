import os
import json
import pandas as pd
import altair as alt
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# ---- Set wide layout ----
st.set_page_config(layout="wide")

# ---- 1. Auth & BigQuery Setup ----
credentials_info = st.secrets["GOOGLE_CREDENTIALS"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# ---- 2. Page Title ----
st.title("🔐 How are users interacting with settings and features in their profiles?")

# ---- 3. SQL Query to Load Full Data ----
@st.cache_data
def load_user_settings_full():
    query = """
        SELECT user_id, plan, crypto_unlocked,
               marketing_push, marketing_email, created_at,
               birth_year, country, device_type
        FROM `sacred-choir-466017-s9.neobank_data_marts.mart_user_settings`
    """
    return client.query(query).to_dataframe()

# Load data
df = load_user_settings_full()
df["created_at"] = pd.to_datetime(df["created_at"])  # Ensure datetime format

# ---- 4. Sidebar: Time Filter ----
st.sidebar.subheader("📆 Select Time Window")
available_years = sorted(df["created_at"].dt.year.unique())
selected_year = st.sidebar.selectbox("Select Year", available_years)
df_year = df[df["created_at"].dt.year == selected_year]

time_granularity = st.sidebar.radio("Filter by:", ["Quarter", "Month"])
if time_granularity == "Quarter":
    quarter = st.sidebar.selectbox("Select Quarter", ["Q1", "Q2", "Q3", "Q4"])
    quarter_map = {"Q1": [1,2,3], "Q2": [4,5,6], "Q3": [7,8,9], "Q4": [10,11,12]}
    df_filtered = df_year[df_year["created_at"].dt.month.isin(quarter_map[quarter])]
else:
    month = st.sidebar.selectbox("Select Month", list(range(1, 13)))
    df_filtered = df_year[df_year["created_at"].dt.month == month]

# ---- 5. Feature Switcher ----
st.sidebar.subheader("🔧 Select Feature to Analyze")
feature_selected = st.sidebar.radio(
    "Choose a feature:",
    ("crypto_unlocked", "marketing_push", "marketing_email"),
    format_func=lambda x: x.replace('_', ' ').title()
)
feature_nice = feature_selected.replace("_", " ").title()

# Ensure relevant columns are present
columns_needed = [
    "user_id", "plan", feature_selected,
    "marketing_push", "marketing_email",
    "created_at", "birth_year", "country", "device_type"
]
df_filtered = df_filtered.dropna(subset=columns_needed)

# ============================================================================
# ---- 6. Business Question 1: Feature Adoption by Plan ----------------------
st.markdown(f"## 📈 {feature_nice} Adoption by Plan")

adoption_by_plan = (
    df_filtered.groupby("plan")[feature_selected]
    .mean().reset_index()
    .sort_values(by=feature_selected, ascending=False)
)
adoption_by_plan[feature_selected] *= 100

total_users = len(df_filtered)
top_plan = adoption_by_plan.iloc[0]
bottom_plan = adoption_by_plan.iloc[-1]

col_chart, col_insights, col_recommendation = st.columns([2.5, 1.5, 2])

with col_chart:
    st.subheader(f"📊 {feature_nice} Adoption by Plan (%)")
    chart = alt.Chart(adoption_by_plan).mark_bar().encode(
        x=alt.X("plan:N", title="User Plan"),
        y=alt.Y(f"{feature_selected}:Q", title=f"{feature_nice} Adoption (%)"),
        color=alt.Color("plan:N", legend=None)
    ).properties(width=500, height=350)
    st.altair_chart(chart, use_container_width=True)

with col_insights:
    st.markdown("### 🔎 Key Insights")
    st.markdown(f"""
    - 👑 **{top_plan['plan']}** users adopt **{feature_nice}** most (**{top_plan[feature_selected]:.1f}%**).
    - 🐢 **{bottom_plan['plan']}** users adopt least (**{bottom_plan[feature_selected]:.1f}%**).
    - Data based on **{total_users} users**.
    """)

with col_recommendation:
    st.markdown("### 💡 Recommendation")
    st.markdown(f"""
    - Target **{bottom_plan['plan']}** users for campaigns to boost **{feature_nice}** adoption.
    - Identify barriers causing lower adoption in this segment.
    """)

st.markdown("---")

# ---- 7. Business Question 2: Demographics & Devices ------------------------
st.markdown(f"## 📱 How Do Demographics & Devices Relate to {feature_nice} Adoption?")

# 1️⃣ Prepare data
cur_year = pd.Timestamp.today().year
df_demo = df_filtered.copy()
df_demo["age"] = cur_year - df_demo["birth_year"]

# Define age buckets
bins = [17, 24, 34, 44, 54, 64, 150]
labels = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
df_demo["age_group"] = pd.cut(df_demo["age"], bins=bins, labels=labels, ordered=True)

# 2️⃣ Aggregate adoption and user count
bubble_df = (
    df_demo.groupby(["age_group", "device_type"])
    .agg(
        adoption_pct=(feature_selected, "mean"),
        user_count=("user_id", "count")
    )
    .reset_index()
)
bubble_df["adoption_pct"] *= 100

# Normalize bubble size for visibility
max_users = bubble_df["user_count"].max()
bubble_df["bubble_size"] = (bubble_df["user_count"] / max_users) *1  # adjust scale

# Identify top dynamic stats
top_row = bubble_df.loc[bubble_df["adoption_pct"].idxmax()]
largest_age = (
    bubble_df.groupby("age_group")["user_count"]
    .sum()
    .reset_index()
    .sort_values(by="user_count", ascending=False)
    .iloc[0]
)

# 3️⃣ Bubble chart
bubble_chart = alt.Chart(bubble_df).mark_circle(opacity=0.6).encode(
    x=alt.X("age_group:N", title="Age Group"),
    y=alt.Y("adoption_pct:Q", title=f"{feature_nice} Adoption (%)", scale=alt.Scale(domain=[0, 100])),
    size=alt.Size("bubble_size:Q", legend=None, scale=alt.Scale(domain=[0, bubble_df["bubble_size"].max()],
                                  range=[100, 3000])),  # <<< control bubble size
    color=alt.Color("device_type:N", title="Device Type"),
    tooltip=["device_type", "user_count:Q", alt.Tooltip("adoption_pct:Q", format=".1f")]
).properties(width=550, height=350)

# 4️⃣ Layout: Chart | Insights | Recommendations
col_chart2, col_ins2, col_rec2 = st.columns([2.5, 1.5, 2])

with col_chart2:
    st.subheader("📱 Adoption by Age Group & Device")
    st.altair_chart(bubble_chart, use_container_width=True)

with col_ins2:
    st.markdown("### 🔎 Key Insights")
    st.markdown(f"""
    - **Highest adoption**: {top_row.device_type} users in {top_row.age_group} → {top_row.adoption_pct:.1f}%.
    - **Largest cohort**: {largest_age.age_group} with {largest_age.user_count} users in total.
    - Bubble size reflects cohort size; Y-axis shows adoption rate within that segment.
    """)

with col_rec2:
    st.markdown("### 💡 Recommendation")
    st.markdown(f"""
    - Focus on large cohorts with low {feature_nice} adoption for higher impact.
    - Tailor campaigns and onboarding by device type for each age group.
    - Investigate segments with 100% adoption but very few users (small sample bias).
    """)

st.markdown("---")


# ----SQL Query to Load Transactions + Join with User Settings ----
@st.cache_data
def load_transactions_with_user_data():
    query = """
        SELECT
            t.transaction_week,
            t.user_id,
            t.amount_usd,
            u.country,
            u.plan
        FROM `sacred-choir-466017-s9.neobank_data_marts.mart_transactions` t
        LEFT JOIN `sacred-choir-466017-s9.neobank_data_marts.mart_user_settings` u
        ON t.user_id = u.user_id
    """
    return client.query(query).to_dataframe()

# Load joined transactions data
df_tx = load_transactions_with_user_data()
df_tx["transaction_week"] = pd.to_datetime(df_tx["transaction_week"])

# ---- Filter by selected year and month/quarter (reuse df_filtered logic) ----
df_tx = df_tx[df_tx["transaction_week"].dt.year == selected_year]
if time_granularity == "Quarter":
    df_tx = df_tx[df_tx["transaction_week"].dt.month.isin(quarter_map[quarter])]
else:
    df_tx = df_tx[df_tx["transaction_week"].dt.month == month]

# ---- Aggregate revenue by country and plan ----
df_revenue = (
    df_tx.groupby(["country", "plan"])["amount_usd"]
    .sum()
    .reset_index()
)

# Get top 5 countries by total revenue
top_countries = (
    df_revenue.groupby("country")["amount_usd"].sum()
    .nlargest(5)
    .index
)
df_revenue = df_revenue[df_revenue["country"].isin(top_countries)]

# ---- Plot revenue by country and plan ----
col_chart3, col_ins3, col_rec3 = st.columns([2.5, 1.5, 2])

with col_chart3:
    st.subheader("💰 Top Countries by Revenue (Split by Plan)")
    chart_rev = alt.Chart(df_revenue).mark_bar().encode(
        x=alt.X("country:N", title="Country"),
        y=alt.Y("amount_usd:Q", title="Revenue (USD)"),
        color=alt.Color("plan:N", title="User Plan"),
        tooltip=["country", "plan", alt.Tooltip("amount_usd:Q", format=",.0f")]
    ).properties(width=550, height=350)
    st.altair_chart(chart_rev, use_container_width=True)

with col_ins3:
    top_rev_country = df_revenue.groupby("country")["amount_usd"].sum().idxmax()
    top_rev_plan = df_revenue.groupby("plan")["amount_usd"].sum().idxmax()
    st.markdown("### 🔎 Key Insights")
    st.markdown(f"""
    - **Highest revenue country**: {top_rev_country}.
    - **Most profitable plan**: {top_rev_plan}.
    - Focus marketing on high-revenue countries with low adoption features.
    """)

with col_rec3:
    st.markdown("### 💡 Recommendation")
    st.markdown("""
    - Boost campaigns in top revenue countries for lower-adoption plans.
    - Consider pricing strategy adjustments for low-revenue plans.
    """)

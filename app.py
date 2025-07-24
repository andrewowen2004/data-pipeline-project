import streamlit as st
import pandas as pd
import requests
import asyncio
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "paypal_webhooks"
AMOUNT_FIELD = "amount"  # change if needed
REFRESH_INTERVAL_SEC = 2

# --- Supabase headers ---
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

# --- Fetch data ---
def fetch_transactions():
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?order=transaction_time.desc&limit=1000"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        df = df.dropna(how='any')
        if 'transaction_time' in df.columns:
            df['transaction_time'] = pd.to_datetime(df['transaction_time']).dt.strftime('%Y-%m-%d %H:%M:%S')
        return df
    return pd.DataFrame()

# --- Outlier detection ---
def filter_outliers(df, field):
    if field not in df.columns:
        return pd.DataFrame(), None
    q1 = df[field].quantile(0.25)
    q3 = df[field].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    inliers = df[(df[field] >= lower) & (df[field] <= upper)]
    outliers = df[(df[field] < lower) | (df[field] > upper)]
    mean = inliers[field].mean()
    return outliers.head(20), mean

# --- Page layout ---
st.set_page_config(layout="wide")
st.title("💳 PayPal Transaction Monitor")
auto_refresh = st.checkbox("Auto-refresh every 2 seconds", value=True)

# Define static column layout once
col1, col2 = st.columns([1, 4])

# Placeholders (for dynamic updating)
with col1:
    st.subheader("📊 Average Transaction (Excl. Outliers)")
    metric_placeholder = st.empty()

with col2:
    st.subheader("⚠️ Potential Fraud: Outlier Transactions")
    table_placeholder = st.empty()

last_updated = st.empty()

# --- Async updater ---
async def update_dashboard():
    while auto_refresh:
        df = fetch_transactions()
        outliers, mean_amount = filter_outliers(df, AMOUNT_FIELD)

        with metric_placeholder:
            if mean_amount is not None:
                st.metric("Mean Amount", f"${mean_amount:,.2f}")
            else:
                st.write("No valid transaction data.")

        with table_placeholder:
            st.dataframe(outliers, use_container_width=True)

        last_updated.markdown(f"Last updated: `{pd.Timestamp.now().strftime('%H:%M:%S')}`")
        await asyncio.sleep(REFRESH_INTERVAL_SEC)

# --- Run ---
if auto_refresh:
    asyncio.run(update_dashboard())
else:
    df = fetch_transactions()
    outliers, mean_amount = filter_outliers(df, AMOUNT_FIELD)
    with metric_placeholder:
        st.metric("Mean Amount", f"${mean_amount:,.2f}" if mean_amount else "N/A")
    with table_placeholder:
        st.dataframe(outliers, use_container_width=True)
    last_updated.markdown(f"Last updated: `{pd.Timestamp.now().strftime('%H:%M:%S')}`")

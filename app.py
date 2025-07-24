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
REFRESH_INTERVAL_SEC = 2

# --- Supabase headers ---
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

# --- Fetch most recent 20 transactions ---
def fetch_transactions():
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?order=transaction_time.desc&limit=20"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        # Remove rows that contain any None values
        df = df.dropna(how='any')

        if 'transaction_time' in df.columns:
            df['transaction_time'] = pd.to_datetime(df['transaction_time']).dt.strftime('%Y-%m-%d %H:%M:%S')

        return df
    else:
        return pd.DataFrame()

# --- UI Layout ---
st.title("🧾 Most Recent 20 PayPal Transactions")

auto_refresh = st.checkbox("Auto-refresh every 2 seconds", value=True)

table_container = st.empty()
last_updated = st.empty()

# --- Async refresh loop ---
async def update_table():
    while auto_refresh:
        df = fetch_transactions()
        with table_container.container():
            st.dataframe(df, use_container_width=True)
        last_updated.markdown(f"Last updated: `{pd.Timestamp.now().strftime('%H:%M:%S')}`")
        await asyncio.sleep(REFRESH_INTERVAL_SEC)

# --- Run dashboard ---
if auto_refresh:
    asyncio.run(update_table())
else:
    df = fetch_transactions()
    table_container.dataframe(df, use_container_width=True)
    last_updated.markdown(f"Last updated: `{pd.Timestamp.now().strftime('%H:%M:%S')}`")

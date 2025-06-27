import streamlit as st
import pandas as pd
import requests
import time
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv
import os, json

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "paypal_webhooks"                        # Replace with your table name

REFRESH_INTERVAL_SEC = 1  # ⏱️ Hard-coded refresh interval in seconds

# --- DATA FETCH FUNCTION ---
def fetch_data():
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?select=*"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Handle empty or single dict response
        if not data:
            return pd.DataFrame()
        if isinstance(data, dict):
            data = [data]

        return pd.DataFrame(data)

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching data from Supabase:\n{e}")
        return pd.DataFrame()

# --- UI SETUP ---
st.set_page_config(page_title="Live PayPal Dashboard", layout="wide")
st.title("📬 Live PayPal Transactions")
st.caption(f"Refreshing every {REFRESH_INTERVAL_SEC} seconds...")

# --- DISPLAY DATA ---
df = fetch_data()

if df.empty:
    st.warning("No transactions found yet.")
else:
    if "timestamp" in df.columns:
        df = df.sort_values("timestamp", ascending=False)

    st.dataframe(df, use_container_width=True)

# --- AUTO-REFRESH LOOP ---
# Wait and rerun the app
REFRESH_INTERVAL_MS = REFRESH_INTERVAL_SEC * 1000
st_autorefresh(interval=REFRESH_INTERVAL_MS, limit=None, key="datarefresh")
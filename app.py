import streamlit as st
import pandas as pd
import requests
import time
from streamlit_autorefresh import st_autorefresh
from dotenv import load_dotenv
import os

# --- ENV SETUP ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE_NAME = "paypal_webhooks"
REFRESH_INTERVAL_SEC = 1

# --- FETCH DATA FUNCTION ---
def fetch_data():
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?select=*"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Cache-Control": "no-cache"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data:
            return pd.DataFrame()
        if isinstance(data, dict):
            data = [data]

        return pd.DataFrame(data)

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching data from Supabase:\n{e}")
        return pd.DataFrame()

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Live PayPal Dashboard", layout="wide")
st.title("💸 Live PayPal Transactions")
st.caption(f"🔁 Auto-refreshing every {REFRESH_INTERVAL_SEC} seconds...")

# --- FETCH AND DISPLAY DATA ---
df = fetch_data()

if df.empty:
    st.warning("⚠️ No transactions found yet.")
else:
    if "transaction_time" in df.columns:
        df["transaction_time"] = pd.to_datetime(df["transaction_time"], errors='coerce')

        st.write("Sample raw transaction_time values:")
        st.write(df["transaction_time"].head(10))

        # Fix timezone awareness: localize naive timestamps, convert others to UTC
        if df["transaction_time"].dt.tz is None:
            df["transaction_time"] = df["transaction_time"].dt.tz_localize('UTC')
        else:
            df["transaction_time"] = df["transaction_time"].dt.tz_convert('UTC')

        st.write("Transaction time range in data:")
        st.write(df["transaction_time"].min(), "to", df["transaction_time"].max())

        today = pd.Timestamp.now(tz='UTC')
        week_ago = today - pd.Timedelta(days=7)

        mask = (df["transaction_time"] >= week_ago) & (df["transaction_time"] <= today)
        df_filtered = df.loc[mask]

        if df_filtered.empty:
            st.warning("⚠️ No transactions found in the last week.")
        else:
            df_filtered = df_filtered.sort_values("transaction_time", ascending=False).head(20)

            st.write(f"🗓 Showing {len(df_filtered)} transactions from {week_ago.date()} to {today.date()}")

            selected_columns = ["id", "amount", "transaction_time"]
            df_to_display = df_filtered[selected_columns] if all(col in df_filtered.columns for col in selected_columns) else df_filtered

            st.dataframe(df_to_display, use_container_width=True)

    else:
        st.warning("⚠️ 'transaction_time' column not found.")

# --- LIVE CLOCK ---
st.write("🕒 Last refresh:", time.strftime("%H:%M:%S"))

# --- AUTO-REFRESH ---
st_autorefresh(interval=REFRESH_INTERVAL_SEC * 1000, limit=None, key="datarefresh")
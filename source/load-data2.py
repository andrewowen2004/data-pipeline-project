# load-data.py
# Created by Andrew Owen on 2025-06-05.

import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import pandas as pd

# PayPal sandbox OAuth URL
oauth_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

# PayPal sandbox transaction search URL
transaction_url = "https://api-m.sandbox.paypal.com/v1/reporting/transactions"

# Replace these with your sandbox credentials
client_id = 'ASKxdNe-yzLc2pYPc4hBsmIFm6R2eWI81Min4YR4sTbNxoBzmRWHmwDj2WYUC69I1MNSRQxiR3_FebXc'
client_secret = 'EMQAZxAD0Clgijg6HyMpJiGfgbcrD02QXY_QGbKgO4YqSW_WoKgrZAM8rfQOK788aSMrELRyJg6oYJ5_'

def get_access_token():
    response = requests.post(
        oauth_url,
        auth=HTTPBasicAuth(client_id, client_secret),
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        data={"grant_type": "client_credentials"},
    )

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Access token retrieved successfully.")
        return access_token
    else:
        print("Failed to get access token:", response.text)
        return None

def get_transactions(access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "start_date": "2025-06-01T00:00:00-0700",
    "end_date": "2025-06-17T23:59:59-0700", 
        "fields": "all",
        "page_size": 100
    }

    response = requests.get(transaction_url, headers=headers, params=params)

    if response.status_code == 200:
        print("Transaction data retrieved successfully.")
        return response.json()
    else:
        print("Failed to retrieve transactions:", response.text)
        return None

def save_transactions_to_db(transactions_data, db_filename="/Users/andrewowen/Downloads/Summer25/data-pipeline-project/data/test.db", table_name="transactions"):
    transaction_details = transactions_data.get("transaction_details", [])

    if not transaction_details:
        print("No transactions to save to DB.")
        return

    records = []
    for detail in transaction_details:
        info = detail.get("transaction_info", {})
        record = {
            "transaction_id": info.get("transaction_id", ""),
            "date": info.get("transaction_initiation_date", ""),
            "amount": info.get("transaction_amount", {}).get("value", ""),
            "currency": info.get("transaction_amount", {}).get("currency_code", ""),
            "status": info.get("transaction_status", ""),
            "subject": info.get("transaction_subject", "")
        }
        records.append(record)

    df = pd.DataFrame(records)

    conn = sqlite3.connect(db_filename)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"Saved {len(df)} transactions to '{db_filename}' in table '{table_name}'.")

if __name__ == "__main__":
    token = get_access_token()
    if token:
        data = get_transactions(token)
        if data:
            save_transactions_to_db(data, db_filename="/Users/andrewowen/Downloads/Summer25/data-pipeline-project/data/test.db", table_name="transactions")

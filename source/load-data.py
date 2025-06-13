#
# data-pipeline-project
# load-data.py
# Created by Andrew Owen on 2025-06-05.
# 

import requests; from requests.auth import HTTPBasicAuth


# PayPal sandbox OAuth URL
oauth_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

client_id = 'ASKxdNe-yzLc2pYPc4hBsmIFm6R2eWI81Min4YR4sTbNxoBzmRWHmwDj2WYUC69I1MNSRQxiR3_FebXc'
client_secret = 'EMQAZxAD0Clgijg6HyMpJiGfgbcrD02QXY_QGbKgO4YqSW_WoKgrZAM8rfQOK788aSMrELRyJg6oYJ5_'

def get_access_token():
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(oauth_url, headers=headers, data=data,
                             auth=HTTPBasicAuth(client_id, client_secret))
    
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']
        print("Access token:", access_token)
        return access_token
    else:
        print("Failed to get access token:", response.text)
        return None

def get_transactions(access_token):
    transactions_url = "https://api-m.sandbox.paypal.com/v1/reporting/transactions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    # Query params: start_date and end_date in ISO8601 format (example: last 7 days)
    params = {
    "start_date": "2025-06-01T00:00:00-0700",
    "end_date": "2025-06-09T23:59:59-0700",  # <-- Updated
    "page_size": 3
}

    response = requests.get(transactions_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Transactions data:", data)
        return data
    else:
        print("Failed to get transactions:", response.text)
        return None

import csv  # Add at the top if not already there

def save_transactions_to_csv(transactions_data, filename="transactions.csv"):
    transaction_details = transactions_data.get("transaction_details", [])
    
    if not transaction_details:
        print("No transactions to save.")
        return

    # Choose what fields you want to extract
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Transaction ID", 
            "Date", 
            "Amount", 
            "Currency", 
            "Status", 
            "Subject"
        ])
        
        for detail in transaction_details:
            info = detail.get("transaction_info", {})
            writer.writerow([
                info.get("transaction_id", ""),
                info.get("transaction_initiation_date", ""),
                info.get("transaction_amount", {}).get("value", ""),
                info.get("transaction_amount", {}).get("currency_code", ""),
                info.get("transaction_status", ""),
                info.get("transaction_subject", "")
            ])
    
    print(f"Saved {len(transaction_details)} transactions to {filename}")


if __name__ == "__main__":
    token = get_access_token()
    if token:
        data = get_transactions(token)
        if data:
            save_transactions_to_csv(data, filename="transactions.csv")


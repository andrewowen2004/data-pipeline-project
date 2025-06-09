#
# data-pipeline-project
# load-data.py
# Created by Andrew Owen on 2025-06-05.
# 

import requests
from requests.auth import HTTPBasicAuth

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
        "start_date": "2025-05-31T00:00:00-0700",
        "end_date": "2025-06-07T23:59:59-0700",
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

if __name__ == "__main__":
    token = get_access_token()
    if token:
        get_transactions(token)


if __name__ == "__main__":
    get_access_token()




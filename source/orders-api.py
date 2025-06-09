import requests
import csv
import time

# PayPal API credentials (sandbox)
CLIENT_ID = 'ASKxdNe-yzLc2pYPc4hBsmIFm6R2eWI81Min4YR4sTbNxoBzmRWHmwDj2WYUC69I1MNSRQxiR3_FebXc'
CLIENT_SECRET = 'EMQAZxAD0Clgijg6HyMpJiGfgbcrD02QXY_QGbKgO4YqSW_WoKgrZAM8rfQOK788aSMrELRyJg6oYJ5_'
BASE_URL = 'https://api.sandbox.paypal.com'

# Get OAuth access token
def get_access_token():
    url = f"{BASE_URL}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()
    return response.json()['access_token']

# Create a new order
def create_order(access_token):
    url = f"{BASE_URL}/v2/checkout/orders"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    # Example order data — replace with your actual order details
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": "10.00"
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=order_data)
    response.raise_for_status()
    return response.json()

def main():
    access_token = get_access_token()
    orders_to_save = []

    for i in range(10):
        try:
            order = create_order(access_token)
            status = order.get('status')
            order_id = order.get('id')

            if status != "PAYER_ACTION_REQUIRED":
                print(f"Order {order_id} created with status {status} — saving.")
                # Save only relevant details to CSV
                orders_to_save.append({
                    "id": order_id,
                    "status": status,
                    # Add more fields if needed
                })
            else:
                print(f"Order {order_id} requires manual payer action — skipping.")
            
            # Optional: pause to avoid rate limits
            time.sleep(0.2)

        except Exception as e:
            print(f"Failed to create order: {e}")

    # Write all allowed orders to CSV
    with open('orders_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for order in orders_to_save:
            writer.writerow(order)

    print(f"Saved {len(orders_to_save)} orders to orders_data.csv")

if __name__ == "__main__":
    main()

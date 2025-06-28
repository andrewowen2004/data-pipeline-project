from fastapi import FastAPI, Request
from supabase import create_client
from dotenv import load_dotenv
import os, json

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI()

@app.post("/paypal/webhook")
async def paypal_webhook(request: Request):
    payload = await request.json()
    print("Webhook payload received:")
    print(json.dumps(payload, indent=2))

    resource = payload.get("resource", {})

    # Extract amount and convert safely
    amount_str = resource.get("amount", {}).get("value")
    try:
        amount = float(amount_str) if amount_str is not None else None
    except (ValueError, TypeError):
        amount = None

    currency = resource.get("amount", {}).get("currency_code")
    transaction_time = resource.get("create_time")

    print(f"Parsed amount: {amount}, currency: {currency}, transaction_time: {transaction_time}")

    supabase.table("paypal_webhooks").insert({
        "amount": amount,
        "transaction_time": transaction_time,
    }).execute()

    return {"status": "received"}
